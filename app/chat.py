import time

import numpy as np
from numpy.linalg import norm

from api.api_completion import get_completion
from api.api_embedding import get_embedding
from app.config import tokenizer, bcolors
from app.memory import load_info


def get_question():
    q = input("Enter your question: ")
    return q


def retrieve(q_embd, info):
    # return the indices of top three related texts
    text_embds = []
    summary_embds = []
    for item in info:
        text_embds.append(item["embd"])
        summary_embds.append(item["summary_embd"])
    # compute the cos sim between info_embds and q_embd
    text_cos_sims = np.dot(text_embds, q_embd) / (norm(text_embds, axis=1) * norm(q_embd))
    summary_cos_sims = np.dot(summary_embds, q_embd) / (norm(summary_embds, axis=1) * norm(q_embd))
    cos_sims = text_cos_sims + summary_cos_sims
    top_args = np.argsort(cos_sims).tolist()
    top_args.reverse()
    indices = top_args[0:3]
    return indices


def get_qa_content(q, retrieved_text):
    content = "After reading some relevant passage fragments from the same document, please respond to the following query. Note that there may be typographical errors in the passages due to the text being fetched from a PDF file or web page."

    content += "\nQuery: " + q

    for i in range(len(retrieved_text)):
        content += "\nPassage " + str(i + 1) + ": " + retrieved_text[i]

    content += "\nAvoid explicitly using terms such as 'passage 1, 2 or 3' in your answer as the questioner may not know how the fragments are retrieved. You can use your own knowledge in addition to the provided information to enhance your response. Please use the same language as in the query to respond, to ensure that the questioner can understand."

    return content


def generate_answer(q, retrieved_indices, info):
    while True:
        sorted_indices = sorted(retrieved_indices)
        retrieved_text = [info[idx]["text"] for idx in sorted_indices]
        content = get_qa_content(q, retrieved_text)
        if len(tokenizer.encode(content)) > 3800:
            retrieved_indices = retrieved_indices[:-1]
            print("Contemplating...")
            if not retrieved_indices:
                raise ValueError("Failed to respond.")
        else:
            break
    return get_completion(content)


def answer(q, info):
    q_embd = get_embedding(q, model="text-embedding-ada-002")
    retrieved_indices = retrieve(q_embd, info)
    return generate_answer(q, retrieved_indices, info)


def chat(memory_path):
    info = load_info(memory_path)
    while True:
        q = get_question()
        if len(tokenizer.encode(q)) > 200:
            raise ValueError("Input query is too long!")
        response = answer(q, info)
        print()
        print(f"{bcolors.OKGREEN}{response}{bcolors.ENDC}")
        print()
        time.sleep(3)  # up to 20 api calls per min
