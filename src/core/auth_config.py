from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class SecSettings(BaseSettings):
    # Крч это буквально упрощение жизни. Окружением заботится сам Pydantic и все отлично
    model_config = SettingsConfigDict(
        env_file=".env", 
        case_sensitive=False,
        extra="ignore",
        env_file_encoding = "utf-8",
        )
    app_name:str = "Auth" 
    database_url: str = Field(alias="DB_URL")
    jwt_secret_key: str = Field(alias="SECRET_KEY")
    jwt_secret_algo: str = "HS256"