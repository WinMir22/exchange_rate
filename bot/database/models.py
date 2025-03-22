from datetime import datetime
from sqlalchemy import func, BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class UsersTable(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, nullable=False, unique=True
    )
    full_name: Mapped[str | None]
    username: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=datetime.now()
    )
