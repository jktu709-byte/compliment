from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from src.api.crud import ComplimentRepository
from src.api.service import ComplimentService
from src.core.database import get_session

def get_repo(session:AsyncSession = Depends(get_session))->ComplimentRepository:
        return ComplimentRepository(session)
                                    
def get_service(repo:ComplimentRepository = Depends(get_repo))->ComplimentService:
        return ComplimentService(repo)

