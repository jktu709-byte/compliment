# Models for validation
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from src.models.comp_models import Compliment, Gender


class ComplimentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    gender: Gender
    title: str
    point: str | None
    created_at: datetime

class ComplimentListResponse(BaseModel):
    compliments: list[ComplimentResponse]
# Проверка бд 
class ComplimentAppendDTO(BaseModel):
    model_config = ConfigDict(from_attributes= True)
    title:str
    gender:Gender
    point:str|None

