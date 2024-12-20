import openai
from app.config import load_openai_api_key
from api.logger import log_api_call

class OpenAIClient:
    _instance = None
    
    @classmethod
    def get_client(cls):
        if cls._instance is None:
            api_key = load_openai_api_key()
            cls._instance = openai.OpenAI(api_key=api_key)
        return cls._instance

    @classmethod
    def reset_client(cls):
        cls._instance = None
        
    @classmethod
    def log_request(cls, endpoint, request_data, response, error=None):
        log_api_call(endpoint, request_data, response, error)