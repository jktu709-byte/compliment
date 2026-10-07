
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.comp_models import Compliment, Gender, History, User


class UserRepository:
    
    def __init__(self,session:AsyncSession) -> None:
        self.session = session
                
    async def get_user_role(self,user_id:int):
        querry = await self.session.execute(
            select(User.role).
            where(User.id == user_id)
        )
        return querry
    
    async def add_history(self,user_id:int): 
        self.session.add(instance=History) #instance= куда добавить, конкретно что добавляем
    
    async def get_user_by_name(self,name:str)-> Result[tuple[User]]|None: 
        return await self.session.execute(
            select(User).
            where(User.name == name)
        )
    
    async def get_user_by_email(self,email:str) -> User|None: 
        res = await self.session.execute(select(User).where(User.email == email))
        return res.scalar_one_or_none()
    
    async def get_user_by_id(self,user_id:int)-> User|None: 
        return await self.session.get(User, user_id)
    
    async def create_user(self,u_name:str,u_email:str,u_gender:Gender,u_password_hash:str):
        user = User(
            name = u_name,
            u_email = u_email,
            gender = u_gender,
            password_hash = u_password_hash)
        self.session.add(user)
        await self.session.flush()
        return user
    
    async def get_all_users(self):
        return await self.session.execute(select(User))
        
    
    async def get_user_history(self,user_id:int)->list[History]:
        stmt = select(
            History).options(selectinload(History.compliment)).filter(History.user_id == user_id
                               ).order_by(History.created_at.desc()).limit(25) 
        res = await self.session.execute(stmt)
        return list(res.scalars().all())
    
    async def add_obj(self,obj):
        self.session.add(obj)
    
    async def refresh_obj(self,obj):
        await self.session.refresh(obj)    
    
    async def commit(self):
        await self.session.commit()
    

        
