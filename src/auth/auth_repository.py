from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.comp_models import RefreshToken


class AuthRepository:
    def __init__(self,session:AsyncSession) -> None:
                self.session = session
    # добавлять токены в бд не надо, просто отправляй их клиенту, потом надо будет разбираться где их хранить - в локалке или же в куках
    async def create_refresh_token(self, user_id:int, token_hash: str, expires:datetime):
        refresh_token = RefreshToken(
            user_id = user_id,
            token_hash = token_hash,
            expires_at = expires
        )
        # крч await сдедует прописывать тогда, когда я обращаюсь к бд и получаю от нее какой либо ответ
        # например метод add() закидывает запись в очередь на запоминание и ему ответ не требуется
        self.session.add(refresh_token)
        # А вот flush() уже закидывает данные в базу и ему нужен await для получения ответа и контакта с бд
        await self.session.flush()
    
    async def get_refresh_token(self,token_hash):
        return await self.session.scalar(
            select(RefreshToken)
            .where(RefreshToken.token_hash == token_hash))
    
    async def delete_refresh_token(self,token_obj:RefreshToken):
        return self.session.delete(token_obj)
    
    async def commit(self):
            await self.session.commit()