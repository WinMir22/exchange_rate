import asyncio
import logging

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.bot.config.configfile import Config, load_config, get_url
from app.bot.handlers import user_handlers
from app.bot.middlewares.DBSessionMiddleware import DBSessionMiddleware

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
    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp.include_router(user_handlers.router)
    # dp.include_router(admin_handlers.router)
    # dp.include_router(other_handlers.router)
    logger.info("Роутеры подключены")
    dp.update.outer_middleware(DBSessionMiddleware(sessionmaker))
    logger.info("Миддлвари подключены")
    await dp.start_polling(bot)
