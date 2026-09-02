from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthSettings(BaseSettings):
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
    access_token_expires_minutes: int = 15
    refresh_token_expires_minutes: int = 60 * 24 * 30
    access_cookie_name: str = "access_token"
    refresh_cookie_name: str = "refresh_token"
    # session_ttl_minutes: int = 60 * 24
    # session_extend_minutes: int = 60 * 24 * 7
    # session_rolling_interval_minutes: int = 10
    # session_absolute_timeout_days: int = 30
    # session_cookie_name: str = "session_id"
    # session_cookie_secure: bool = False
    # session_cookie_domain: str | None = None
auth_settings = AuthSettings()