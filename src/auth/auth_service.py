from datetime import datetime, timedelta, timezone

from src.auth.auth_config import auth_settings
from src.auth.auth_repository import AuthRepository
from src.auth.security import security
from src.auth.tokens import token_helper
from src.exceptions.semantic_exceptions import (
    InvalidCredentialsError,
    RefreshTokenExpiredError,
    RefreshTokenNotFoundError,
    UserNotFoundError,
)
from src.models.comp_models import User
from src.schemas.auth_schemas import TokenPairSchema
from src.user.repository import UserRepository


class AuthService:
    
    def __init__(
        self,
        auth_repo:AuthRepository,
        user_repo:UserRepository
        ):
        self.auth_repo = auth_repo
        self.user_repo = user_repo
        
    async def login(self,email:str,password:str):
        user = await self._get_user_or_raise(u_email=email,password=password)
        token_pair = await self._issue_tokens(user_id=user.id)
        return token_pair.access_token,token_pair.refresh_token
    
    async def refresh_token(self,raw_token:str):
        stored = await self._get_valid_refresh(raw_token=raw_token)
        user = await self._get_user_for_token(stored.user_id)
        await self.auth_repo.delete_refresh_token(stored)
        pair = await self._issue_tokens(user.id)
        return pair
    
    async def _get_user_or_raise(self,u_email:str,password:str) ->User:
            user = await self.user_repo.get_user_by_email(email=u_email)
            if not user:
                raise UserNotFoundError("Пользователь не найден")
            if not security.verify_password(password=password,password_hash=user.password_hash):
                raise InvalidCredentialsError("Неверный логин или пароль") 
            return user
    
    async def _get_valid_refresh(self,raw_token:str):
        token_hash = token_helper.hash_session_token(raw_token)
        stored = await self.auth_repo.get_refresh_token(token_hash=token_hash)
        if not stored or stored.revoked:
            raise RefreshTokenNotFoundError()
        # прописываем удаление токена
        now = datetime.now(timezone.utc)
        if stored.expires_at <= now:
             #можно удалить пакетами через cron
             await self.auth_repo.delete_refresh_token(stored) 
             raise RefreshTokenExpiredError()
        return stored
        
    async def _get_user_for_token(self,user_id:int):
        user = await self.user_repo.get_user_by_id(user_id=user_id)
        if not user:
            raise UserNotFoundError
        return user

    def _refresh_expiry(self) -> datetime:
        """Продлевает токен по мере расходования"""
        return datetime.now(timezone.utc) + timedelta(minutes=auth_settings.refresh_token_expires_minutes)
    # здесь собирается токен для последующего использования в логине
    async def _issue_tokens(self, user_id: int) -> TokenPairSchema:
        access_token = token_helper.create_access_token(user_id)
        refresh_token = token_helper.create_refresh_token()
        refresh_hash = token_helper.hash_session_token(refresh_token)
        expires_at = self._refresh_expiry()
        await self.auth_repo.create_refresh_token(user_id=user_id,token_hash=refresh_hash,expires=expires_at)
        await self.auth_repo.commit()
        return TokenPairSchema(access_token=access_token, refresh_token=refresh_token)