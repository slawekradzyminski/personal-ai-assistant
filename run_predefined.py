from app.config import load_openai_api_key
from app.input_reader import get_text
from app.memory import memorize
from app.chat import chat

document_path = 'https://www.awesome-testing.com/2023/05/bi-directional-contract-testing'

load_openai_api_key()

text = get_text(document_path)
memory_path = memorize(text)
chat(memory_path)
