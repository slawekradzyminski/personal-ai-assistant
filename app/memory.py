import hashlib
import json
import os
import time
import jsonlines

from actions.embeddings import get_embeddings
from api.api_completion import api_get_completion

def process_chunk(chunk, info):
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

def store_info(chunks, memory_path):
    info = []
    
    for chunk in chunks:
        info = process_chunk(chunk, info)
        time.sleep(3)  # Rate limiting

    with jsonlines.open(memory_path, mode="w") as f:
        f.write(info)
        print("Finish storing info.")

def get_summary(chunk):
    content = "The following is a passage fragment. Please summarize what information the readers can take away from it:"
    content += "\n" + chunk
    return api_get_completion(content)

def load_info(memory_path):
    with open(memory_path, 'r', encoding='utf8') as f:
        for line in f:
            info = json.loads(line)
    return info

def memorize(chunks):
    text = "".join(chunks)
    sha = hashlib.sha256(text.encode('UTF-8')).hexdigest()
    memory_path = f"memory/{sha}.json"
    
    if os.path.exists(memory_path):
        print("Detected cached memories.")
    else:
        print("Memorizing...")
        store_info(chunks, memory_path)
    return memory_path
