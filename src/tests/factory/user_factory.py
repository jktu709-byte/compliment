from sqlalchemy.ext.asyncio import AsyncSession

from src.models.comp_models import User


class User_Factory:
    
    def __init__(self,session:AsyncSession) -> None:
        self.session = session
        
    async def create_user(
        self,
        name="test_name",
        email="test_email",
        role="test_role",
        password_hash="test_hash"
        ):
        user = User(name=name,email=email,role=role,password_hash=password_hash)
        self.session.add(user)
        await self.session.flush([user])
        return user
    