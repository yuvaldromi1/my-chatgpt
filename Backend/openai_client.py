import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

SYSTEM_PROMPT = "You are a knowledgeable assistant. Provide clear, accurate, and well-structured answers."


def get_chat_response(history):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
    )
    return response.choices[0].message.content
