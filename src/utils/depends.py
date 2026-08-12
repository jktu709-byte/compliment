from fastapi import Depends #noqa
from src.api.repository import ComplimentRepository,UserRepository,AuthRepository
from src.api.service import ComplimentService,UserService,AuthService
from src.core.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession


def get_compl_repo(session:AsyncSession = Depends(get_session))-> ComplimentRepository:
        return ComplimentRepository(session)
                                    
def get_compl_service(repo:ComplimentRepository = Depends(get_compl_repo))->ComplimentService:
        return ComplimentService(repo)


def get_user_repo(session:AsyncSession = Depends(get_session))-> UserRepository:
        return UserRepository(session)
                                    
def get_user_service(repo:ComplimentRepository = Depends(get_user_repo))->UserService:
        return UserService(repo)

def get_auth_repo(session:AsyncSession = Depends(get_session))-> AuthRepository:
        return AuthRepository(session)
                                    
def get_auth_service(repo:ComplimentRepository = Depends(get_user_repo))->AuthService:
        return AuthService(repo)
