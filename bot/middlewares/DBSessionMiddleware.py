from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot.database.statements.insert import add_user
from bot.database.statements.select import check_user


class DbSessionMiddleware(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        super().__init__()
        self.session_pool = session_pool

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        if event.message:
            async with self.session_pool() as session:
                await add_user(
                    check=await check_user(
                        user_id=event.message.from_user.id,
                        event=event.message,
                        session=session,
                    ),
                    id=event.message.from_user.id,
                    full_name=event.message.from_user.full_name,
                    username=event.message.from_user.username,
                    session=session,
                )
                data["session"] = session
                return await handler(event, data)
        if event.callback_query:
            async with self.session_pool() as session:
                await add_user(
                    check=await check_user(
                        user_id=event.callback_query.from_user.id,
                        event=event,
                        session=session,
                    ),
                    id=event.callback_query.from_user.id,
                    full_name=event.callback_query.from_user.full_name,
                    username=event.callback_query.from_user.username,
                    session=self.session_pool,
                )
                data["session"] = session
                return await handler(event, data)
