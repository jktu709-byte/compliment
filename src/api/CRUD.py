from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,func,or_
from src.models.models import Gender,Compliment,History #noqa

# Мой класс отвечает за огромное количество вещей. Это как-то не по SRP.Разберись с этим
# Наследование? Подкласс? Отдельные модули? Вынести рандом в бизнес логику, ведь это не crud
# Все калссы могут коммитить. Отделный класс под сохранение? Прописать атрибут в __init__?
class ComplimentCRUD():
    def __init__(self,session:AsyncSession) -> None:
        self.session = session
    
    async def create_compliment(self, title:str, gender:Gender|None, meaning:str,history:str) -> Compliment:
        obj = Compliment(title=title,gender = gender,meaning = meaning,history = history)
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
    
    async def update_compliment(self,compliment_id:int,**kwargs)-> Compliment|None:
        obj = await self.get_compliment(compliment_id)
        if not obj:
            return None
        # проблема безопасности
        for key, value in kwargs.items():
            setattr(obj,key,value)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj 

    async def random_compliment(self,gender:Gender)->Compliment|None:
        stmt = select(Compliment)
        
        if gender:
            stmt = stmt.filter(or_(Compliment.gender == gender,Compliment.gender.is_(None)))
        
        stmt = stmt.order_by(func.random()).limit(1)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none() 
            
    async def delete_compliment(self,compliment_id:int)->bool:
        obj = await self.get_compliment(compliment_id)
        if not obj:
            return False
        await self.session.delete(obj)
        await self.session.commit()
        return True
    
   