from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,func,or_
from src.models.comp_models import Gender,Compliment #noqa
from src.api.crud import ComplimentRepository
class ComplimentService():
    def __init__(self,session:AsyncSession) -> None:
        self.session = session
    # There is need to be an uncommon stuff like history view and remove something useless. 
    # I should use my crud functional for this.
        
    async def get_compliment(self,):
        pass
            
    async def random_compliment(self,gender:Gender)->Compliment|None:
        stmt = select(Compliment)
        
        if gender:
            stmt = stmt.filter(or_(Compliment.gender == gender,Compliment.gender.is_(None)))
        
        stmt = stmt.order_by(func.random()).limit(1)
        res = await self.session.execute(stmt)
        # res = 
        return res.scalar_one_or_none()