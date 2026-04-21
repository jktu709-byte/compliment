from src.core.database import async_engine
from src.models.comp_models import Base
async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        async_engine.echo = True

async def reset_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        async_engine.echo = True       
# def __init__(self, session:AsyncSession) -> None:
#         self.session = session