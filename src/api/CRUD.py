from src.models.models import Base
from src.core.database import async_engine
class Async():
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
            async_engine.echo = True
        
    @staticmethod
    async def insert_data():
        pass
    
    async def get_data(self):
        pass
    
    async def filter_data(self):
        pass
    
    async def change_data(self):
        pass
    
    async def delete_data(self):
        pass
    
    
            