from enum import Enum
from typing import Annotated, List, Optional, TypeAlias #noqa
from sqlalchemy import DateTime, Integer, String, text,ForeignKey,Enum as SEnum #noqa
from sqlalchemy.orm import DeclarativeBase,mapped_column,Mapped,relationship #noqa
from datetime import datetime
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
    name:Mapped[str] = mapped_column(nullable=False)
    gender:Mapped[Gender] = mapped_column(nullable=False)
    role:Mapped[Role] = mapped_column(nullable=False)
    password_hash:Mapped[str] = mapped_column(nullable=False)
    user_history:Mapped[List["History"]] = relationship("History",back_populates="user")
class History(BDBase):
    __tablename__ = "history"
    id:Mapped[int] = mapped_column(primary_key=True)
    compliment_id:Mapped[int] = mapped_column(ForeignKey("compliments.id",ondelete="CASCADE"))
    compliment:Mapped["Compliment"] = relationship("Compliment",back_populates="history")
    user_id:Mapped[int] = mapped_column(ForeignKey("users.id",ondelete="CASCADE"))
    user:Mapped["User"] = relationship("User",back_populates="user_history")
    created_at:Mapped[datetime] = mapped_column(DateTime,server_default=text("TIMEZONE('utc',now())"))

# Later I must setup a verification,authentificetion,autorization and etc.

#В планах добавить табличку Context, где будут обьяснятся примеры и контекст
