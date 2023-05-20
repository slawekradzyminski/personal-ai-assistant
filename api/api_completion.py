import openai
import backoff


@backoff.on_exception(backoff.expo, (openai.error.RateLimitError, openai.error.OpenAIError), max_tries=10)
def api_get_completion(content):
    messages = [
        {"role": "user", "content": content}
    ]

    completion = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages,
        temperature=0.2,
        top_p=0.95,
        # max_tokens=2000,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    return completion.choices[0].message.content
