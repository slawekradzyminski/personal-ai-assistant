import sys

from app.config import load_openai_api_key
from app.text_reader import get_text
from app.memory import memorize
from app.chat import chat

if len(sys.argv) < 2:
    print("Usage: python3 main.py <path_to_document>")
    sys.exit(1)

document_path = sys.argv[1]

load_openai_api_key()

text = get_text(document_path)
memory_path = memorize(text)
chat(memory_path)
