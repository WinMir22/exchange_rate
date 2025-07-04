from datetime import datetime
from typing import List

from sqlalchemy import func, BigInteger, ARRAY, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.services.exchange_rate_services.list_of_rates import rates


class Base(DeclarativeBase):
    pass


class UsersTable(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, nullable=False, unique=True
    )
    full_name: Mapped[str | None]
    username: Mapped[str | None]
    currencies: Mapped[list[str]] = mapped_column(
        ARRAY(String), server_default="{" + ",".join(rates) + "}"
    )
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
