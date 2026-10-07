from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.comp_models import Compliment, Gender, History, User  #noqa


class ComplimentRepository:
    
    def __init__(self,session:AsyncSession) -> None:
        self.session = session
    
    async def add_compliment(self, title:str, gender:Gender|None, point:str) -> Compliment:
        obj = Compliment(
            title=title,
            gender = gender,
            point = point,
        )
        self.session.add(obj)
        return obj
    
    async def add_list(self, compliments:list[Compliment]):
        res = self.session.add_all(compliments)
        await res # type: ignore
         
    async def get_compliment(self,complmnt_id:int)->Compliment|None:
        res = await self.session.execute(
            select(Compliment)
            .filter(Compliment.id == complmnt_id))
        return res.scalar_one_or_none()
    
    async def get_all_compliments(self)->list[Compliment]:
        res = await self.session.execute(select(Compliment))
        # тут возвращается последовательность, поэтому ради типизации и чтобы линтер не ругался я просто воткну надстройку
        return list(res.scalars().all())
         
    async def delete_compliment(self,compliment_id:int)->bool:
        obj = await self.get_compliment(compliment_id)
        if not obj:
            return False
        await self.session.delete(obj)
        return True
    
    async def commit(self):
        await self.session.commit()