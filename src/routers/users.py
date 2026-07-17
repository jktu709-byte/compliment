from fastapi import APIRouter, HTTPException, Depends
from src.api.service import ComplimentService
from src.schemas.comp_schemas import UserCreate
from src.utils.depends import get_service

user_router = APIRouter("/Users",tags=['Пользователи'])

@user_router.post("/register",status_code=201,summary="Регистрация пользователя")
async def register(payload:UserCreate,service: ComplimentService = Depends(get_service)):
    # try:
        # return await service
    ...