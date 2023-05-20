import os

from api.api_embeddings import api_get_embeddings
from opensource.instructor_embeddings import get_free_embeddings

use_open_ai_api = os.getenv('USE_OPEN_AI_API') == 'True'


def get_embeddings(text):
    if use_open_ai_api:
        return api_get_embeddings(text)

    return get_free_embeddings(text)
