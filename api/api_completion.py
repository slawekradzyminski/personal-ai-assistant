import openai
import backoff

client = openai.OpenAI()

@backoff.on_exception(backoff.expo, (openai.RateLimitError, openai.OpenAIError), max_tries=10)
def api_get_completion(content):
    print(content)
    messages = [
        {"role": "user", "content": content}
    ]
    print(content)

    completion = client.chat.completions.create(model='gpt-3.5-turbo',
    messages=messages,
    temperature=0.2,
    top_p=0.95,
    # max_tokens=2000,
    frequency_penalty=0.0,
    presence_penalty=0.0)

    return completion.choices[0].message.content
