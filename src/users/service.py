from datetime import UTC, datetime, timedelta

from src.auth.security import security
from src.exceptions.semantic_exceptions import (
    UserAlreadyExistsError,
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
        _raw_token, token_hash = token_helper.generate_sesion_token()
        expires_at = datetime.now(UTC) + timedelta(minutes=30)

        await self.repo.create_email_verification_token(
            user_id=user.id,
            expires=expires_at,
            token_hash=token_hash,
        )
        await self.repo.commit()
        return user

    async def get_email(self,email:str):
        user = await self.repo.get_user_by_email(email=email)
        return user