from routers import conversations


def create_conversation(client):
    response = client.post("/api/conversations")
    assert response.status_code == 200
    return response.json()["conversationId"]


def test_health_check(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_conversation_returns_id(client):
    conversation_id = create_conversation(client)
    assert len(conversation_id) == 24


def test_new_conversation_has_no_messages(client):
    conversation_id = create_conversation(client)
    response = client.get(f"/api/conversations/{conversation_id}/messages")
    assert response.status_code == 200
    assert response.json() == []


def test_send_message_returns_assistant_reply(client):
    conversation_id = create_conversation(client)
    response = client.post(f"/api/conversations/{conversation_id}/messages", json={"content": "Hello"})
    assert response.status_code == 200
    assert response.json() == {"role": "assistant", "content": "Echo: Hello"}


def test_history_is_saved_in_order(client):
    conversation_id = create_conversation(client)
    client.post(f"/api/conversations/{conversation_id}/messages", json={"content": "First"})
    client.post(f"/api/conversations/{conversation_id}/messages", json={"content": "Second"})

    messages = client.get(f"/api/conversations/{conversation_id}/messages").json()
    assert [m["role"] for m in messages] == ["user", "assistant", "user", "assistant"]
    assert [m["content"] for m in messages] == ["First", "Echo: First", "Second", "Echo: Second"]


def test_full_history_is_sent_to_the_model(client, fake_ai):
    conversation_id = create_conversation(client)
    client.post(f"/api/conversations/{conversation_id}/messages", json={"content": "My name is Yuval"})
    client.post(f"/api/conversations/{conversation_id}/messages", json={"content": "What is my name?"})

    last_history = fake_ai[-1]
    assert last_history[0] == {"role": "user", "content": "My name is Yuval"}
    assert last_history[-1] == {"role": "user", "content": "What is my name?"}
    assert len(last_history) == 3


def test_conversations_are_isolated(client):
    first = create_conversation(client)
    second = create_conversation(client)
    client.post(f"/api/conversations/{first}/messages", json={"content": "Only in first"})

    assert client.get(f"/api/conversations/{second}/messages").json() == []


def test_invalid_id_returns_400(client):
    response = client.get("/api/conversations/not-an-id/messages")
    assert response.status_code == 400


def test_unknown_conversation_returns_404(client):
    missing = "0123456789abcdef01234567"
    assert client.get(f"/api/conversations/{missing}/messages").status_code == 404
    assert client.post(f"/api/conversations/{missing}/messages", json={"content": "hi"}).status_code == 404


def test_missing_content_returns_422(client):
    conversation_id = create_conversation(client)
    response = client.post(f"/api/conversations/{conversation_id}/messages", json={})
    assert response.status_code == 422


def test_openai_failure_returns_502(client, monkeypatch):
    def broken(history):
        raise RuntimeError("service unavailable")

    monkeypatch.setattr(conversations, "get_chat_response", broken)
    conversation_id = create_conversation(client)
    response = client.post(f"/api/conversations/{conversation_id}/messages", json={"content": "Hello"})
    assert response.status_code == 502
