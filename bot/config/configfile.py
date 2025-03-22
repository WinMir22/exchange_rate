from dataclasses import dataclass
from environs import Env


@dataclass
class DatabaseConfig:
    database: str
    db_host: str
    db_user: str
    db_password: str
    db_port: str


@dataclass
class TgBot:
    token: str
    winner_id: int
    dima_id: int


@dataclass
class Config:
    tg_bot: TgBot
    db: DatabaseConfig


def load_config(path: str | None = None) -> Config:

    env: Env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
            winner_id=int(env('WINNER_ID')),
            dima_id=int(env('DIMA_ID'))
        ),
        db=DatabaseConfig(
            database=env('DATABASE'),
            db_host=env('DB_HOST'),
            db_user=env('DB_USER'),
            db_password=env('DB_PASSWORD'),
            db_port=env('DB_PORT')
        )
    )


def get_url(path: str | None = None) -> str:
    config = load_config(path=path)
    user = config.db.db_user
    password = config.db.db_password
    host = config.db.db_host
    port = config.db.db_port
    name = config.db.database
    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}"
