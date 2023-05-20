from InstructorEmbedding import INSTRUCTOR

model = INSTRUCTOR('hkunlp/instructor-xl')


def get_free_embeddings(text):
    return model.encode(text).tolist()
