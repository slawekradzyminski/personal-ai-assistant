import tempfile

import math
import validators
import os
import requests
from bs4 import BeautifulSoup
import fitz
import docx

from pydub import AudioSegment
from pydub.silence import split_on_silence

from api.api_whisper import get_transcript

dummy_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


def get_extension(text_path):
    return os.path.splitext(text_path)[1][1:]


def process_audio(text_path):
    file_size = os.path.getsize(text_path)

    if file_size > 25 * 1024 * 1024:
        print('File is bigger than 25MB. Processing in chunks')
        transcript = process_large_audio(text_path)
    else:
        transcript = get_transcript(text_path)

    return transcript


def process_large_audio(text_path):
    extension = get_extension(text_path)
    sound = AudioSegment.from_file(text_path, format=extension)
    chunks = split_audio_into_chunks(sound)

    # Process each chunk and concatenate the results
    full_transcript = ''
    for idx, chunk in enumerate(chunks):
        with tempfile.NamedTemporaryFile(delete=True, suffix=f'.{extension}') as temp_file:
            chunk.export(temp_file.name, format=extension)
            transcript_chunk = get_transcript(temp_file.name)
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


def process_url(url):
    headers = dummy_headers
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        text = soup.get_text()
    else:
        raise ValueError(f"Invalid URL! Status code {response.status_code}.")
    return text


def process_pdf(text_path):
    full_text = ""
    num_pages = 0
    with fitz.open(text_path) as doc:
        for page in doc:
            num_pages += 1
            text = page.get_text()
            full_text += text + "\n"
    return f"This is a {num_pages}-page document.\n" + full_text


def process_doc(text_path):
    doc = docx.Document(text_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)


def process_txt(text_path):
    with open(text_path, 'r', encoding='utf8') as f:
        lines = f.readlines()
    return '\n'.join(lines)


def get_text(text_path):
    suffix = os.path.splitext(text_path)[-1]
    if validators.url(text_path):
        text = process_url(text_path)
    elif suffix == ".pdf":
        text = process_pdf(text_path)
    elif ".doc" in suffix:
        text = process_doc(text_path)
    elif suffix == ".txt":
        text = process_txt(text_path)
    elif suffix.lower() in [".wav", ".mp3", ".m4a"]:
        text = process_audio(text_path)
    else:
        raise ValueError("Invalid document path!")
    text = " ".join(text.split())
    return text
