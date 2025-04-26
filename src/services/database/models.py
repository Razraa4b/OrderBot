from sqlalchemy import Integer, BigInteger, Boolean, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(DeclarativeBase, AsyncAttrs):
    pass


class User(Base):
    __tablename__ = "Users"
    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger(), nullable=False)
    bot_settings: Mapped["UserBotSettings"] = relationship(back_populates="user") # type: ignore


class UserBotSettings(Base):
    __tablename__ = "UsersBotSettings"
    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("Users.id"))
    user: Mapped["User"] = relationship(back_populates="bot_settings", cascade="delete, delete-orphan", single_parent=True) # type: ignore
    is_enabled: Mapped[bool] = mapped_column(Boolean(), default=True)
