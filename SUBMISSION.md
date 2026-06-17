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

1. צור repository חדש ב-GitHub: https://github.com/new  
   - שם מומלץ: `My-ChatGPT`  
   - Public או Private לפי דרישות הקורס  
   - **אל** תסמן "Add a README" (כבר קיים בפרויקט)
2. מהתיקייה `Yuval Dromi` הרץ:
   ```bash
   git remote add origin https://github.com/yuvaldromi1/My-ChatGPT.git
   git push -u origin main
   ```
   (אם `origin` כבר קיים: `git push -u origin main` בלבד)
3. ודא שהקישור ב-`README.md` תואם ל-repository האמיתי.

> **סטטוס:** ה-remote כבר מוגדר מקומית. נשאר ליצור את ה-repository ב-GitHub ולהריץ `git push`.

## קובץ ZIP מוכן

נוצר קובץ הגשה נקי (בלי `node_modules`, `venv`, `.env`):

`C:\Projects\Yuval-Dromi-Submission.zip`

עותק תיקייה נקייה (לפני ZIP): `C:\Projects\Yuval-Dromi-Submission`

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
