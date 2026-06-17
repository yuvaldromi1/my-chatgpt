# My ChatGPT — Full Stack Web Developer Project

אתר צ'אט המאפשר לנהל שיחה מתמשכת עם מודל שפה (OpenAI), בדומה ל-ChatGPT.
השיחות נשמרות במסד נתונים MongoDB.

**מתכנת:** Yuval Dromi
**קורס:** Full Stack Web Developer, ג'ון ברייס

## קישור ל-GitHub

> 🔗 https://github.com/yuvaldromi1/My-ChatGPT

## מבנה הפרויקט

```
Yuval Dromi/
├── Database/    Export של מסד הנתונים (MongoDB)
├── Backend/     צד שרת — Python FastAPI + Postman collection
└── Frontend/    צד לקוח — React (Vite)
```

## טכנולוגיות

- **Backend:** Python, FastAPI, Motor (MongoDB async), OpenAI SDK
- **Frontend:** React, Vite, Axios, React Router
- **Database:** MongoDB

---

## הרצה מקומית

### 1) מסד נתונים
ודא ש-MongoDB מותקן ורץ מקומית (ברירת מחדל: `mongodb://localhost:27017`).
לשחזור נתוני הדוגמה מההגשה: ראה [Database/README.md](Database/README.md).

### Frontend — שחזור שיחה
בטעינת הדף, האפליקציה משחזרת את השיחה האחרונה מ-`sessionStorage` באמצעות `GET /api/conversations/{id}/messages`.

### 2) Backend
```bash
cd Backend
python -m venv venv
venv\Scripts\activate        # ב-Windows
pip install -r requirements.txt
copy .env.example .env       # ואז מלא את OPENAI_API_KEY בקובץ .env
uvicorn main:app --reload
```
השרת יעלה בכתובת http://localhost:8000 (תיעוד אוטומטי: http://localhost:8000/docs).

### 3) Frontend
```bash
cd Frontend
npm install
npm run dev
```
הלקוח יעלה בכתובת http://localhost:5173.

---

## נקודות קצה (REST API)

| Method | Endpoint | תיאור |
|--------|----------|-------|
| POST | `/api/conversations` | פתיחת שיחה חדשה, מחזיר `conversationId` |
| POST | `/api/conversations/{id}/messages` | שליחת הודעת משתמש וקבלת תשובת הצ'אט |
| GET | `/api/conversations/{id}/messages` | שליפת היסטוריית שיחה |

## מסד הנתונים (MongoDB — `chatgpt_db`)

- **conversations**: `{ _id, title, createdAt }`
- **messages**: `{ _id, conversationId, role: "user"|"assistant", content, createdAt }`

`role` מאפשר לזהות מי כתב כל הודעה, ו-`conversationId` מבדיל בין שיחות שונות.

## אבטחה

- הפנייה ל-OpenAI מתבצעת מצד השרת בלבד.
- מפתח ה-API נשמר בקובץ `Backend/.env` ואינו עולה ל-GitHub (`.gitignore`).
