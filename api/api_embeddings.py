import openai
import backoff

model = "text-embedding-ada-002"


@backoff.on_exception(backoff.expo, (openai.error.RateLimitError, openai.error.OpenAIError), max_tries=10)
def api_get_embeddings(text):
    text = text.replace("\n", " ")
    return openai.Embedding.create(
        input=[text],
        model=model)['data'][0]['embedding']
