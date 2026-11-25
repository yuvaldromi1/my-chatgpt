import { useEffect, useState } from 'react'
import { createConversation, getMessages, sendMessage } from '../api.js'
import ChatWindow from '../components/ChatWindow.jsx'
import MessageInput from '../components/MessageInput.jsx'

const STORAGE_KEY = 'chatgpt_conversationId'

export default function Home() {
    const [conversationId, setConversationId] = useState(null)
    const [messages, setMessages] = useState([])
    const [loading, setLoading] = useState(false)

    async function startNewConversation() {
        setMessages([])
        setConversationId(null)
        sessionStorage.removeItem(STORAGE_KEY)
        try {
            const id = await createConversation()
            setConversationId(id)
            sessionStorage.setItem(STORAGE_KEY, id)
        } catch {
            // server unavailable
        }
    }

    useEffect(() => {
        async function initConversation() {
            const savedId = sessionStorage.getItem(STORAGE_KEY)
            if (savedId) {
                try {
                    const history = await getMessages(savedId)
                    setConversationId(savedId)
                    setMessages(history)
                    return
                } catch {
                    sessionStorage.removeItem(STORAGE_KEY)
                }
            }
            await startNewConversation()
        }
        initConversation()
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
        } catch (err) {
            if (err.response?.status === 404) {
                sessionStorage.removeItem(STORAGE_KEY)
                try {
                    const id = await createConversation()
                    setConversationId(id)
                    sessionStorage.setItem(STORAGE_KEY, id)
                    const reply = await sendMessage(id, text)
                    setMessages((prev) => [...prev, { role: reply.role, content: reply.content }])
                    return
                } catch {
                    // fallback to general error
                }
            }
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
