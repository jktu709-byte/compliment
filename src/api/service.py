import random
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select,func,or_
from src.models.comp_models import Gender,Compliment,History #noqa
from src.api.crud import ComplimentRepository #noqa
class ComplimentService():
    def __init__(self,session:AsyncSession) -> None:
        self.session = session
    # There is need to be an uncommon stuff like history view and remove something useless. 
    # I should use my crud functional for this.
        
    async def get_compliment_for_user(self,user_id:int):
        # нужен объект класса, иначе сессия не воркает
        repo = ComplimentRepository(self.session)
        # Check all compliments
        all_compliments = await repo.get_all_compliments()
        # if list empty return None
        if not all_compliments:
            return None 
        # check history
        set_history_ids = await repo.get_all_history(user_id= user_id)
        # check available
        available = [compliment for compliment in all_compliments if compliment.id not in set_history_ids]
        # if available empty -> return all
        if not available:
            available = all_compliments
        # get random compliment from available compliments 
        chosen = random.choice(available)
        # history note 
        history_row = History(compliment_id = chosen.id, user_id = user_id)
        # save history
        self.session.add(history_row)
        # save all
        await self.session.commit()
        return chosen
    
    async def gender_compliment(self,gender:Gender)->Compliment|None:
        stmt = select(Compliment)
        
        if gender:
            stmt = stmt.filter(or_(Compliment.gender == gender,Compliment.gender.is_(None)))
        
        stmt = stmt.order_by(func.random()).limit(1)
        res = await self.session.execute(stmt)
        # res = 
        return res.scalar_one_or_none()