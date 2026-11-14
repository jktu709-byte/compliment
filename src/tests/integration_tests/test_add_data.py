import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.comp_models import Gender
from src.tests.factory.complmnt_factory import Complmnt_Factory


@pytest.fixture
def complmnt_factory(test_session:AsyncSession) -> Complmnt_Factory:
    return Complmnt_Factory(test_session)
    
@pytest.mark.asyncio 
async def test_add_data(complmnt_factory):
    res = await complmnt_factory.create_complmnt()
    assert  res.title == "test_title"
    assert res.gender == Gender.neutral
    assert res.point == "test_point"
    return res