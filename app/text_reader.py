import validators
import os
import requests
from bs4 import BeautifulSoup
import fitz
import docx

dummy_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


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
    else:
        raise ValueError("Invalid document path!")
    text = " ".join(text.split())
    return text
