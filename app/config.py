import os

import openai
import tiktoken

tokenizer = tiktoken.get_encoding("cl100k_base")


def load_openai_api_key():
    openai.api_key = os.environ.get("OPEN_API_TOKEN")
    if openai.api_key:
        print("Loaded openai api key.")
    else:
        raise ValueError("Environment variable 'OPEN_API_TOKEN' not found.")


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
