from datetime import UTC, datetime, timedelta

from src.auth.security import security
from src.celery.tasks import send_email
from src.exceptions.semantic_exceptions import (
    InvalidEmailVerificationTokenError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from src.models.comp_models import Gender
from src.users.repository import UserRepository
from src.auth.tokens import token_helper

class UserService:
    def __init__(self,repo:UserRepository):
        self.repo = repo
        
    async def register(self,name:str,email:str,gender:Gender,password:str):
        existing = await self.repo.get_user_by_email(email)
        if existing:
            raise UserAlreadyExistsError("Пользователь с таким email уже существует")
        user = await self.repo.create_user(
            u_name=name,
            u_gender=gender,
            u_email = email,
            u_password_hash=security.hash_password(password)
            )
        raw_token, token_hash = token_helper.generate_token()
        expires_at = datetime.now(UTC) + timedelta(minutes=30)

        await self.repo.create_email_verification_token(
            user_id=user.id,
            expires=expires_at,
            token_hash=token_hash,
        )
        await self.repo.commit()
        send_email.delay(to_email = user.email,subject = 'Email Verification',body=raw_token)
        return user

    async def get_email(self,email:str):
        user = await self.repo.get_user_by_email(email=email)
        return user

    async def confirm_email(self, raw_token: str) -> None:
        token_hash = token_helper.hash_token(raw_token)
        email_token = await self.repo.get_email_verification_token_by_hash(token_hash)
        # Засекаю время
        now = datetime.now(UTC)
        # откидываю лишнее и сверяю время
        if email_token is None or email_token.expires_at <= now:
            raise InvalidEmailVerificationTokenError()
        # ищу пользователя
        user = await self.repo.get_user_by_id(email_token.user_id)
        if user is None:
            raise UserNotFoundError()
        # подтверждаю верификацию и устанавливаю время
        user.email_verified_at = now
        await self.repo.delete_email_verification_token(email_token)
        await self.repo.commit()
