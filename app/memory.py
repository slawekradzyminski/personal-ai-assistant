import hashlib
import json
import os

import jsonlines
from tqdm import tqdm
import time

from api.api_completion import chatGPT_api
from api.api_embedding import get_embedding
from app.config import tokenizer


def store_info(text, memory_path, chunk_sz=800, max_memory=100):
    info = []
    text = text.replace("\n", " ").split()
    # raise error if the anticipated api usage is too massive
    if (len(text) / chunk_sz) >= 100:
        raise ValueError("Processing is aborted due to high anticipated costs.")
    for idx in tqdm(range(0, len(text), chunk_sz)):
        chunk = " ".join(text[idx: idx + chunk_sz])
        if len(tokenizer.encode(chunk)) > chunk_sz * 3:
            print("Skipped an uninformative chunk.")
            continue
        summary = get_summary(chunk)
        embd = get_embedding(chunk)
        summary_embd = get_embedding(summary)
        item = {
            "id": len(info),
            "text": chunk,
            "embd": embd,
            "summary": summary,
            "summary_embd": summary_embd,
        }
        info.append(item)
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

    messages = [
        {"role": "user", "content": content}
    ]
    summary = chatGPT_api(messages).content

    return summary
