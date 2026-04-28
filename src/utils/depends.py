from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from src.api.crud import ComplimentRepository
from src.api.service import ComplimentService
from src.core.database import get_session

async def get_repo(session:AsyncSession = Depends(get_session))->ComplimentRepository:
    return ComplimentRepository(session)

async def get_service(service:ComplimentRepository = Depends(get_repo))->ComplimentService:
    return ComplimentService(service)

