from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.lexicon.lexicon_ru import lexicon

router = Router()
logger = logging.getLogger(__name__)

@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer(lexicon["start_command"])
