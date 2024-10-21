from typing import Optional

from src.infrastructure.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Messages(Base):
    __tablename__ = 'Messages'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    text: Mapped[Optional[str]] = mapped_column(nullable=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey('UserProfile.id'), nullable=True)
    recipient_id: Mapped[int] = mapped_column(
        ForeignKey('UserProfile.id'), nullable=False
    )

    sender = relationship(
        'UserProfile', foreign_keys=[sender_id], back_populates='sent_messages'
    )
    recipient = relationship(
        'UserProfile', foreign_keys=[recipient_id], back_populates='received_messages'
    )
