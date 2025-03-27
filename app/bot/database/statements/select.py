from aiogram.types import Message, CallbackQuery, ChatMemberUpdated
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.database.models import UsersTable


async def check_user(
    type_event: Message | CallbackQuery | ChatMemberUpdated,
    session: AsyncSession,
) -> bool:
    if type_event.from_user:
        statement = select(UsersTable).where(
            UsersTable.user_id == type_event.from_user.id
        )
        check = True if await session.scalar(statement) is None else False
        return check
    return False
