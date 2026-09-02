from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from src.models.comp_models import Gender


# Валидация ответа
class UserCreate(BaseModel):
    name:str
    email:EmailStr
    gender:Gender
    password:str

class UserResponse(BaseModel):
    ...
class LoginRequest(BaseModel):
    name: str
    password: str

class UserRead(BaseModel):
    id: int
    name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


class SessionLoginResponse(BaseModel):
    user: UserRead