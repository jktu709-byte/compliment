from enum import Enum
from typing import Annotated, Optional, TypeAlias #noqa
from sqlalchemy import text,ForeignKey
from sqlalchemy.orm import DeclarativeBase,mapped_column,Mapped
from datetime import datetime

intpk: TypeAlias = Annotated[int,mapped_column(primary_key=True)]
created:TypeAlias = Annotated[datetime,
                              mapped_column(server_default=text("TIMEZONE('utc',now())"))]
class Base(DeclarativeBase):
    ...

#Насчет пола просто вьебу выпадающий список так будет проще
class Gender(Enum):
    male = "male"
    female = "female"
    neutral = "neutral"

class Compliment(Base):
    __tablename__ = "Compliments"
    id:Mapped[intpk]
    gender:Mapped[Gender|None]
    title:Mapped[str]
    meaning:Mapped[str]
    created_at:Mapped[created]
    
class History(Base):
    __tablename__ = "Recent Compliments"
    id:Mapped[intpk]
    compliment_id:Mapped[int] = mapped_column(
        ForeignKey("Compliments.id",ondelete="CASCADE")
    )
    user_gender:Mapped[Gender]
    created_at:Mapped[created]
    
#В планах добавить табличку Context, где будут обьяснятся примеры и контекст