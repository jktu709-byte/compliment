from fastapi import APIRouter,Depends, HTTPException,status #noqa
from src.user.service import UserService
from src.schemas.auth_schemas import UserCreateSchema
from src.utils.depends import get_service  #type:ignore
from src.exceptions.semantic_exceptions import UserAlreadyExistsError,AppError
user_router = APIRouter("/users",tags=['Пользователи']) # type: ignore

@user_router.post("/register",status_code=201,summary="Регистрация пользователя")
async def register(payload:UserCreateSchema,service: UserService = Depends(get_service)):
    try:
        return await service.register(name=payload.name,email=payload.email,gender=payload.gender,password=payload.password)    
    except UserAlreadyExistsError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,detail="User already exist") from e
    except AppError as e:
        detail = str(e) or "Bad request"
        raise HTTPException(status.HTTP_400_BAD_REQUEST,detail=detail) from e
    
    