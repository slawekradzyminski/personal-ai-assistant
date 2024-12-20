import openai
import backoff
from api.api_client import OpenAIClient

model = "text-embedding-3-small"

@backoff.on_exception(backoff.expo, (openai.RateLimitError, openai.OpenAIError), max_tries=10)
def api_get_embeddings(text):
    if not text or not isinstance(text, str):
        raise ValueError("Input must be a non-empty string")
        
    client = OpenAIClient.get_client()
    
    text = text.replace("\n", " ").strip()
    
    request_data = {
        'model': model,
        'input': [text]
    }
    
    try:
        response = client.embeddings.create(**request_data)
        embedding = response.data[0].embedding
        OpenAIClient.log_request('embeddings', request_data, f"Generated embedding vector of length {len(embedding)}")
        return embedding
        
    except Exception as e:
        OpenAIClient.log_request('embeddings', request_data, None, e)
        raise
