from tqdm import tqdm
from app.config import tokenizer

def create_chunks(text, chunk_sz=800, max_memory=150):
    if _exceeds_memory_limit(text, chunk_sz, max_memory):
        raise ValueError("Processing is aborted due to high anticipated costs.")

    paragraphs = text.split("\n\n")
    chunks = []
    current_chunk = []
    current_length = 0

    for paragraph in tqdm(paragraphs):
        current_chunk, current_length, new_chunks = _process_paragraph(
            paragraph, current_chunk, current_length, chunk_sz
        )
        chunks.extend(new_chunks)

    if current_chunk:
        final_chunk = _finalize_chunk(current_chunk)
        if not _is_uninformative(final_chunk):
            chunks.append(final_chunk)

    return chunks

def _process_paragraph(paragraph, current_chunk, current_length, chunk_sz):
    sentences = _split_into_sentences(paragraph)
    new_chunks = []

    for sentence in sentences:
        current_chunk, current_length, chunk = _process_sentence(
            sentence, current_chunk, current_length, chunk_sz
        )
        if chunk and not _is_uninformative(chunk):
            new_chunks.append(chunk.strip())

    return current_chunk, current_length, new_chunks

def _split_into_sentences(paragraph):
    return [_normalize_sentence(s) for s in paragraph.replace("\n", " ").split(". ")]

def _normalize_sentence(sentence):
    if not sentence.endswith("."):
        sentence = sentence.strip() + "."
    return sentence

def _process_sentence(sentence, current_chunk, current_length, chunk_sz):
    sentence_tokens = tokenizer.encode(sentence)
    sentence_length = len(sentence_tokens)
    chunk = None

    if current_length + sentence_length > chunk_sz:
        chunk = " ".join(current_chunk)
        current_chunk = [sentence]
        current_length = sentence_length
    else:
        current_chunk.append(sentence)
        current_length += sentence_length

    return current_chunk, current_length, chunk

def _finalize_chunk(chunk):
    return " ".join(chunk).strip()

def _exceeds_memory_limit(text, chunk_sz, max_memory):
    return (len(text.split()) / chunk_sz) >= max_memory

def _is_uninformative(chunk):
    if not chunk or chunk.isspace():
        return True
        
    chunk = chunk.strip()
    too_short = len(chunk) < 10
    
    encoded_tokens = tokenizer.encode(chunk)
    encoded_length = len(encoded_tokens)
    char_length = len(chunk)
    
    worthless = encoded_length >= (char_length * 2)
    
    return too_short or worthless