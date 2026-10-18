# Подготовка окружения прод бд
from pathlib import Path
from sqlalchemy import URL
from pydantic_settings import BaseSettings, SettingsConfigDict
base_dir = Path(__file__).resolve().parent.parent.parent
env_file = base_dir / ".env"
    
if not env_file.exists():
    raise FileNotFoundError(f"Env file not found:{env_file}")
class DBSettings(BaseSettings):
    # Крч это буквально упрощение жизни. Окружением заботится сам Pydantic и все отлично
    model_config = SettingsConfigDict(
        env_file=".env", 
        case_sensitive=False,
        extra="ignore",
        env_file_encoding = "utf-8",
        )    
    POSTGRES_USER:str = "POSTGRES_USER"
    POSTGRES_PASSWORD:str = "POSTGRES_PASSWORD"
    POSTGRES_DB:str = "POSTGRES_DB"
    POSTGRES_HOST:str = "POSTGRES_HOST"
    POSTGRES_PORT:int = "POSTGRES_PORT","5432" # type: ignore
   
# DB_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    DB_URL = URL.create(
        drivername="postgresql+asyncpg",
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        password=POSTGRES_PASSWORD,
        database=POSTGRES_DB,
        username=POSTGRES_USER
        )
db_settings = DBSettings()
missing = []
if not db_settings.POSTGRES_DB: 
    missing.append("POSTGRES_DB")
if not db_settings.POSTGRES_HOST:
    missing.append("POSTGRES_HOST")
if not db_settings.POSTGRES_PASSWORD:
    missing.append("POSTGRES_PASSWORD")
if not db_settings.POSTGRES_PORT:
    missing.append("POSTGRES_PORT")
if not db_settings.POSTGRES_USER:
    missing.append("POSTGRES_USER")
    
if missing:
    raise ValueError(f"Something's going wrong: {missing}")

print(f"DB connected: {db_settings.POSTGRES_HOST}:{db_settings.POSTGRES_PORT}/{db_settings.POSTGRES_DB}")    
# def check_env():
#     pass
    















