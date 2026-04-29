# Отдельный файл/класс для разного рода фильтраций
from sqlalchemy import func, or_, select

from src.models.comp_models import Compliment, Gender
class Filters():
    # фильтр по гендеру
    async def gender_compliment(self,gender:Gender)->Compliment|None:
        stmt = select(Compliment)
        
        if gender:
            stmt = stmt.filter(or_(Compliment.gender == gender,Compliment.gender.is_(None)))
        
        stmt = stmt.order_by(func.random()).limit(1)
        res = await self.session.execute(stmt)
        # res = 
        return res.scalar_one_or_none()
    # фильтр по дате добавления
    async def datetime_filter(self):
        pass    
    