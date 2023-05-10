import openai
import backoff


@backoff.on_exception(backoff.expo, (openai.error.RateLimitError, openai.error.OpenAIError), max_tries=10)
def get_transcript(text_path):
    with open(text_path, 'rb') as f:
        response = openai.Audio.transcribe(
            file=f,
            model='whisper-1',
            response_format='text'
        )

    return response
