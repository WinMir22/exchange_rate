import logging
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.database.models import UsersTable


logger = logging.getLogger(__name__)


async def add_user(
    check: bool, id: int, full_name: str, username: str, session: AsyncSession
) -> None:
    if check:
        add_user_statement = UsersTable(
            user_id=id, full_name=full_name, username=username
        )
        async with session:
            session.add(add_user_statement)
            logger.info(f"Добавил в бд {full_name}" f"({id})")
            await session.commit()
            return
    return
