from datetime import datetime

from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.comp_models import Compliment, Gender, History, RefreshToken, User


class Repository:
    def __init__(self,session:AsyncSession) -> None:
            self.session = session
class UserRepository(Repository):
    
    async def get_user_role(self,user_id:int):
        querry = await self.session.execute(select(User.role).where(User.id == user_id))
        return querry
    async def add_history(self,user_id:int): self.session.add(instance=History) #instance= куда добавить, конкретно что добавляем
    async def get_user_by_name(self,name:str)-> Result[tuple[User]]|None: return await self.session.execute(select(User).where(User.name == name))
    
    async def get_user_by_email(self,email:str) -> User|None: 
        res = await self.session.execute(select(User).where(User.email == email))
        return res.scalar_one_or_none()
    
    async def get_user_by_id(self,user_id:int)-> User|None: 
        return await self.session.get(User, user_id)
    
    async def create_user(self,u_name:str,u_email:str,u_gender:Gender,u_password_hash:str):
        user = User(name = u_name,u_email = u_email,gender = u_gender,password_hash = u_password_hash)
        self.session.add(user)
        await self.session.flush()
        return user
    
    async def get_all_users(self):
        return await self.session.execute(select(User))
        
    
    async def get_user_history(self,user_id:int)->list[History]:
        stmt = select(
            History
            ).options(selectinload(History.compliment)
                      ).filter(History.user_id == user_id
                               ).order_by(History.created_at.desc()
                                          ).limit(25) 
        res = await self.session.execute(stmt)
        return list(res.scalars().all())
    
    async def add_obj(self,obj):
         self.session.add(obj)
    
    async def refresh_obj(self,obj):
        await self.session.refresh(obj)    
    
    async def commit(self):
            await self.session.commit()
    
class ComplimentRepository(Repository):
    
    async def add_compliment(self, title:str, gender:Gender|None, point:str) -> Compliment:
        obj = Compliment(title=title,gender = gender,point = point,)
        self.session.add(obj)
        return obj
    
    async def add_list(self, compliments:list[Compliment]):
        res = self.session.add_all(compliments)
        await res # type: ignore
         
    async def get_compliment(self,complmnt_id:int)->Compliment|None:
        res = await self.session.execute(select(Compliment).filter(Compliment.id == complmnt_id))
        return res.scalar_one_or_none()
    
    async def get_all_compliments(self)->list[Compliment]:
        res = await self.session.execute(select(Compliment))
        # тут возвращается последовательность, поэтому ради типизации и чтобы линтер не ругался я просто воткну надстройку
        return list(res.scalars().all())
         
    async def delete_compliment(self,compliment_id:int)->bool:
        obj = await self.get_compliment(compliment_id)
        if not obj:
            return False
        await self.session.delete(obj)
        return True
    
    async def commit(self):
        await self.session.commit()
        
class AuthRepository(Repository):
    # добавлять токены в бд не надо, просто отправляй их клиенту, потом надо будет разбираться где их хранить - в локалке или же в куках
    async def create_refresh_token(self, user_id:int, token_hash: str, expires:datetime):
        refresh_token = RefreshToken(user_id = user_id,token_hash = token_hash,expires_at = expires)
        # крч await сдедует прописывать тогда, когда я обращаюсь к бд и получаю от нее какой либо ответ
        # например метод add() просто закидывает запись в очередь на запоминание и ему ответ, а то есть await не требуется
        self.session.add(refresh_token)
        # А вот flush() уже закидывает данные в базу и ему нужен await для получения ответа и налаживания контакта с базой
        await self.session.flush()
    
    async def get_refresh_token(self,token_hash):
        return await self.session.scalar(select(RefreshToken).where(RefreshToken.token_hash == token_hash))
    
    async def delete_refresh_token(self,token_obj:RefreshToken):
        return self.session.delete(token_obj)
    async def commit(self):
            await self.session.commit()