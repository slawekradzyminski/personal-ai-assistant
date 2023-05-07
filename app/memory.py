import hashlib
import json
import os

import jsonlines
from tqdm import tqdm
import time

from api.api_completion import get_completion
from api.api_embedding import get_embedding
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer


def is_uninformative(chunk):
    parser = PlaintextParser.from_string(chunk, Tokenizer("english"))
    summarizer = TextRankSummarizer()

    # Adjust the sentence count as needed.
    sentence_count = 2
    summarized_sentences = summarizer(parser.document, sentence_count)
    summarized_chunk = " ".join([str(sentence) for sentence in summarized_sentences])

    summarized_length = len(summarized_chunk.split())
    original_length = len(chunk.split())

    # Adjust the threshold as needed.
    return summarized_length / original_length < 0.2


def process_chunk(chunk, info):
    if is_uninformative(chunk) < 0.5:
        print("Skipped an uninformative chunk.")
        return info

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

    return info


def store_info(text, memory_path, chunk_sz=800, max_memory=100):
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
    return get_completion(content)
