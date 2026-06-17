import axios from 'axios'

// כל הפניות עוברות דרך ה-Backend (FastAPI). המפתח של OpenAI נמצא בשרת בלבד.
const api = axios.create({
  baseURL: 'http://localhost:8000/api',
})

export async function createConversation() {
  const { data } = await api.post('/conversations')
  return data.conversationId
}

export async function sendMessage(conversationId, content) {
  const { data } = await api.post(
    `/conversations/${conversationId}/messages`,
    { content },
  )
  return data // { role, content }
}

export async function getMessages(conversationId) {
  const { data } = await api.get(`/conversations/${conversationId}/messages`)
  return data // [{ role, content }, ...]
}
