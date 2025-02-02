import os

from dotenv import load_dotenv

from src.settings.base import create_postgres_url, MyBaseSettings

load_dotenv()


class Postgres(MyBaseSettings):
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DATABASE: str = os.getenv("POSTGRES_DATABASE")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT"))
    POSTGRES_HOST: str = 'localhost'

    # class Config:
    #     env_prefix = 'POSTGRES_'

    @property
    def URL(self):
        return create_postgres_url(
            self.POSTGRES_USER, self.POSTGRES_PASSWORD, self.POSTGRES_HOST, self.POSTGRES_PORT, self.POSTGRES_DATABASE
        )


class Telegram(MyBaseSettings):
    BOT_TOKEN: str = os.getenv("BOT_TOKEN")

    # class Config:
    #     env_prefix = 'BOT_'


class Settings(MyBaseSettings):
    db: Postgres = Postgres()
    bot: Telegram = Telegram()


settings = Settings()
