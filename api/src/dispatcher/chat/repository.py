from dataclasses import dataclass
from typing import List

from sqlalchemy import (
    insert,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.dispatcher.chat.schema import MessageCreateSchema
from src.dispatcher.models import Messages


@dataclass
class ChatRepository:
    db_session: AsyncSession

    async def save_message(self, body: MessageCreateSchema) -> MessageCreateSchema:
        query = insert(Messages).values(**body.dict(exclude_none=True))

        async with self.db_session as session:
            await session.execute(query)
            await session.commit()
        return body

    async def get_all_messages(self) -> List[Messages]:
        query = select(Messages).options(
            joinedload(Messages.sender),
        )

        async with self.db_session as session:
            result = (await session.execute(query)).scalars().all()
            return result
