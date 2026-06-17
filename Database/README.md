# Database — MongoDB Export

תיקייה זו מיועדת לייצוא מסד הנתונים `chatgpt_db` לפני ההגשה.

## איך לייצא (mongodump)

מתוך שורת הפקודה, כשה-MongoDB רץ:

```bash
mongodump --db chatgpt_db --out "C:\Projects\Yuval Dromi\Database"
```

הפקודה תיצור כאן תיקייה `chatgpt_db` עם קבצי ה-BSON של האוספים
(`conversations` ו-`messages`).

## איך לשחזר (mongorestore) — למי שבודק

```bash
mongorestore --db chatgpt_db "C:\Projects\Yuval Dromi\Database\chatgpt_db"
```

> אם מתקינים MongoDB Database Tools בנפרד — הכלים `mongodump` / `mongorestore`
> מגיעים מחבילת "MongoDB Database Tools".
