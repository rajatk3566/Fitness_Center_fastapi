from pydantic_settings import BaseSettings
from datetime import timedelta


class Settings(BaseSettings):
    PROJECT_NAME: str = "Fitness Center API"
    API_V1_STR: str = "/api/v1"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    def get_access_token_expiry(self) -> timedelta:
        return timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)

    @property
    def DATABASE_URL(self) -> str:
        return "mysql://root:consultadd@localhost:3306/test"

    class Config:
        from_attributes = True


settings = Settings()
