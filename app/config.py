import os
from dotenv import load_dotenv
import tiktoken

load_dotenv()

tokenizer = tiktoken.get_encoding("cl100k_base")

def load_openai_api_key():
    api_key = os.getenv('OPEN_API_TOKEN')
    if not api_key:
        raise ValueError("Environment variable 'OPEN_API_TOKEN' not found.")
    return api_key

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
