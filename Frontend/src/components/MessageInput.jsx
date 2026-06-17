import { useState } from 'react'

export default function MessageInput({ onSend, disabled }) {
  const [text, setText] = useState('')

  function submit(e) {
    e.preventDefault()
    if (!text.trim()) return
    onSend(text)
    setText('')
  }

  return (
    <form className="message-input" onSubmit={submit}>
      <input
        type="text"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="כתוב הודעה..."
        disabled={disabled}
      />
      <button type="submit" disabled={disabled}>
        שלח
      </button>
    </form>
  )
}
