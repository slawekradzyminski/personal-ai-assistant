import openai


def chatGPT_api(messages):
    completion = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages,
        temperature=0.2,
        top_p=0.95,
        # max_tokens=2000,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    return completion.choices[0].message
