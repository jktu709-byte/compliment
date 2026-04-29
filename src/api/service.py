 # I use my crud functional for solving business problems.
import random
from fastapi import Depends #noqa
from sqlalchemy import select,func,or_ # noqa
from src.core.database import get_session #noqa
from src.models.comp_models import Gender,Compliment,History #noqa
from src.api.crud import ComplimentRepository #noqa

class ComplimentService:
    def __init__(self,repo:ComplimentRepository) -> None:
        # it's clean work,bcs service don't know about repository, only about object repo
        self.repo = repo
    
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
    
    