import os
import ebooklib
from bs4 import BeautifulSoup
from ebooklib import epub


def process_epub(epub_path):
    if not os.path.exists(epub_path):
        raise FileNotFoundError(f"File not found: {epub_path}")

    chapters = epub2thtml(epub_path)
    text = thtml2ttext(chapters)
    delimiter = " "
    return delimiter.join(text)


def epub2thtml(epub_path):
    book = epub.read_epub(epub_path)
    chapters = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            chapters.append(item.get_content())
    return chapters


blacklist = [
    '[document]',
    'noscript',
    'header',
    'html',
    'meta',
    'head',
    'input',
    'script',
]


def chap2text(chap):
    output = ''
    soup = BeautifulSoup(chap, 'html.parser')
    text = soup.find_all(text=True)
    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)
    return output


def thtml2ttext(thtml):
    output = []
    for html in thtml:
        text = chap2text(html)
        output.append(text)
    return output
