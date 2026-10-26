# Подготовка окружения прод бд
from sqlalchemy import URL
from pydantic_settings import BaseSettings, SettingsConfigDict

# Занимается сборкой url базы. Приводит, сверяет типы, подставляет значения, в общем заметно лучше, чем прошлый os.getenv
class DBSettings(BaseSettings):
    # Типизация
    POSTGRES_PASSWORD:str 
    POSTGRES_DB:str 
    POSTGRES_HOST:str
    POSTGRES_PORT:int
    POSTGRES_USER:str
    # Куда обращаться+как брать данные
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
# DB_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    @property
    def db_url(self) -> URL:
        return URL.create(
            drivername="postgresql+asyncpg",
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            password=self.POSTGRES_PASSWORD,
            database=self.POSTGRES_DB,
            username=self.POSTGRES_USER
            )
# Продакшн
db_settings = DBSettings() # type: ignore
# def check_env():
#     pass
    















