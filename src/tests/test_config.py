# Нужно будет вынести логику построения url бд в отдельный сервис. Смотреть на эти костяли больно.

import os
from pathlib import Path

from dotenv import load_dotenv

# Используй URL.connect, а не костыльное говно
from sqlalchemy import URL  #noqa

base_dir = Path(__file__).resolve().parent
env_file = base_dir / "tests.env"
    
if not env_file.exists():
    raise FileNotFoundError(f"Env file not found:{env_file}")
    
load_dotenv(env_file,override=True)
TEST_USER = os.getenv("TEST_USER")
TEST_PASSWORD = os.getenv("TEST_PASSWORD")
TEST_DB = os.getenv("TEST_DB")
TEST_HOST = os.getenv("TEST_HOST")
TEST_PORT = int(os.getenv("TEST_PORT")) # type: ignore
    
TEST_DB_URL = f"postgresql+asyncpg://{TEST_USER}:{TEST_PASSWORD}@{TEST_HOST}:{TEST_PORT}/{TEST_DB}"
    
    
print(f"DB connected: {TEST_HOST}:{TEST_PORT}/{TEST_DB}")