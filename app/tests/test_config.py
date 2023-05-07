import pytest
from app.config import load_openai_api_key


def test_load_openai_api_key_success(monkeypatch):
    monkeypatch.setenv("OPEN_API_TOKEN", "test_api_key")

    try:
        load_openai_api_key()
    except ValueError:
        pytest.fail("load_openai_api_key() raised ValueError unexpectedly!")


def test_load_openai_api_key_failure(monkeypatch):
    monkeypatch.delenv("OPEN_API_TOKEN", raising=False)

    with pytest.raises(ValueError):
        load_openai_api_key()
