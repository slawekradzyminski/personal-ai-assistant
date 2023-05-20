import requests
from bs4 import BeautifulSoup

dummy_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


def process_url(url):
    print('URL detected, downloading & parsing...')
    response = requests.get(url, headers=dummy_headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        text = soup.get_text()
    else:
        raise ValueError(f"Invalid URL! Status code {response.status_code}.")
    return text
