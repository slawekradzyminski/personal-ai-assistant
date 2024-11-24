import pytest
from app.config import load_openai_api_key

def test_load_openai_api_key_success(monkeypatch):
    # given
    monkeypatch.setenv('OPEN_API_TOKEN', 'test-key')
    
    # when
    with pytest.MonkeyPatch.context() as m:
        m.setattr('builtins.print', lambda x: None) 
        load_openai_api_key()
        
    # then do nothing

def test_load_openai_api_key_missing(monkeypatch):
    # given
    monkeypatch.delenv('OPEN_API_TOKEN', raising=False)
    monkeypatch.setattr('dotenv.load_dotenv', lambda: None)
    monkeypatch.setattr('os.getenv', lambda key, default=None: None)
    
    # when
    with pytest.raises(ValueError) as exc_info:
        load_openai_api_key()
        
    # then
    assert str(exc_info.value) == "Environment variable 'OPEN_API_TOKEN' not found."
