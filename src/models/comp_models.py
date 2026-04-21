from enum import Enum
from typing import Annotated, List, Optional, TypeAlias #noqa
from sqlalchemy import VARCHAR, String, text,ForeignKey,Enum as SEnum
from sqlalchemy.orm import DeclarativeBase,mapped_column,Mapped,relationship
from datetime import datetime

intpk: TypeAlias = Annotated[int,mapped_column(primary_key=True)]
created:TypeAlias = Annotated[datetime,
                              mapped_column(server_default=text("TIMEZONE('utc',now())"))]
nullable_string = Annotated[String,mapped_column(nullable= True)]
class Base(DeclarativeBase):
    ...
#Насчет пола просто вьебу выпадающий список так будет проще
class Gender(str,Enum):
    male = "male"
    female = "female"
    neutral = "neutral"

class Compliments(Base):
    __tablename__ = "compliments"
    id:Mapped[intpk]
    gender:Mapped[Gender|None] =mapped_column(SEnum(Gender),nullable= True)
    title:Mapped[nullable_string] 
    point:Mapped[nullable_string] 
    created_at:Mapped[created] 
    # history:Mapped[String] = relationship("history.id",ondelete="CASCADE")
    
class History(Base):
    __tablename__ = "history"
    id:Mapped[intpk]
    
    compliment_id:Mapped[int] = mapped_column(ForeignKey("compliments.id",ondelete="CASCADE"))
    # прописать relationship
    compliments:Mapped[List["Compliments"]] = relationship(back_populates="Compliments.title")
    
    user_id:Mapped[int] = mapped_column(ForeignKey("user.id",ondelete="CASCASDE"))
    
    created_at:Mapped[created]

# Later I must setup a verification,authentificetion,autorization and etc.
class Users(Base):
    __tablename__ = "users"
    id: Mapped[intpk]
    name:Mapped[VARCHAR]
    user_history:Mapped[List["History"]] = relationship(back_populates="history.compliments")
    
#В планах добавить табличку Context, где будут обьяснятся примеры и контекст