from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class MyBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        extra='ignore',
        env_file_encoding='utf-8',
        case_sensitive=False,
    )

def create_postgres_url(username, password, host, port, database) -> str:
    return str(PostgresDsn.build(
        scheme="postgresql",
        username=username,
        password=password,
        host=host,
        port=port,
        path=database,
    ))
