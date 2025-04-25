import logging

from typing import cast, List

from aiogram.types import CallbackQuery, Message
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.database.models import UsersTable

logger = logging.getLogger(__name__)


class DatabaseCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def check_user(
        self,
        event: Message | CallbackQuery,
    ) -> bool:
        """Check if a user exists in the 'users' table based on Telegram event.

        :param event: Aiogram event (Message or CallbackQuery)
        :return: True if user not in db, else False
        """
        if event.from_user:
            statement = select(UsersTable).where(
                UsersTable.user_id == event.from_user.id
            )
            check = True if await self.session.scalar(statement) is None else False
            return check
        return False

    async def get_currencies(self, user_id: int) -> list:
        """Get exchange_rate list (rates order)

        :param user_id: telegram user id
        :return: list of rates order
        """
        user = await self.session.get(UsersTable, user_id)
        if user:
            return cast(List[str], user.currencies)
        return []

    async def add_user(
        self,
        check: bool,
        user_id: int,
        full_name: str,
        username: str,
    ) -> None:
        """Add user to database

        :param check: True or False, function check_user result
        :param user_id: telegram user_id
        :param full_name: telegram user full name
        :param username: telegram username
        :return: None
        """
        if check:
            add_user_statement = UsersTable(
                user_id=user_id, full_name=full_name, username=username
            )
            self.session.add(add_user_statement)
            logger.info(f"Добавил в бд {full_name}" f"({user_id})")
            await self.session.commit()

    async def update_currencies(self, user_id: int, rate: list) -> None:
        """Change rates order in database, users table

        :param user_id: telegram user id
        :param rate: rates list to update
        :return:
        """
        statement = (
            update(UsersTable)
            .where(UsersTable.user_id == user_id)
            .values(currencies=rate)
        )
        await self.session.execute(statement)
        await self.session.commit()
