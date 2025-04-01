from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.database.models import UsersTable


async def update_currencies(user_id: int, rate: str, session: AsyncSession):
    statement = (
        update(UsersTable).where(UsersTable.user_id == user_id).values(currencies=rate)
    )
    async with session:
        await session.execute(statement)
        await session.commit()
