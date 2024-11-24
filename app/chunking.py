from tqdm import tqdm
from app.config import tokenizer

def is_uninformative(chunk):
    if not chunk or chunk.isspace():
        return True
        
    chunk = chunk.strip()
    too_short = len(chunk) < 10
    
    encoded_tokens = tokenizer.encode(chunk)
    encoded_length = len(encoded_tokens)
    char_length = len(chunk)
    
    worthless = encoded_length >= (char_length * 2)
    
    return too_short or worthless

def create_chunks(text, chunk_sz=800, max_memory=150):
    chunks = []
    
    if (len(text.split()) / chunk_sz) >= max_memory:
        raise ValueError("Processing is aborted due to high anticipated costs.")

    paragraphs = text.split("\n\n")
    current_chunk = []
    current_length = 0
    
    for paragraph in tqdm(paragraphs):
        sentences = paragraph.replace("\n", " ").split(". ")
        
        for sentence in sentences:
            if not sentence.endswith("."):
                sentence = sentence.strip() + "."
                
            sentence_tokens = tokenizer.encode(sentence)
            sentence_length = len(sentence_tokens)
    
            if current_length + sentence_length > chunk_sz:
                chunk_text = " ".join(current_chunk)
                if not is_uninformative(chunk_text):
                    chunks.append(chunk_text)
                current_chunk = [sentence]
                current_length = sentence_length
            else:
                current_chunk.append(sentence)
                current_length += sentence_length
                
        if current_chunk and current_length < chunk_sz:
            current_chunk.append("\n\n")
            
    if current_chunk:
        chunk_text = " ".join(current_chunk).strip()
        if not is_uninformative(chunk_text):
            chunks.append(chunk_text)
            
    return chunks 