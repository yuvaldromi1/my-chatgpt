import os

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

client = AsyncIOMotorClient(MONGO_URI)
db = client["chatgpt_db"]

# אוסף השיחות (מזהה ייחודי לכל שיחה) ואוסף ההודעות
conversations_collection = db["conversations"]
messages_collection = db["messages"]
