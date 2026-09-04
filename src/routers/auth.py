from fastapi import APIRouter, Depends, HTTPException, Response, status

from src.api.service import AuthService
from src.core.auth_config import auth_settings
from src.exceptions.semantic_exceptions import (
    AppError,
    InvalidCredentialsError,
    RefreshTokenExpiredError,
    RefreshTokenNotFoundError,
    UserNotFoundError,
)
from src.schemas.auth import LoginRequest, RefreshRequest, TokenPair
from src.utils.depends import get_service

auth_router = APIRouter(prefix="/auth",tags=["Auth"])

def _set_cookies_settings(response:Response,acces_token:str,refresh_token:str):
    response.set_cookie(
        key= auth_settings.access_cookie_name,
        value= acces_token,
        # если поставить True - получишь защиту от xss
        httponly=False,
        secure=auth_settings.session_cookie_secure,
        samesite= "lax",
        max_age= auth_settings.access_token_expires_minutes * 15,
        path="/"
    )
    response.set_cookie(
            key= auth_settings.refresh_cookie_name,
            value= refresh_token,
            # если поставить True - получишь защиту от xss
            httponly=False,
            secure=auth_settings.session_cookie_secure,
            samesite= "lax",
            max_age= auth_settings.refresh_token_expires_minutes * 15,
            path="/"
        )
    
@auth_router.get("/login/jwt",summary= "Вход JWT")
async def login(data:LoginRequest,response:Response,service:AuthService = Depends(get_service)) -> TokenPair:
    try:
        # вводим данные 
        acces,refresh = await service.login(data.name,data.password)
    # при неверном вводе пароля или логина выкидываем ошибку
    except InvalidCredentialsError() as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,detail=str(e)) from e
    # ловим любую другую ошибку(надо будет сделать более детальные ошибки)
    except AppError() as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,detail= str(e)) from e
    _set_cookies_settings(response,acces,refresh)
    return TokenPair(access_token=acces,refresh_token=refresh)
        
@auth_router.get("/tokens/refresh")
async def refresh_token(data:RefreshRequest,response:Response,service:AuthService = Depends(get_service)) -> TokenPair:
    try:
        pair = await service.refresh_token(data.refresh_token)
    except RefreshTokenExpiredError as err:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,detail=str(err)) from err
    except RefreshTokenNotFoundError as err:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,detail= str(err)) from err
    except UserNotFoundError as err:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,detail= str(err)) from err
    except AppError as err: 
        raise HTTPException(status.HTTP_400_BAD_REQUEST,detail= str(err)) from err
    # настраиваем куки перед отправкой данных
    _set_cookies_settings(acces_token=pair.acces,refresh_token=pair.refresh)
    return pair

# @auth_router.get("/me")
# async def get_me():
#     res = get_user_from_bearer()
#     return res