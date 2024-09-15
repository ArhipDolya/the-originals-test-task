from pydantic_settings import BaseSettings


class Config(BaseSettings):
    ...


def get_config() -> Config:
    return Config()
