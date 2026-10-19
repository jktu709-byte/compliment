# Подготовка окружения прод бд
from pathlib import Path
from sqlalchemy import URL
from pydantic_settings import BaseSettings, SettingsConfigDict
base_dir = Path(__file__).resolve().parent.parent.parent
env_file = base_dir / ".env"
    
if not env_file.exists():
    raise FileNotFoundError(f"Env file not found:{env_file}")
# Занимается сборкой url базы. Приводит, сверяет типы, подставляет значения, в общем заметно лучше, чем прошлый os.getenv
class DBSettings(BaseSettings):
    # Типизация
    DB_PASSWORD:str 
    DB_NAME:str 
    DB_HOST:str
    DB_PORT:int
    DB_USER:str
    # Куда обращаться+как брать данные
    model_config = SettingsConfigDict(
            env_file=".env", 
            case_sensitive=False,
            extra="ignore",
            env_file_encoding = "utf-8",
            ) 
# DB_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    @property
    def db_url(self) -> URL:
        return URL.create(
            drivername="postgresql+asyncpg",
            host=self.DB_HOST,
            port=self.DB_PORT,
            password=self.DB_PASSWORD,
            database=self.DB_NAME,
            username=self.DB_USER
            )
db_settings = DBSettings()            # type: ignore
# def check_env():
#     pass
    















