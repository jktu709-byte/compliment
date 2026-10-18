# Подготовка окружения прод бд
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import URL

base_dir = Path(__file__).resolve().parent.parent.parent
env_file = base_dir / ".env"
    
if not env_file.exists():
    raise FileNotFoundError(f"Env file not found:{env_file}")
    
load_dotenv(env_file,override=True)
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST","localhost")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT","5432")) # type: ignore    
# DB_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
DB_URL = URL.create(
    drivername="postgresql+asyncpg",
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    password=POSTGRES_PASSWORD,
    database=POSTGRES_DB,
    username=POSTGRES_USER
    )

missing = []
if not POSTGRES_DB: 
    missing.append("POSTGRES_DB")
if not POSTGRES_HOST:
    missing.append("POSTGRES_HOST")
if not POSTGRES_PASSWORD:
    missing.append("POSTGRES_PASSWORD")
if not POSTGRES_PORT:
    missing.append("POSTGRES_PORT")
if not POSTGRES_USER:
    missing.append("POSTGRES_USER")
    
if missing:
    raise ValueError(f"Something's going wrong: {missing}")

print(f"DB connected: {POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")    
# def check_env():
#     pass
    















