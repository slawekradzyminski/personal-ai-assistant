import os
import re
import validators

from app.youtube_url_downloader import download_audio
from modals.audio_processor import process_audio
from modals.doc_processor import process_doc
from modals.epub_processor import process_epub
from modals.pdf_processor import process_pdf
from modals.txt_processor import process_txt
from modals.url_processor import process_url

def extract_text(path):
    suffix = os.path.splitext(path)[-1].lower()

    if validators.url(path):
        text = _process_url_input(path)
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
        text = processor(path)

    text = " ".join(text.split())
    return text

def _process_url_input(url: str) -> str:
    if _is_youtube_url(url):
        audio_path = download_audio(url)
        return process_audio(audio_path)
    return process_url(url)

def _is_youtube_url(url: str) -> bool:
    youtube_pattern = re.compile(
        r'^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$'
    )
    return bool(youtube_pattern.match(url))

def _unsupported_file_type(_):
    raise ValueError("Invalid document path!")
