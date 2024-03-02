from pydantic_settings import BaseSettings, SettingsConfigDict

from ._constants import BASE_DIR


class Config(BaseSettings):
    BOT_TOKEN: str

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    model_config = SettingsConfigDict(env_file=BASE_DIR/'.env', env_file_encoding='utf-8', extra='ignore')


config = Config()
