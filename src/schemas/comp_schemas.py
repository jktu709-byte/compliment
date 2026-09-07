# Models for validation
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from src.models.comp_models import Compliment, Gender


class ComplimentResponse(BaseModel):
    # as i know from_attributes might read field from objects attributes
    model_config = ConfigDict(from_attributes = True)
    title:str
    point:str|None

class ComplimentListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    compliments_list: list[Compliment]
# валидация ответа истории
class ComplimentHistoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes= True)
    compliment:ComplimentResponse|None
    created_at:datetime
# Проверка бд 
class ComplimentAppendDTO(BaseModel):
    model_config = ConfigDict(from_attributes= True)
    title:str
    gender:Gender
    point:str|None

