import os
import tempfile

import math
from pydub import AudioSegment
from pydub.silence import split_on_silence

from api.api_whisper import api_get_transcript


def process_audio(path):
    print('Transcripting the audio file...')
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"Audio file not found: {path}")
        
    file_size = os.path.getsize(path)
    whisper_api_size_limit = 25 * 1024 * 1024

    if file_size > whisper_api_size_limit:
        print('File is bigger than 25MB. Processing in chunks')
        transcript = process_large_audio(path)
    else:
        transcript = api_get_transcript(path)

    return transcript


def process_large_audio(path):
    extension = get_extension(path)
    sound = AudioSegment.from_file(path, format=extension)
    chunks = split_audio_into_chunks(sound)
    return process_each_chunk_and_get_full_transcript(chunks, extension)


def process_each_chunk_and_get_full_transcript(chunks, extension):
    full_transcript = ''
    for idx, chunk in enumerate(chunks):
        with tempfile.NamedTemporaryFile(delete=True, suffix=f'.{extension}') as temp_file:
            chunk.export(temp_file.name, format=extension)
            transcript_chunk = api_get_transcript(temp_file.name)
            full_transcript += f" [Chunk {idx + 1}] " + transcript_chunk

    return full_transcript


# https://github.com/jiaaro/pydub/issues/169
def calculate_silence_thresh(dbfs):
    rounded_down_value = math.floor(dbfs)
    result = rounded_down_value - 2
    return result


def split_audio_into_chunks(sound):
    chunks = split_on_silence(
        sound,
        min_silence_len=1000,
        silence_thresh=calculate_silence_thresh(sound.dBFS),
        keep_silence=100,
        seek_step=100
    )
    ten_minutes = 10 * 60 * 1000  # 10 minutes will produce files smaller than 25 MB
    target_length = ten_minutes
    output_chunks = [chunks[0]]
    for chunk in chunks[1:]:
        if len(output_chunks[-1]) < target_length:
            output_chunks[-1] += chunk
        else:
            output_chunks.append(chunk)

    return output_chunks


def get_extension(path):
    return os.path.splitext(path)[1][1:]
