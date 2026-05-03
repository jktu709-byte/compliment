raise RuntimeError("LOADED THIS FILE")
from enum import Enum
from typing import Annotated, List, Optional, TypeAlias #noqa
from sqlalchemy import DateTime, Integer, String, text,ForeignKey,Enum as SEnum
from sqlalchemy.orm import DeclarativeBase,mapped_column,Mapped,relationship #noqa
from datetime import datetime
# def pk():
#     return mapped_column(Integer,primary_key=True)
# def title_str():
#     return mapped_column(String,nullable=False)
# def created():
#     return mapped_column(datetime,server_default=text("TIMEZONE('utc',now())"))
# intpk: TypeAlias = Annotated[int,mapped_column(Integer,primary_key=True)]
# created:TypeAlias = Annotated[datetime,mapped_column(server_default=text("TIMEZONE('utc',now())"))]
# str_512 = Annotated[str,mapped_column(String(512))]
class Base(DeclarativeBase):
    pass
#Насчет пола просто вьебу выпадающий список так будет проще
class Gender(str,Enum):
    male = "male"
    female = "female"
    neutral = "neutral"
# 
class Compliment(Base):
    __tablename__ = "compliments"
    id:Mapped[int] = mapped_column(primary_key=True)
    gender:Mapped[Gender|None] =mapped_column(Enum(Gender),nullable= True)
    # title:Mapped[str] = mapped_column(nullable= False)
    # point:Mapped[str|None] = mapped_column(nullable= True)
    created_at:Mapped[datetime] = mapped_column(DateTime,server_default=text("TIMEZONE('utc',now())")) 
    history:Mapped[list["History"]] = relationship(back_populates="compliment")
    
class History(Base):
    __tablename__ = "history"
    id:Mapped[int] = mapped_column(primary_key=True)
    compliment_id:Mapped[int] = mapped_column(ForeignKey("compliments.id",ondelete="CASCADE"))
    # прописать relationship
    compliment:Mapped["Compliment"] = relationship(back_populates="history")
    user_id:Mapped[int] = mapped_column(ForeignKey("user.id",ondelete="CASCADE"))
    created_at:Mapped[datetime] = mapped_column(DateTime,server_default=text("TIMEZONE('utc',now())"))

# Later I must setup a verification,authentificetion,autorization and etc.
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    # name:Mapped[str] = mapped_column(nullable=False)
    user_history:Mapped[List["History"]] # = relationship(back_populates="history.compliments")
    
#В планах добавить табличку Context, где будут обьяснятся примеры и контекст
# type_annotation_map = {
    #     intpk: Integer,
    #     created:datetime,
    #     title_string:String,
    #     nullable_string:String,
    # }