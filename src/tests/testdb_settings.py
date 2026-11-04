from pydantic_settings import BaseSettings,SettingsConfigDict
from sqlalchemy import URL

class TESTDBSettings(BaseSettings):
    # Типизация
    POSTGRES_PASSWORD:str 
    POSTGRES_DB:str 
    POSTGRES_HOST:str
    POSTGRES_PORT:int
    POSTGRES_USER:str
    # Куда обращаться+как брать данные
    model_config = SettingsConfigDict(
        env_file="tests.env",
        extra="ignore",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
# DB_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    @property
    def test_db_url(self) -> URL:
        return URL.create(
            drivername="postgresql+asyncpg",
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            password=self.POSTGRES_PASSWORD,
            database=self.POSTGRES_DB,
            username=self.POSTGRES_USER
            )
# Продакшн
test_db_settings = TESTDBSettings() # type: ignore