import openai
import backoff
from api.api_client import OpenAIClient

@backoff.on_exception(backoff.expo, (openai.RateLimitError, openai.OpenAIError), max_tries=10)
def api_get_completion(content):
    client = OpenAIClient.get_client()
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant that provides clear and accurate responses."},
        {"role": "user", "content": content}
    ]
    
    request_data = {
        'model': 'gpt-4-turbo-preview',
        'messages': messages,
        'temperature': 0.2,
        'top_p': 0.95,
        'frequency_penalty': 0.0,
        'presence_penalty': 0.0
    }
    
    try:
        completion = client.chat.completions.create(**request_data)
        response = completion.choices[0].message.content
        OpenAIClient.log_request('chat/completions', request_data, response)
        return response
        
    except Exception as e:
        OpenAIClient.log_request('chat/completions', request_data, None, e)
        raise
