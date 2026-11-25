import os

# Must be set before the app modules are imported.
os.environ.setdefault("OPENAI_API_KEY", "test-key")
os.environ.setdefault("MONGO_URI", "mongodb://localhost:27017")

import pytest
from fastapi.testclient import TestClient
from mongomock_motor import AsyncMongoMockClient

import main
from routers import conversations


@pytest.fixture
def fake_ai(monkeypatch):
    """Replace the OpenAI call; records the history it received."""
    calls = []

    def fake_response(history):
        calls.append(history)
        return f"Echo: {history[-1]['content']}"

    monkeypatch.setattr(conversations, "get_chat_response", fake_response)
    return calls


@pytest.fixture
def client(monkeypatch, fake_ai):
    """API client backed by an in-memory MongoDB."""
    db = AsyncMongoMockClient()["chatgpt_test"]
    monkeypatch.setattr(conversations, "conversations_collection", db["conversations"])
    monkeypatch.setattr(conversations, "messages_collection", db["messages"])
    with TestClient(main.app) as test_client:
        yield test_client
