 # I use my crud functional for solving business problems.
import json
import random
from datetime import datetime, timedelta, timezone

from fastapi import UploadFile

from src.api.repository import AuthRepository, ComplimentRepository, UserRepository
from src.auth.auth_config import auth_settings
from src.auth.security import security
from src.auth.tokens import token_helper
from src.exceptions.semantic_exceptions import (
    ComplimentAlreadyExistsError,  #noqa
    ComplimentNotFoundError,
    InvalidCredentialsError,
    RefreshTokenExpiredError,
    RefreshTokenNotFoundError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from src.models.comp_models import Compliment, Gender, History, User
from src.schemas.auth import TokenPairSchema
from src.schemas.comp_schemas import ComplimentAppendDTO


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
        # if available empty -> return all
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
    
class AuthService:
    
    def __init__(
        self,
        auth_repo:AuthRepository,
        user_repo:UserRepository
        ):
        self.auth_repo = auth_repo
        self.user_repo = user_repo
        
    async def login(self,email:str,password:str):
        user = await self._get_user_or_raise(u_email=email,password=password)
        token_pair = await self._issue_tokens(user_id=user.id)
        return token_pair.access_token,token_pair.refresh_token
    
    async def refresh_token(self,raw_token:str):
        stored = await self._get_valid_refresh(raw_token=raw_token)
        user = await self._get_user_for_token(stored.user_id)
        await self.auth_repo.delete_refresh_token(stored)
        pair = await self._issue_tokens(user.id)
        return pair
    
    async def _get_user_or_raise(self,u_email:str,password:str) ->User:
            user = await self.user_repo.get_user_by_email(email=u_email)
            if not user:
                raise UserNotFoundError("Пользователь не найден")
            if not security.verify_password(password=password,password_hash=user.password_hash):
                raise InvalidCredentialsError("Неверный логин или пароль") 
            return user
    
    async def _get_valid_refresh(self,raw_token:str):
        token_hash = token_helper.hash_session_token(raw_token)
        stored = await self.auth_repo.get_refresh_token(token_hash=token_hash)
        if not stored or stored.revoked:
            raise RefreshTokenNotFoundError()
        # прописываем удаление токена
        now = datetime.now(timezone.utc)
        if stored.expires_at <= now:
             await self.auth_repo.delete_refresh_token(stored) #можно удалить пакетами через cron
             raise RefreshTokenExpiredError()
        return stored
        
    async def _get_user_for_token(self,user_id:int):
        user = await self.user_repo.get_user_by_id(user_id=user_id)
        if not user:
            raise UserNotFoundError
        return user

    def _refresh_expiry(self) -> datetime:
        return datetime.now(timezone.utc) + timedelta(minutes=auth_settings.refresh_token_expires_minutes)
    # здесь собирается токен для последующего использования в логине
    async def _issue_tokens(self, user_id: int) -> TokenPairSchema:
        access_token = token_helper.create_access_token(user_id)
        refresh_token = token_helper.create_refresh_token()
        refresh_hash = token_helper.hash_session_token(refresh_token)
        expires_at = self._refresh_expiry()
        await self.auth_repo.create_refresh_token(user_id=user_id,token_hash=refresh_hash,expires=expires_at)
        await self.auth_repo.commit()
        return TokenPairSchema(access_token=access_token, refresh_token=refresh_token)
class UserService:
    def __init__(self,repo:UserRepository):
        self.repo = repo
        
    async def register(self,name:str,email:str,gender:Gender,password:str):
        existing = self.repo.get_user_by_email(email)
        if existing:
            raise UserAlreadyExistsError("Пользователь с таким email уже существует")
        user = await self.repo.create_user(u_name=name,u_gender=gender,u_email = email,u_password_hash=security.hash_password(password))
        await self.repo.commit()
        return user