import random
from fastapi import Depends #noqa
from sqlalchemy import select,func,or_
from src.core.database import get_session #noqa
from src.models.comp_models import Gender,Compliment,History #noqa
from src.api.crud import ComplimentRepository #noqa
from src.utils.depends import get_repo

# There is need to be an uncommon stuff like history view and remove something useless. 
    # I should use my crud functional for this.
class ComplimentService():
    def __init__(self,repo) -> None:
        # it's clean work,bcs service don't know about repository, only about object repo
        self.repo = get_repo
    
    async def get_compliment_for_user(self,user_id:int):
        # нужен объект класса, иначе сессия не воркает
        # Check all compliments
        all_compliments = await self.repo.get_all_compliments()
        # if list empty return None
        if not all_compliments:
            return None 
        # check history
        set_history_ids = await self.repo.get_all_history(user_id= user_id)
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
        self.repo.add(history_row)
        # save all
        await self.repo.commit()
        return chosen
    
    async def change_compliment():
        return ComplimentRepository.update_compliment()
    
    async def gender_compliment(self,gender:Gender)->Compliment|None:
        stmt = select(Compliment)
        
        if gender:
            stmt = stmt.filter(or_(Compliment.gender == gender,Compliment.gender.is_(None)))
        
        stmt = stmt.order_by(func.random()).limit(1)
        res = await self.session.execute(stmt)
        # res = 
        return res.scalar_one_or_none()