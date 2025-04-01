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
        async with session:
            check = True if await session.scalar(statement) is None else False
        return check
    return False


async def get_currencies(user_id: int, session: AsyncSession) -> list:  # noqa
    async with session:
        user = await session.get(UsersTable, user_id)
        if user:
            currencies: list = user.currencies  # noqa
            return currencies
        return []
