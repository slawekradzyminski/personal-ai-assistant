import hashlib
import json
import os

import jsonlines
from tqdm import tqdm
import time

from actions.embeddings import get_embeddings
from api.api_completion import api_get_completion

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


def process_chunk(chunk, info):
    if is_uninformative(chunk):
        print("Skipped an uninformative chunk.")
        print(chunk)
        return info

    summary = get_summary(chunk)
    embd = get_embeddings(chunk)
    summary_embd = get_embeddings(summary)
    item = {
        "id": len(info),
        "text": chunk,
        "embd": embd,
        "summary": summary,
        "summary_embd": summary_embd,
    }
    info.append(item)

    return info


def store_info(text, memory_path, chunk_sz=800, max_memory=150):
    info = []
    text = text.replace("\n", " ").split()

    if (len(text) / chunk_sz) >= max_memory:
        raise ValueError("Processing is aborted due to high anticipated costs.")

    for idx in tqdm(range(0, len(text), chunk_sz)):
        chunk = " ".join(text[idx: idx + chunk_sz])
        info = process_chunk(chunk, info)
        time.sleep(3)  # up to 20 api calls per min

    with jsonlines.open(memory_path, mode="w") as f:
        f.write(info)
        print("Finish storing info.")


def load_info(memory_path):
    with open(memory_path, 'r', encoding='utf8') as f:
        for line in f:
            info = json.loads(line)
    return info


def memorize(text):
    sha = hashlib.sha256(text.encode('UTF-8')).hexdigest()
    memory_path = f"memory/{sha}.json"
    file_exists = os.path.exists(memory_path)
    if file_exists:
        print("Detected cached memories.")
    else:
        print("Memorizing...")
        store_info(text, memory_path)
    return memory_path


def get_summary(chunk):
    content = "The following is a passage fragment. Please summarize what information the readers can take away from it:"
    content += "\n" + chunk
    return api_get_completion(content)
