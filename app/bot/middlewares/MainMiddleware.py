from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.bot.database.db_class import DatabaseCRUD


class MainMiddleware(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        super().__init__()
        self.session_pool = session_pool

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        user = event.from_user
        data["user_id"] = user.id
        data["full_name"] = user.full_name

        async with self.session_pool() as session:
            database_crud = DatabaseCRUD(session)
            await database_crud.add_user(
                check=await database_crud.check_user(
                    event=event,
                ),
                user_id=user.id,
                full_name=user.full_name,
                username=user.username,
            )
            data["database_crud"] = database_crud
            return await handler(event, data)
