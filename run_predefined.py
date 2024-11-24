from app.config import load_openai_api_key
from app.input_reader import extract_text
from app.chunking import create_chunks
from app.memory import memorize
from app.chat import chat

def main():
    document_path = 'https://www.awesome-testing.com/2023/05/bi-directional-contract-testing'
    
    load_openai_api_key()
    
    text = extract_text(document_path)
    chunks = create_chunks(text)
    for chunk in chunks:
        print(chunk)
        print("\n")
    memory_path = memorize(chunks)
    chat(memory_path)

if __name__ == '__main__':
    main()
