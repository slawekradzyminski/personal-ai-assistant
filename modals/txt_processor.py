def process_txt(path):
    with open(path, 'r', encoding='utf8') as f:
        lines = f.readlines()
    return '\n'.join(lines)