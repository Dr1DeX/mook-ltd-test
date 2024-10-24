from datetime import datetime
from typing import Optional

from sqlalchemy import (
    ForeignKey,
    func,
    TIMESTAMP,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from src.infrastructure.database import Base


class Messages(Base):
    __tablename__ = 'Messages'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    text: Mapped[Optional[str]] = mapped_column(nullable=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey('UserProfile.id'), nullable=False)

    sender = relationship(
        'UserProfile',
        foreign_keys=[sender_id],
        back_populates='sent_messages',
    )
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())


class UserProfile(Base):
    __tablename__ = 'UserProfile'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    username: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)

    sent_messages = relationship(
        'Messages',
        foreign_keys=[Messages.sender_id],
        back_populates='sender',
    )
