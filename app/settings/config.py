from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    # JWT
    SECRET_KEY: str = Field(None, env="SECRET_KEY")
    ALGORITHM: str = Field(None, env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(None, env="ACCESS_TOKEN_EXPIRE_MINUTES")

    class Config:
        env_file = ".env"
        extra = "ignore"


def get_config() -> Config:
    return Config()
