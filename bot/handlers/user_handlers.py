import logging
from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from bot.lexicon.lexicon_ru import lexicon

router = Router()
logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def start_command(message: Message):
    name, user_id = message.from_user.full_name, message.from_user.id
    await message.answer(lexicon["start_command"])
    logger.info(f"Пользователь {name}({user_id}) запустил бота")


@router.message(Command("help"))
async def help_command(message: Message):
    name, user_id = message.from_user.full_name, message.from_user.id
    await message.answer(lexicon["help_command"])
    logger.info(f"Пользователь {name}({user_id}) вызвал команду хелп")
