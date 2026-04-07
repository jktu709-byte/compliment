from pydantic import BaseModel
from typing import Optional
from models.models import Gender

class ComplimentSchema(BaseModel):
    title:str
    gender:Optional[Gender|None]
    point:Optional[str|None]
    