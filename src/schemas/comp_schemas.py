# Models for validation
from pydantic import BaseModel, ConfigDict
from typing import Optional
from src.models.comp_models import Gender

class ComplimentResponse(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    title:str
    point:Optional[str]
class ComplimentSchema(BaseModel):
    title:str
    gender:Optional[Gender|None]
    point:str|None
    