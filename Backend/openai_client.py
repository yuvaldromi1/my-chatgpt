import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# הפנייה ל-OpenAI מתבצעת מצד השרת בלבד. המפתח נקרא מקובץ ה-.env.
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

SYSTEM_PROMPT = "You are a helpful assistant. Answer clearly and concisely."


def get_chat_response(history):
    """
    מקבל את כל היסטוריית השיחה (רשימת {"role", "content"}),
    מוסיף הודעת מערכת, ומחזיר את תשובת הצ'אט.
    שליחת כל ההיסטוריה היא מה ששומר על ההקשר של השיחה.
    """
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
    )
    return response.choices[0].message.content
