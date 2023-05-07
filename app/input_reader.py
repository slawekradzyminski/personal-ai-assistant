import os

import validators

from processors.audio_processor import process_audio
from processors.doc_processor import process_doc
from processors.pdf_processor import process_pdf
from processors.txt_processor import process_txt
from processors.url_processor import process_url


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
