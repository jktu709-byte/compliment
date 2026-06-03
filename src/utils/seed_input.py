import asyncio #NOQA
from src.core.database import async_session
from src.models.comp_models import Compliment
from seed_data import compliments

async def seed():
    async with async_session() as session:
        try:
            res = [Compliment(**item) for item in compliments]
            session.add_all(res)
            await session.commit()
            print(f"Добавлено {len(res)} комплиментов")
        except Exception as e:
            print(f"Somethings gone wrong {e.__class__}")

# if __name__ == "__main__":
#     asyncio.run(seed())