import logging

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis
from aiogram_dialog import setup_dialogs
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.bot.config import Config, load_config, get_url
from app.bot.dialogs import start_dialog, one_rate_dialog, favorite_dialog
from app.bot.handlers import start
from app.bot.middlewares.MainMiddleware import MainMiddleware

logger = logging.getLogger(__name__)


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
        "[%(asctime)s] - %(name)s - %(message)s",
    )
    config: Config = load_config()
    logger.info("Конфиг загружен")
    engine = create_async_engine(get_url())
    sessionmaker = async_sessionmaker(engine)
    logger.info("Соединение с базой данных установлено")
    redis = Redis(host="localhost", decode_responses=True)
    storage = RedisStorage(
        redis=redis, key_builder=DefaultKeyBuilder(with_destiny=True)
    )
    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=storage)
    dp.include_router(start.router)
    dp.include_router(start_dialog)
    dp.include_router(one_rate_dialog)
    dp.include_router(favorite_dialog)
    logger.info("Роутеры подключены")
    dp.update.outer_middleware(MainMiddleware(sessionmaker))
    logger.info("Миддлвари подключены")
    setup_dialogs(dp)
    await dp.start_polling(bot)
