import { useEffect, useRef } from 'react'

export default function ChatWindow({ messages, loading }) {
  const endRef = useRef(null)

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  return (
    <div className="chat-window">
      {messages.length === 0 && !loading && (
        <p className="empty-state">התחל שיחה חדשה — כתוב הודעה למטה 👇</p>
      )}

      {messages.map((m, i) => (
        <div key={i} className={`message ${m.role}`}>
          <div className="bubble">{m.content}</div>
        </div>
      ))}

      {loading && (
        <div className="message assistant">
          <div className="bubble typing">מקליד…</div>
        </div>
      )}

      <div ref={endRef} />
    </div>
  )
}
