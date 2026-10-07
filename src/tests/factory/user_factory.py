from sqlalchemy.ext.asyncio import AsyncSession

from src.models.comp_models import Role, User


class User_Factory:
    
    def __init__(self,session:AsyncSession) -> None:
        self.session = session
        
    async def base_test_user(self,role=Role.BASEUSER) -> User:
        test_user = User(
            name="test_name",
            email="test_email123@gmail.com",
            role=role,
            password_hash="random_hash")
        self.session.add(test_user)
        await self.session.flush([test_user])
        return test_user
    
    async def admin_test_user(self,role=Role.ADMIN) -> User:
            test_user = User(
                name="test_name",
                email="test_email123@gmail.com",
                role=role,
                password_hash="random_hash")
            self.session.add(test_user)
            await self.session.flush([test_user])
            return test_user
        
    async def moderator_test_user(self,role=Role.MODERATOR) -> User:
            test_user = User(
                name="test_name",
                email="test_email123@gmail.com",
                role=role,
                password_hash="random_hash")
            self.session.add(test_user)
            await self.session.flush([test_user])
            return test_user
        