import pytest #noqa
from src.models.comp_models import Compliment, Gender
from sqlalchemy.ext.asyncio import AsyncSession
class Complmnt_Factory:
    
    def __init__(self,session:AsyncSession):
        self.session = session
        
    async def create_complmnt(self) -> Compliment:
        complmnt = Compliment(title= "test_title",point= "test_point",gender=Gender.neutral)
        self.session.add(complmnt)  # type: ignore
        await self.session.flush([complmnt])
        return complmnt