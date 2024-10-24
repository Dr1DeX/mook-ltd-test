from dataclasses import dataclass

from src.dispatcher.chat.repository import ChatRepository
from src.dispatcher.chat.schema import (
    MessageCreateSchema,
    MessageHistoryResponseSchema,
)


@dataclass
class ChatService:
    chat_repository: ChatRepository

    async def save_message(
        self,
        body: MessageCreateSchema,
    ) -> MessageHistoryResponseSchema:
        new_message = await self.chat_repository.save_message(body=body)
        new_message_schema = MessageHistoryResponseSchema(
            sender_id=body.sender_id,
            text=new_message.text,
        )
        return new_message_schema

    async def get_all_message(self) -> list[MessageHistoryResponseSchema]:
        messages = await self.chat_repository.get_all_messages()
        messages_schema = [
            MessageHistoryResponseSchema.model_validate(message) for message in messages
        ]
        return messages_schema
