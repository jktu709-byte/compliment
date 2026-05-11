# Тут читаются настройки базы данных
import os 

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT",5432))
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_DB = os.getenv("POSTGRES_DB")

DB_URL = (
    f"postgresql+asyncpg://{POSTGRES_USER}:"
    f"{POSTGRES_PASSWORD}@{POSTGRES_HOST}:"
    f"{POSTGRES_PORT}/{POSTGRES_DB}"
)

print(f"DB connected: {POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")



# from dotenv import load_dotenv 
# import os
# from pathlib import Path

# BASE_DIR = Path(__file__).resolve().parent.parent.parent
# load_dotenv(BASE_DIR / "docker.env")
# POSTGRES_USER = os.getenv("POSTGRES_USER")
# POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
# POSTGRES_DB = os.getenv("POSTGRES_DB")
# POSTGRES_HOST = os.getenv("POSTGRES_HOST")
# POSTGRES_PORT = os.getenv("POSTGRES_PORT")






