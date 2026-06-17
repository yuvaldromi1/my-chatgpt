from pydantic import BaseModel


class MessageIn(BaseModel):
    """הודעה שנשלחת מהלקוח לשרת."""
    content: str


class MessageOut(BaseModel):
    """הודעה שמוחזרת מהשרת ללקוח."""
    role: str          # "user" או "assistant"
    content: str


class ConversationOut(BaseModel):
    """תשובה ביצירת שיחה חדשה."""
    conversationId: str
