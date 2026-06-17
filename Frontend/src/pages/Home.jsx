import { useEffect, useState } from 'react'
import { createConversation, sendMessage } from '../api.js'
import ChatWindow from '../components/ChatWindow.jsx'
import MessageInput from '../components/MessageInput.jsx'

export default function Home() {
  const [conversationId, setConversationId] = useState(null)
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)

  async function startNewConversation() {
    setMessages([])
    setConversationId(null)
    try {
      const id = await createConversation()
      setConversationId(id)
    } catch {
      // אם השרת לא זמין, נציג הודעה בעת השליחה
    }
  }

  // ב-Refresh מתחילים שיחה חדשה (אין חובה לשחזר את הקודמת)
  useEffect(() => {
    startNewConversation()
  }, [])

  async function handleSend(text) {
    if (!conversationId) {
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: 'השרת אינו זמין כרגע. ודא שה-Backend רץ.' },
      ])
      return
    }

    setMessages((prev) => [...prev, { role: 'user', content: text }])
    setLoading(true)
    try {
      const reply = await sendMessage(conversationId, text)
      setMessages((prev) => [...prev, { role: reply.role, content: reply.content }])
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: 'שגיאה: לא ניתן לקבל תשובה מהשרת.' },
      ])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="home">
      <div className="chat-header">
        <button className="new-chat-btn" onClick={startNewConversation}>
          + שיחה חדשה
        </button>
      </div>
      <ChatWindow messages={messages} loading={loading} />
      <MessageInput onSend={handleSend} disabled={loading} />
    </div>
  )
}
