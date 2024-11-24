import os
import re
import validators

from app.youtube_url_downloader import download_audio
from processors.audio_processor import process_audio
from processors.doc_processor import process_doc
from processors.epub_processor import process_epub
from processors.pdf_processor import process_pdf
from processors.txt_processor import process_txt
from processors.url_processor import process_url

def get_text(text_path):
    suffix = os.path.splitext(text_path)[-1].lower()

    if validators.url(text_path):
        if _is_youtube_url(text_path):
            audio_path = download_audio(text_path)
            text = process_audio(audio_path)
        else:
            text = process_url(text_path)
    else:
        process_map = {
            ".epub": process_epub,
            ".pdf": process_pdf,
            ".doc": process_doc,
            ".docx": process_doc,
            ".txt": process_txt,
            ".wav": process_audio,
            ".mp3": process_audio,
            ".m4a": process_audio,
        }

        processor = process_map.get(suffix, _unsupported_file_type)
        text = processor(text_path)

    text = " ".join(text.split())
    return text

def _is_youtube_url(url: str) -> bool:
    youtube_pattern = re.compile(
        r'^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$'
    )
    return bool(youtube_pattern.match(url))

def _unsupported_file_type(_):
    raise ValueError("Invalid document path!")
