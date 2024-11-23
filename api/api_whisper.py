import openai
import backoff
client = openai.OpenAI()

@backoff.on_exception(backoff.expo, (openai.RateLimitError, openai.OpenAIError), max_tries=10)
def api_get_transcript(text_path):
    with open(text_path, 'rb') as f:
        response = client.audio.transcriptions.create(
            file=f,
            model='whisper-1',
            response_format='text'
        )

    return response