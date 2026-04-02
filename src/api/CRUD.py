from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,func,or_ #noqa
from src.models.models import Gender,Compliment#noqa
from src.schemas.schemas import ComplimentSchema
# Мой класс отвечает за огромное количество вещей. Это как-то не по SRP.Разберись с этим
# Вынести рандом в бизнес логику.
# Unit of work?
class ComplimentRepository():
    def __init__(self,session:AsyncSession) -> None:
        self.session = session
    
    async def create_compliment(self, title:str, gender:Gender|None, point:str,history:str) -> Compliment:
        obj = Compliment(title=title,gender = gender,point = point,history = history)
        self.session.add(obj)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj
    
    async def get_compliment(self,compliment_id:int)->Compliment|None:
        res = await self.session.execute(select(Compliment).filter(Compliment.id == compliment_id))
        return res.scalar_one_or_none()
    
    async def get_all_compliments(self)->Sequence[Compliment]:
        res = await self.session.execute(select(Compliment))
        return res.scalars().all()
    
    # это будет @put endpoint
    async def update_compliment(self,compliment_id:int,payload:ComplimentSchema)-> Compliment|None:
        obj = await self.get_compliment(compliment_id)
        if not obj:
            return None
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(obj,field,value)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj 
         
    async def delete_compliment(self,compliment_id:int)->bool:
        obj = await self.get_compliment(compliment_id)
        if not obj:
            return False
        await self.session.delete(obj)
        await self.session.commit()
        return True
    
