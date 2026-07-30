from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.comp_models import Compliment, Gender, History, User


class Repository:
    def __init__(self,session:AsyncSession) -> None:
            self.session = session
class UserRepository(Repository):
    
    async def get_user_role(self,user_id:int):
        querry = await self.session.execute(select(User.role).where(User.id == user_id))
        return querry
    
    async def get_user_by_name(self,name:str)-> User|None:
        return await self.session.execute(select(User).where(User.name == name))
    
    async def get_user_by_id(self,user_id:int)-> User|None:
        return await self.session.get(User, user_id)
    
    async def create_user(self,u_name:str,u_gender:Gender,u_password_hash:str):
        user = User(name = u_name,gender = u_gender,password_hash = u_password_hash)
        self.session.add(user)
        await self.session.flush()
        return user
    
    async def get_all_users(self):
        return await self.session.execute(select(User))
        
    
    async def get_user_history(self,user_id:int)->list[History]:
        stmt = select(
            History
            ).options(selectinload(History.compliment)
                      ).filter(History.user_id == user_id
                               ).order_by(History.created_at.desc()
                                          ).limit(25) 
        res = await self.session.execute(stmt)
        return res.scalars().all()
    
class ComplimentRepository(Repository):
    
    async def create_compliment(self, title:str, gender:Gender|None, point:str) -> Compliment:
        obj = Compliment(title=title,gender = gender,point = point,)
        self.session.add(obj)
        return obj
    
    async def add_list(self, compliments:list[Compliment]):
        await self.session.add_all(compliments)
         
    async def get_compliment(self,complmnt_id:int)->Compliment|None:
        res = await self.session.execute(select(Compliment).filter(Compliment.id == complmnt_id))
        return res.scalar_one_or_none()
    
    async def get_all_compliments(self)->list[Compliment]:
        res = await self.session.execute(select(Compliment))
        return res.scalars().all()
         
    async def delete_compliment(self,compliment_id:int)->bool:
        obj = await self.get_compliment(compliment_id)
        if not obj:
            return False
        await self.session.delete(obj)
        return True
    
    async def commit(self):
        await self.session.commit()
        
class AuthRepository(Repository):
    
    async def get_user_status(self,):
        ...