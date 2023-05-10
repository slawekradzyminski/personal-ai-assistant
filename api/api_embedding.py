import openai
import backoff


@backoff.on_exception(backoff.expo, (openai.error.RateLimitError, openai.error.OpenAIError), max_tries=10)
def get_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    return openai.Embedding.create(
        input=[text],
        model=model)['data'][0]['embedding']
