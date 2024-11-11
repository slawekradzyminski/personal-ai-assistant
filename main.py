import sys
from dotenv import load_dotenv
import os

from app.input_reader import get_text
from app.memory import memorize
from app.chat import chat

if len(sys.argv) < 2:
    print("Usage: python3 main.py <path_to_document>")
    sys.exit(1)

document_path = sys.argv[1]

load_dotenv() 
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    print("Error: OPENAI_API_KEY not found in .env file")
    sys.exit(1)

text = get_text(document_path)
memory_path = memorize(text)
chat(memory_path)
