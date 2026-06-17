export default function About() {
  return (
    <div className="about">
      <h1>אודות המערכת</h1>
      <p>
        זהו אתר צ'אט המאפשר לנהל שיחה מתמשכת עם מודל שפה (OpenAI), בדומה ל-ChatGPT.
        השיחות נשמרות במסד נתונים MongoDB, וניתן לראות עבור כל הודעה האם נכתבה ע"י
        המשתמש או ע"י הצ'אט, וכן להבחין בין שיחות שונות לפי מזהה ייחודי.
      </p>

      <h2>הטכנולוגיות</h2>
      <ul>
        <li>צד שרת: Python + FastAPI (REST API)</li>
        <li>צד לקוח: React (SPA) + Vite</li>
        <li>מסד נתונים: MongoDB</li>
        <li>בינה מלאכותית: OpenAI API (הפנייה מצד השרת בלבד)</li>
      </ul>

      <h2>על המתכנת</h2>
      <p>
        פותח ע"י <strong>Yuval Dromi</strong> כפרויקט סיום בקורס Full Stack Web
        Developer, ג'ון ברייס.
      </p>
    </div>
  )
}
