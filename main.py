#!/usr/bin/env python3
import sys

from app.config import load_openai_api_key
from app.input_reader import extract_text
from app.chunking import create_chunks
from app.memory import memorize
from app.chat import chat

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <path_to_document>")
        sys.exit(1)

    document_path = sys.argv[1]
    load_openai_api_key()

    text = extract_text(document_path)
    chunks = create_chunks(text)
    memory_path = memorize(chunks)
    chat(memory_path)

if __name__ == "__main__":
    main()
