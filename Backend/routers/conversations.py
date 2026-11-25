from datetime import UTC, datetime

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, HTTPException

from db import conversations_collection, messages_collection
from models import ConversationOut, MessageIn, MessageOut
from openai_client import get_chat_response

router = APIRouter(prefix="/api/conversations", tags=["conversations"])


def _now():
    return datetime.now(UTC)


def _parse_id(conversation_id: str) -> ObjectId:
    try:
        return ObjectId(conversation_id)
    except (InvalidId, TypeError):
        raise HTTPException(status_code=400, detail="Invalid conversation id") from None


@router.post("", response_model=ConversationOut)
async def create_conversation():
    result = await conversations_collection.insert_one(
        {"title": "New conversation", "createdAt": _now()}
    )
    return {"conversationId": str(result.inserted_id)}


@router.post("/{conversation_id}/messages", response_model=MessageOut)
async def add_message(conversation_id: str, message: MessageIn):
    oid = _parse_id(conversation_id)

    conversation = await conversations_collection.find_one({"_id": oid})
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # 1)
    await messages_collection.insert_one(
        {
            "conversationId": oid,
            "role": "user",
            "content": message.content,
            "createdAt": _now(),
        }
    )

    # 2)
    history_docs = (
        await messages_collection.find({"conversationId": oid})
        .sort("createdAt", 1)
        .to_list(length=None)
    )
    history = [{"role": d["role"], "content": d["content"]} for d in history_docs]

    # 3)
    try:
        assistant_content = get_chat_response(history)
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"OpenAI request failed: {exc}",
        ) from exc

    # 4)
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
    oid = _parse_id(conversation_id)

    conversation = await conversations_collection.find_one({"_id": oid})
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    history_docs = (
        await messages_collection.find({"conversationId": oid})
        .sort("createdAt", 1)
        .to_list(length=None)
    )
    return [{"role": d["role"], "content": d["content"]} for d in history_docs]
