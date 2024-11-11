import os
from dotenv import load_dotenv
import openai
import tiktoken

tokenizer = tiktoken.get_encoding("cl100k_base")

def load_openai_api_key():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Environment variable 'OPENAI_API_KEY' not found.")
    openai.api_key = api_key
    print("Loaded openai api key.")

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
