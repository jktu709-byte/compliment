from enum import Enum
from typing import Annotated, Optional, TypeAlias #noqa
from sqlalchemy import String, text,ForeignKey,Enum as SEnum
from sqlalchemy.orm import DeclarativeBase,mapped_column,Mapped
from datetime import datetime

intpk: TypeAlias = Annotated[int,mapped_column(primary_key=True)]
created:TypeAlias = Annotated[datetime,
                              mapped_column(server_default=text("TIMEZONE('utc',now())"))]
class Base(DeclarativeBase):
    ...

#Насчет пола просто вьебу выпадающий список так будет проще
class Gender(str,Enum):
    male = "male"
    female = "female"
    neutral = "neutral"

class Compliment(Base):
    __tablename__ = "compliments"
    id:Mapped[intpk]
    gender:Mapped[Gender|None] =mapped_column(SEnum(Gender),nullable= True)
    title:Mapped[str] =mapped_column(String,nullable= True)
    meaning:Mapped[str] = mapped_column(String,nullable= True)
    created_at:Mapped[created] = mapped_column(String,nullable= True)
    history: Mapped[str] = mapped_column(String,nullable=True)
    
class History(Base):
    __tablename__ = "history"
    id:Mapped[intpk]
    compliment_id:Mapped[int] = mapped_column(
        ForeignKey("Compliments.id",ondelete="CASCADE")
    )
    user_gender:Mapped[Gender]
    created_at:Mapped[created]
    
#В планах добавить табличку Context, где будут обьяснятся примеры и контекст