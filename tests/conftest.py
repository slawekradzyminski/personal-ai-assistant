import pytest
from unittest.mock import patch
from api.api_client import OpenAIClient

@pytest.fixture(autouse=True)
def mock_environment(monkeypatch):
    monkeypatch.setenv('OPEN_API_TOKEN', 'test-key')
    OpenAIClient.reset_client()

@pytest.fixture(autouse=True)
def mock_openai():
    with patch('openai.OpenAI') as mock_openai:
        mock_client = mock_openai.return_value
        mock_client.chat.completions.create.return_value.choices[0].message.content = "mocked response"
        mock_client.embeddings.create.return_value.data[0].embedding = [0.1, 0.2, 0.3]
        mock_client.audio.transcriptions.create.return_value = "mocked transcript"
        yield mock_client 