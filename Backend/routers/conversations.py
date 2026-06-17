from datetime import datetime, timezone

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, HTTPException

from db import conversations_collection, messages_collection
from models import ConversationOut, MessageIn, MessageOut
from openai_client import get_chat_response

router = APIRouter(prefix="/api/conversations", tags=["conversations"])


def _now():
    return datetime.now(timezone.utc)


def _parse_id(conversation_id: str) -> ObjectId:
    try:
        return ObjectId(conversation_id)
    except (InvalidId, TypeError):
        raise HTTPException(status_code=400, detail="Invalid conversation id")


@router.post("", response_model=ConversationOut)
async def create_conversation():
    """פותח שיחה חדשה ומחזיר את המזהה שלה."""
    result = await conversations_collection.insert_one(
        {"title": "New conversation", "createdAt": _now()}
    )
    return {"conversationId": str(result.inserted_id)}


@router.post("/{conversation_id}/messages", response_model=MessageOut)
async def add_message(conversation_id: str, message: MessageIn):
    """
    שומר את הודעת המשתמש, שולח את כל ההיסטוריה ל-OpenAI,
    שומר את תשובת הצ'אט ומחזיר אותה.
    """
    oid = _parse_id(conversation_id)

    conversation = await conversations_collection.find_one({"_id": oid})
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # 1) שמירת הודעת המשתמש
    await messages_collection.insert_one(
        {
            "conversationId": oid,
            "role": "user",
            "content": message.content,
            "createdAt": _now(),
        }
    )

    # 2) שליפת כל ההיסטוריה לפי סדר כרונולוגי (שמירת ההקשר)
    history_docs = (
        await messages_collection.find({"conversationId": oid})
        .sort("createdAt", 1)
        .to_list(length=None)
    )
    history = [{"role": d["role"], "content": d["content"]} for d in history_docs]

    # 3) קריאה ל-OpenAI מצד השרת
    try:
        assistant_content = get_chat_response(history)
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"OpenAI request failed: {exc}",
        )

    # 4) שמירת תשובת הצ'אט
    await messages_collection.insert_one(
        {
            "conversationId": oid,
            "role": "assistant",
            "content": assistant_content,
            "createdAt": _now(),
        }
    )

    return {"role": "assistant", "content": assistant_content}


@router.get("/{conversation_id}/messages", response_model=list[MessageOut])
async def get_messages(conversation_id: str):
    """שליפת היסטוריית שיחה (אופציונלי)."""
    oid = _parse_id(conversation_id)
    history_docs = (
        await messages_collection.find({"conversationId": oid})
        .sort("createdAt", 1)
        .to_list(length=None)
    )
    return [{"role": d["role"], "content": d["content"]} for d in history_docs]
