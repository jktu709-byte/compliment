import pytest

from src.api.service import ComplimentService
from src.tests.factory.complmnt import Complmnt_Factory
from src.tests.factory.DB import get_test_session


@pytest.mark.asyncio 
async def test_add_data(factory:Complmnt_Factory):
    ...