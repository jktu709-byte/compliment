from fastapi import Depends #noqa
from src.api.repository import Repository
from src.core.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession


def get_repo(session:AsyncSession = Depends(get_session))->Repository:
        return Repository(session)
                                    
def get_service(repo:Repository = Depends(get_repo))->Service:
        return Service(repo)

