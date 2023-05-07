import docx


def process_doc(text_path):
    doc = docx.Document(text_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)
