# רשימת הגשה — פרויקט גמר Full Stack Web

## לפני יצירת קובץ ה-ZIP

### למחוק מתוך התיקייה (לא לכלול בהגשה)

| נתיב | סיבה |
|------|------|
| `Frontend/node_modules/` | תלויות — יש להריץ `npm install` מחדש |
| `Frontend/dist/` | build — לא נדרש |
| `Frontend/vite.log` | קובץ לוג |
| `Backend/venv/` או `Backend/.venv/` | סביבה וירטואלית Python |
| `Backend/__pycache__/` | קבצי cache |
| `Backend/.env` | **סודות** — מפתח OpenAI |

### לוודא שכן כלול

| נתיב | סיבה |
|------|------|
| `Backend/.env.example` | תבנית להגדרות (בלי מפתחות אמיתיים) |
| `Backend/requirements.txt` | תלויות Python |
| `Backend/postman_collection.json` | בדיקת API |
| `Frontend/package.json` + `package-lock.json` | תלויות Node |
| `Database/chatgpt_db/` | ייצוא MongoDB (mongodump) |
| `README.md` | הוראות הרצה + קישור GitHub |

## GitHub

1. צור repository בשם `My-ChatGPT` (או עדכן את הקישור ב-`README.md`).
2. העלה את הקוד: `git remote add origin ...` ואז `git push -u origin main`.
3. ודא שהקישור ב-README תואם ל-repository האמיתי.

## בדיקה מהירה לבודק

```bash
# 1. MongoDB
mongorestore --db chatgpt_db "Database/chatgpt_db"

# 2. Backend
cd Backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env   # מלא OPENAI_API_KEY
uvicorn main:app --reload

# 3. Frontend
cd Frontend
npm install
npm run dev
```

פתח http://localhost:5173 — שלח הודעה, רענן את הדף — ההיסטוריה אמורה להיטען מחדש.

## Postman

ייבא את `Backend/postman_collection.json` והרץ: Create Conversation → Send Message → Get Messages.
