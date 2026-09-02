 # I use my crud functional for solving business problems.
import json
import random
from datetime import datetime, timedelta, timezone

from fastapi import UploadFile

from src.api.repository import AuthRepository, ComplimentRepository, UserRepository
from src.auth.security import security
from src.auth.tokens import token_helper
from src.core.auth_config import auth_settings
from src.exceptions.semantic_exceptions import (
    ComplimentAlreadyExistsError,
    ComplimentNotFoundError,
    InvalidCredentialsError,
    RefreshTokenExpiredError,
    RefreshTokenNotFoundError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from src.models.comp_models import Compliment, Gender, History
from src.schemas.auth import TokenPair
from src.schemas.comp_schemas import ComplimentAppendDTO


class ComplimentService:
    def __init__(self,repo:ComplimentRepository):
        self.repo = repo
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
        
        НАПИШИ ПРОВЕРКУ ВХОДЯЩИХ ДАННЫХ!!!!
        
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
            raise ComplimentNotFoundError()
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
        if not res:
            raise ComplimentNotFoundError("Список комплиментов не был найден")
        return res
    
    async def get_history(self,user_id:int):
        list_history = self.repo.get_user_history(user_id=user_id)
        if not list_history:
            raise ComplimentNotFoundError()
        return list_history
    
    async def change_compliment(self,comp_id:int):
        # достаю данные
        obj = await self.repo.get_compliment(complmnt_id=comp_id)
        if not obj:
            raise ComplimentNotFoundError()
        # инициализируем поле и значение в модели 
        for field, value in ComplimentAppendDTO.model_dump(exclude_unset=True).items():
            # Задаем новые значени 
            setattr(obj,field,value)
        # Сохраняем,передаем и перемешиваем объект
        self.session.add(obj)
        self.session.flush(obj)
        self.session.refresh(obj)
        return obj
    
class AuthService:
    
    def __init__(
        self,
        auth_repo:AuthRepository,
        user_repo:UserRepository
        ):
        self.auth_repo = auth_repo
        self.user_repo = user_repo
        
    async def login(self,name:str,password:str) -> TokenPair:
        user = self._get_user_or_raise(name=name,password=password)
        token_pair = self._issue_tokens(user.id)
        return token_pair.acces_token,token_pair.refresh_token
    
    async def refresh_token(self,raw_token:str):
        stored = self._get_valid_refresh(raw_token=raw_token)
        user = self._get_user_for_token(stored.user_id)
        await self.auth_repo.delete_refresh_token(stored)
        pair = self._issue_tokens(user.id)
        return pair
    
    async def _get_valid_refresh(self,raw_token:str):
        token_hash = token_helper.hash_session_token(raw_token)
        stored = await self.auth_repo.get_refresh_token(token_hash=token_hash)
        if not stored or stored.revoked:
            raise RefreshTokenNotFoundError
        # прописываем удаление токена
        now = datetime.now(timezone.utc)
        if stored.expires_at <= now:
             await self.auth_repo.delete_refresh_token(stored) #можно удалить пакетами через cron
             raise RefreshTokenExpiredError
        return stored
        
    async def _get_user_for_token(self,user_id:int):
        user = await self.user_repo.get_user_by_id(user_id=user_id)
        if not user:
            raise UserNotFoundError
        return user
    ИМЯ НЕ УНИКАЛЬНЫЙ КЛЮЧ. А ЧТО БУДЕТ ЕСЛИ ЕСТЬ ДУПЛИКАТ? НЕ ДАВАТЬ ДВУМ РАЗНЫМ ЛЮДЯМ ДОСТУП ИЗ-ЗА ОДНОГО ИМЕНИ? НЕДАЛЬНОВИДНО
    async def _get_user_or_raise(self,name:str,password:str):
        user = await self.user_repo.get_user_by_name(name)
        if not user or not security.verify_password(password=password,password_hash=user.password_hash):
            raise InvalidCredentialsError("Неверный логин или пароль") 
        return user
    
    def _refresh_expiry(self) -> datetime:
        return datetime.now(timezone.utc) + timedelta(minutes=auth_settings.refresh_token_expires_minutes)
    # здесь собирается токен для последующего использования в логине
    async def _issue_tokens(self, user_id: int) -> TokenPair:
        refresh_token = token_helper.create_refresh_token()
        refresh_hash = token_helper.hash_session_token(refresh_token)
        access_token = token_helper.create_access_token(user_id)
        expires_at = self._refresh_expiry()
        await self.db.auth.create_refresh_token(user_id=user_id, token_hash=refresh_hash, expires_at=expires_at)
        await self.db.session.commit()
        return TokenPair(access_token=access_token, refresh_token=refresh_token)
class UserService:
    def __init__(self,repo:UserRepository):
        self.repo = repo
        
    async def register(self,name:str,gender:Gender,password:str):
        existing = self.repo.get_user_by_name(name)
        if existing:
            raise UserAlreadyExistsError
        user = await self.repo.create_user(u_name=name,u_gender=gender,u_password_hash=security.hash_password(password))
        await self.repo.commit()
        return user