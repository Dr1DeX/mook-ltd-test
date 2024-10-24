from pydantic import BaseModel


class MessageCreateSchema(BaseModel):
    sender_id: int
    text: str


class MessageHistoryResponseSchema(BaseModel):
    sender_id: int
    text: str

    class Config:
        from_attributes = True
