import validators
import os
import requests
from bs4 import BeautifulSoup
import fitz
import docx


def get_text(text_path):
    url = text_path
    suffix = os.path.splitext(text_path)[-1]
    if validators.url(url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36", }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            text = soup.get_text()
        else:
            raise ValueError(f"Invalid URL! Status code {response.status_code}.")
    elif suffix == ".pdf":
        full_text = ""
        num_pages = 0
        with fitz.open(text_path) as doc:
            for page in doc:
                num_pages += 1
                text = page.get_text()
                full_text += text + "\n"
        text = f"This is a {num_pages}-page document.\n" + full_text
    elif ".doc" in suffix:
        doc = docx.Document(text_path)
        fullText = []
        for para in doc.paragraphs:
            fullText.append(para.text)
        text = '\n'.join(fullText)
    elif suffix == ".txt":
        with open(text_path, 'r', encoding='utf8') as f:
            lines = f.readlines()
        text = '\n'.join(lines)
    else:
        raise ValueError("Invalid document path!")
    text = " ".join(text.split())
    return text


