import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.comp_schemas import ComplimentAppendDTO
from src.tests.factory.complmnt_factory import Complmnt_Factory


@pytest.fixture
# в pytest все устроено так, что не нужно прописывать тип объекта. 
# Достаточно указать нужную ранее определенную фикстуру и pytest найдет ее сам в своем хранилище фикстур
# проще говоря - дай мне фикстуру с именем test_session и засунь ее внутрь последующего объекта
def complmnt_factory(test_session:AsyncSession) -> Complmnt_Factory:
    return Complmnt_Factory(test_session)
    
@pytest.mark.asyncio 
async def test_add_data(factory:Complmnt_Factory):
    complmnt = ComplimentAppendDTO
    res = await factory.create_complmnt()
    assert  complmnt.title == res.title
    assert complmnt.gender == res.gender
    assert complmnt.point == res.point
    return res