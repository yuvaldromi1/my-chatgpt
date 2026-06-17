"""Insert sample conversation data for Database export (submission)."""
from datetime import datetime, timezone

from bson import ObjectId
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
client = MongoClient(MONGO_URI)
db = client["chatgpt_db"]

conversations = db["conversations"]
messages = db["messages"]

# Clear existing sample data for a clean export
conversations.delete_many({})
messages.delete_many({})

now = datetime.now(timezone.utc)
conv_id = ObjectId()

conversations.insert_one(
    {
        "_id": conv_id,
        "title": "New conversation",
        "createdAt": now,
    }
)

sample_messages = [
    {"role": "user", "content": "שלום! מי אתה?", "offset_sec": 0},
    {
        "role": "assistant",
        "content": "שלום! אני עוזר וירטואלי. איך אוכל לעזור לך היום?",
        "offset_sec": 2,
    },
    {"role": "user", "content": "מה זה פרויקט Full Stack?", "offset_sec": 5},
    {
        "role": "assistant",
        "content": (
            "פרויקט Full Stack משלב פיתוח צד לקוח (Frontend) וצד שרת (Backend), "
            "לעיתים עם מסד נתונים — כמו באפליקציית הצ'אט הזו."
        ),
        "offset_sec": 8,
    },
]

for msg in sample_messages:
    created = datetime.fromtimestamp(now.timestamp() + msg["offset_sec"], tz=timezone.utc)
    messages.insert_one(
        {
            "conversationId": conv_id,
            "role": msg["role"],
            "content": msg["content"],
            "createdAt": created,
        }
    )

print(f"Seeded conversation {conv_id} with {len(sample_messages)} messages")
