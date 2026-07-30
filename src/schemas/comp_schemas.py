# Models for validation
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from src.models.comp_models import Compliment, Gender


# Валидация ответа
class UserCreate(BaseModel):
    name:str
    gender:Gender
    password:str

class ComplimentResponse(BaseModel):
    # as i know from_attributes might read field from objects attributes
    model_config = ConfigDict(from_attributes = True)
    title:str
    point:Optional[str]

class ComplimentListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    compliments_list: list[Compliment]
# валидация ответа истории
class ComplimentHistoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes= True)
    compliment:Optional[ComplimentResponse]
    created_at:datetime
# Проверка бд 
class ComplimentAppendDTO(BaseModel):
    model_config = ConfigDict(from_attributes= True)
    title:str
    gender:Gender
    point:Optional[str]