from src.models.models import Base
from src.core.database import async_engine,async_session
class ComplimentCRUD():
    def __init__(self, session:async_session) -> None:
        self.session = async_session
        
    async def create_tables(self):
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
            async_engine.echo = True
    # Хотел написать перезапуск базы но по итогу решил запустить это в контейнере
    # @staticmethod
    # async def wait_db():
    #         pass
    async def insert_data(self):
        pass
    
    async def get_data(self):
        pass
    
    async def filter_data(self):
        pass
    
    async def change_data(self):
        pass
    
    async def delete_data(self):
        pass
    
    
            