from urllib.parse import quote

from pydantic_settings import BaseSettings, SettingsConfigDict


class CelerySettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_HOST: str = "rabbitmq"
    RABBITMQ_PORT: int = 5672

    @property
    def broker_url(self) -> str:
        user = quote(self.RABBITMQ_USER, safe="")
        password = quote(self.RABBITMQ_PASSWORD, safe="")
        return f"amqp://{user}:{password}@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}//"


celery_settings = CelerySettings()  # type: ignore[call-arg]
