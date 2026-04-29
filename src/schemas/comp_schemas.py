# Models for validation
from pydantic import BaseModel
from typing import Optional
from src.models.comp_models import Gender

class ComplimentSchema(BaseModel):
    title:str
    gender:Optional[Gender|None]
    point:Optional[str|None]
    