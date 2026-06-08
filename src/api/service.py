 # I use my crud functional for solving business problems.
import json
import random
from fastapi import Depends, UploadFile #noqa
from src.models.comp_models import Gender,Compliment,History #noqa
from src.api.crud import ComplimentRepository #noqa
from src.schemas.comp_schemas import ComplimentAppendDTO
class ComplimentService:
    
    def __init__(self,repo:ComplimentRepository) -> None:
        # it's clean work,bcs service don't know about repository, only about object repo
        self.repo = repo
    
    async def input_data_from_file(
        self,
        file:UploadFile,
        ):
        # получаем данные на входе(файл) и распаковываем их
        data = json.load(file.file)
        
        if "compliments" not in data:
            raise KeyError
        # простенькая валидация на всякую бяку  
        valid_data = [ComplimentAppendDTO.model_validate(item) for item in data["compliments"]]
        # если ничего не передали - дальше не идем, возвращаем None
        print(type(valid_data))
        
        if not valid_data:
            return None  
        # Если данные есть пробуем занести их в базу
        entities = [Compliment(title = i.title,point = i.point,gender = i.gender) for i in valid_data]
        print(entities[0])
        # Добавляем/сохраняем
        await self.repo.add_list(compliments=entities)
        await self.repo.commit()
        print(f"Данные добавлены успешно: {len(entities)}")       
        
    async def get_compliment_for_user(self,user_id:int) -> int|None:
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
    
    async def list_compliments(self) -> list[Compliment]:
        res = await self.repo.get_all_compliments()
        return res
    
    async def get_history(self,user_id:int):
        list_history = self.repo.get_user_history(user_id=user_id)
        if not list_history:
            return None
        return list_history
    
    async def change_compliment(self,comp_id:int):
        # достаю данные
        obj = await self.repo.get_compliment(complmnt_id=comp_id)
        if not obj:
            return None
        # инициализируем поле и значение в модели 
        for field, value in ComplimentAppendDTO.model_dump(exclude_unset=True).items():
            # Задаем новые значени 
            setattr(obj,field,value)
        # Сохраняем,передаем и перемешиваем объект
        self.session.add(obj)
        self.session.flush(obj)
        self.session.refresh(obj)
        return obj
    
    