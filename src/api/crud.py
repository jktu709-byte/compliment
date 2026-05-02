# CRUD functional work with session and data
from typing import List, Set
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,func,or_ #noqa
from src.models.comp_models import Gender,Compliment,Users,History#noqa
from src.schemas.comp_schemas import ComplimentSchema
from sqlalchemy.orm import selectinload
class ComplimentRepository:
    def __init__(self,session:AsyncSession) -> None:
        self.session = session

    async def create_compliment(self, title:str, gender:Gender|None, point:str,history:str) -> Compliment:
        obj = Compliment(title=title,gender = gender,point = point,history = history)
        self.session.add(obj)
        return obj
    
    async def get_compliment(self,complmnt_id:int)->Compliment|None:
        res = await self.session.execute(select(Compliment).filter(Compliment.id == complmnt_id))
        return res.scalar_one_or_none()
    
    async def get_all_compliments(self)->List[Compliment]:
        res = await self.session.execute(select(Compliment))
        return res.scalars().all()
    
    async def get_user_history(self,user_id:int)->None|List[History]:
        stmt = select(History).options(selectinload(History.compliment)).filter(History.user_id == user_id) #noqa
        res = await self.session.execute(stmt)
        return res.scalars().all()
    
    async def update_compliment(self,compliment_id:int,payload:ComplimentSchema)-> Compliment|None:
        obj = await self.get_compliment(compliment_id)
        if not obj:
            return None
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(obj,field,value)
        self.session.add(obj)
        self.session.flush(obj)
        self.session.refresh(obj)
        return obj 
         
    async def delete_compliment(self,compliment_id:int)->bool:
        obj = await self.get_compliment(compliment_id)
        if not obj:
            return False
        await self.session.delete(obj)
        return True
    
