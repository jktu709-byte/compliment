# CRUD functional work with session and data
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select #noqa
from src.models.comp_models import Gender,Compliment,History#noqa
from sqlalchemy.orm import selectinload
class ComplimentRepository:
    
    def __init__(self,session:AsyncSession) -> None:
        self.session = session

    async def create_compliment(self, title:str, gender:Gender|None, point:str) -> Compliment:
        obj = Compliment(title=title,gender = gender,point = point,)
        self.session.add(obj)
        return obj
    
    async def add_list(self, compliments:List[Compliment]):
        await self.session.add_all(compliments)
         
    async def get_compliment(self,complmnt_id:int)->Compliment|None:
        res = await self.session.execute(select(Compliment).filter(Compliment.id == complmnt_id))
        return res.scalar_one_or_none()
    
    async def get_all_compliments(self)->List[Compliment]:
        res = await self.session.execute(select(Compliment))
        return res.scalars().all()
    
    async def get_user_history(self,user_id:int)->List[History]:
        stmt = select(
            History
            ).options(selectinload(History.compliment)
                      ).filter(History.user_id == user_id
                               ).order_by(History.created_at.desc()
                                          ).limit(25) #noqa
        res = await self.session.execute(stmt)
        return res.scalars().all()
         
    async def delete_compliment(self,compliment_id:int)->bool:
        obj = await self.get_compliment(compliment_id)
        if not obj:
            return False
        await self.session.delete(obj)
        return True
    
    async def commit(self):
        await self.session.commit()