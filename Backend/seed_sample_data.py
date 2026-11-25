from datetime import datetime, timezone

from bson import ObjectId
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
client = MongoClient(MONGO_URI)
db = client["chatgpt_db"]

conversations = db["conversations"]
messages = db["messages"]

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
    {"role": "user", "content": "Hello! Who are you?", "offset_sec": 0},
    {
        "role": "assistant",
        "content": "Hello! I am a virtual assistant. How can I help you today?",
        "offset_sec": 2,
    },
    {"role": "user", "content": "What is a Full Stack project?", "offset_sec": 5},
    {
        "role": "assistant",
        "content": (
            "A Full Stack project combines client-side development (Frontend) and "
            "server-side development (Backend), often with a database - like this chat application."
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
