def process_txt(text_path):
    with open(text_path, 'r', encoding='utf8') as f:
        lines = f.readlines()
    return '\n'.join(lines)