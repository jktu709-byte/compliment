from src.auth.security import security
from src.exceptions.semantic_exceptions import (
    UserAlreadyExistsError,
)
from src.models.comp_models import Gender
from src.user.repository import UserRepository


class UserService:
    def __init__(self,repo:UserRepository):
        self.repo = repo
        
    async def register(self,name:str,email:str,gender:Gender,password:str):
        existing = self.repo.get_user_by_email(email)
        if existing:
            raise UserAlreadyExistsError("Пользователь с таким email уже существует")
        user = await self.repo.create_user(u_name=name,u_gender=gender,u_email = email,u_password_hash=security.hash_password(password))
        await self.repo.commit()
        return user