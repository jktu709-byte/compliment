# Models for validation
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional
from src.models.comp_models import Gender

class ComplimentResponse(BaseModel):
    # as i know from_attributes might read field from objects attributes
    model_config = ConfigDict(from_attributes = True)
    title:str
    point:Optional[str]

class ComplimentHistoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes= True)
    compliment:Optional[ComplimentResponse]
    created_at:datetime
class ComplimentSchema(BaseModel):
    model_config = ConfigDict(from_attributes= True)
    title:str
    gender:Optional[Gender|None]
    point:str|None
    