import openai


def get_transcript(text_path):
    with open(text_path, 'rb') as f:
        response = openai.Audio.transcribe(
            file=f,
            model='whisper-1',
            response_format='text'
        )

    return response
