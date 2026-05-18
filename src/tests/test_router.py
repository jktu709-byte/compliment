from fastapi import APIRouter
from sqlalchemy import text 
from sqlalchemy.ext.asyncio import AsyncSession

test_router = APIRouter(prefix="/test")

@test_router.get("/connection")
def get_connection():
    pass

@test_router.get("/querry")
async def check_querry_conn(session:AsyncSession):
    res = await session.execute(text("SELECT 1"))
    assert res.scalar() == 1
    