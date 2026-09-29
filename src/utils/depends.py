from fastapi import Depends, HTTPException,Request,status #noqa
from src.api.repository import ComplimentRepository,UserRepository,AuthRepository
from src.api.service import ComplimentService,UserService,AuthService
from src.core.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.auth_config import auth_settings
import jwt
from src.auth.tokens import token_helper
from src.exceptions.semantic_exceptions import RefreshTokenNotFoundError, UserNotFoundError
from src.models.comp_models import User




def get_compl_repo(session:AsyncSession = Depends(get_session))-> ComplimentRepository:
        return ComplimentRepository(session)
                                    
def get_compl_service(repo:ComplimentRepository = Depends(get_compl_repo))->ComplimentService:
        return ComplimentService(repo) # type: ignore

def get_user_repo(session:AsyncSession = Depends(get_session))-> UserRepository:
        return UserRepository(session)
                                    
def get_user_service(repo:UserRepository = Depends(get_user_repo))->UserService:
        return UserService(repo)

def get_auth_repo(session:AsyncSession = Depends(get_session))-> AuthRepository:
        return AuthRepository(session)
                                    
def get_auth_service(repo:AuthRepository = Depends(get_user_repo))->AuthService:
        return AuthService(repo) #type:ignore

async def get_current_user_from_bearer(req:Request,user_repo:UserRepository) -> User:
        raw_token = _extract_token(req)
        try:
                payload = token_helper.decode_token(raw_token)
        except jwt.ExpiredSignatureError:
                raise HTTPException(status.HTTP_401_UNAUTHORIZED,detail="Token Expired")
        except jwt.InvalidTokenError:
                raise HTTPException(status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
        user_id = int(payload["sub"])
        user = await user_repo.get_user_by_id(user_id=user_id)
        if user is None:
                raise UserNotFoundError("Пользователь не найден")
        return user

def _extract_token(req:Request):
        header = req.headers.get("authorization")
        if header is None:
                raise RefreshTokenNotFoundError("Рефреш токен не найден")
        if header or header.lower().startswith("bearer "):
                return header.split("",1)[1].strip()
        cookies = req.cookies.get(auth_settings.access_cookie_name)
        if cookies:
                return cookies
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,detail="Missing acces token")