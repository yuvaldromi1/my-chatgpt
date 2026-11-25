from pydantic import BaseModel


class MessageIn(BaseModel):
    content: str


class MessageOut(BaseModel):
    role: str
    content: str


class ConversationOut(BaseModel):
    conversationId: str
