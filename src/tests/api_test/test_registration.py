from src.schemas.auth import UserCreateSchema as ucs
from src.tests.factory.user_factory import User_Factory as uf


async def test_register(payload:ucs,test_data = uf.create_user):
    ...