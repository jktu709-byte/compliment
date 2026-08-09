from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, DateTime, ForeignKey, String, func, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class BDBase(DeclarativeBase):
    pass
#Насчет пола просто вьебу выпадающий список так будет проще
class Gender(str,Enum):
    male = "male"
    female = "female"
    neutral = "neutral"

class Role(str,Enum):
    user = "user"
    admin = "admin"
    moderation = "moderation"

class Status(str, Enum):
    ACTIVE = "ACTIVE"
    BANNED = "BANNED"

class Compliment(BDBase):
    __tablename__ = "compliments"
    id:Mapped[int] = mapped_column(primary_key=True)
    gender:Mapped[Gender] =mapped_column(nullable= False)
    title:Mapped[str] = mapped_column(nullable= False)
    point:Mapped[str|None] = mapped_column(nullable= True)
    # category:Mapped[str|None] = mapped_column()
    created_at:Mapped[datetime] = mapped_column(DateTime,server_default=text("TIMEZONE('utc',now())")) 
    history:Mapped[list["History"]] = relationship("History",back_populates="compliment")
class User(BDBase):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(nullable=False,unique=True,index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    email:...
    gender:Mapped[Gender] = mapped_column(nullable=False,index=True)
    status:Mapped[Status]= mapped_column(nullable=True)
    role:Mapped[Role] = mapped_column(nullable=False)
    password_hash:Mapped[str] = mapped_column(String(255),unique=True,nullable=False,)
    user_history:Mapped[list["History"]] = relationship("History",back_populates="user")
    refresh_tokens:Mapped[list["RefreshToken"]] = relationship("RefreshToken",back_populates="user",cascade="all, delete-orphan")
class History(BDBase):
    __tablename__ = "history"
    id:Mapped[int] = mapped_column(primary_key=True)
    compliment_id:Mapped[int] = mapped_column(ForeignKey("compliments.id",ondelete="CASCADE"))
    compliment:Mapped["Compliment"] = relationship("Compliment",back_populates="history")
    user_id:Mapped[int] = mapped_column(ForeignKey("users.id",ondelete="CASCADE"))
    user:Mapped["User"] = relationship("User",back_populates="user_history")
    created_at:Mapped[datetime] = mapped_column(DateTime,server_default=text("TIMEZONE('utc',now())"))

# Later I must setup a verification,authentificetion,autorization and etc.
class RefreshToken(BDBase):
    id:Mapped[int] = mapped_column(primary_key=True)
    user_id:Mapped[int] = mapped_column(ForeignKey("users.id"),index=True)
    token_hash:Mapped[str] = mapped_column(String(128),unique=True)
    expires_at:Mapped[datetime] = mapped_column(DateTime(timezone=True),index=True)
    revoked:Mapped[bool] = mapped_column(Boolean,default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    user: Mapped[User] = relationship(back_populates="refresh_tokens")    
#В планах добавить табличку Context, где будут обьяснятся примеры и контекст
