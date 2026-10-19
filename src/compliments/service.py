import json
import random

from fastapi import UploadFile

from src.compliments.repository import ComplimentRepository
from src.exceptions.semantic_exceptions import (
    ComplimentAlreadyExistsError,  #noqa
    ComplimentNotFoundError,
)
from src.models.comp_models import Compliment, Gender, History  #noqa
from src.schemas.comp_schemas import ComplimentAppendDTO
from src.user.repository import UserRepository


class ComplimentService:
    def __init__(self,repo:ComplimentRepository,u_repo:UserRepository):
        self.repo = repo
        self.u_repo = u_repo
    # подумать над целесообразностью async в cpu задаче
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
            return "No data"  
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
            raise ComplimentNotFoundError("Compliments does not exists")
        # check history
        set_history_ids = await self.u_repo.get_user_history(user_id= user_id)
        # check available
        available = [compliment for compliment in all_compliments if compliment.id not in set_history_ids]
        # if available emptyh -> return all
        if not available:
            available = all_compliments
        # get random compliment from available compliments 
        chosen = random.choice(available)
        # history note 
        history_row = History(compliment_id = chosen.id, user_id = user_id)
        # save history
        await self.u_repo.add_history(user_id=history_row.user_id)
        # save all
        await self.repo.commit()
        return chosen # type: ignore
    
    async def list_compliments(self) -> list[Compliment]:
        res = await self.repo.get_all_compliments()
        if not res:
            raise ComplimentNotFoundError("Список комплиментов не был найден")
        return res
    
    async def get_history(self,user_id:int):
        list_history = self.u_repo.get_user_history(user_id=user_id)
        if not list_history:
            raise ComplimentNotFoundError("Комплимент(ы) не был(и) найден(ы)")
        return list_history
    
    async def change_compliment(self,comp_id:int):
        # достаю данные
        obj = await self.repo.get_compliment(complmnt_id=comp_id)
        if not obj:
            raise ComplimentNotFoundError("Комплимент(ы) не был(и) найден(ы)")
        # инициализируем поле и значение в модели 
        compliment_dto = ComplimentAppendDTO(title=obj.title,gender=obj.gender,point=obj.point)
        for field, value in compliment_dto.model_dump(exclude_unset=True).items():
            # Задаем новые значени 
            setattr(obj,field,value)
        # Сохраняем,передаем и перемешиваем объект
        await self.u_repo.add_obj(obj)
        await self.u_repo.refresh_obj(obj)
        await self.u_repo.commit()
        return obj