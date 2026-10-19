import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import URL

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
    
TEST_URL = URL.create(
    drivername="postgresql+asyncpg",
    password=TEST_PASSWORD,
    port=TEST_PORT,
    username=TEST_USER,
    database=TEST_DB,
    host=TEST_HOST
) 

print(f"DB connected: {TEST_HOST}:{TEST_PORT}/{TEST_DB}")