from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from src.dispatcher.messages.models import Messages
from src.infrastructure.database import Base


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
    received_messages = relationship(
        'Messages',
        foreign_keys=Messages.recipient_id,
        back_populates='recipient',
    )
