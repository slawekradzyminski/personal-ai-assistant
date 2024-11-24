import fitz


def process_pdf(path):
    full_text = ""
    num_pages = 0
    with fitz.open(path) as doc:
        for page in doc:
            num_pages += 1
            text = page.get_text()
            full_text += text + "\n"
    return f"This is a {num_pages}-page document.\n" + full_text
