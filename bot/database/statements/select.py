from aiogram.types import TelegramObject
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import UsersTable


async def check_user(
    user_id: int, event: TelegramObject, session: AsyncSession
) -> bool:
    statement = select(UsersTable).where(
        UsersTable.user_id == event.from_user.id
        )
    check = True if await session.scalar(statement) is None else False
    return check
