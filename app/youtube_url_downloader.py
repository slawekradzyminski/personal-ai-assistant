import os
import re
from typing import Optional
from yt_dlp import YoutubeDL

def download_audio(yt_url: str, output_dir: str = "downloads") -> Optional[str]:
    try:
        os.makedirs(output_dir, exist_ok=True)
        ydl_opts = _get_ydl_options(output_dir)
        
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(yt_url, download=True)
            filename = ydl.prepare_filename(info)
            final_path = os.path.splitext(filename)[0] + '.mp3'
            print(f'Download completed: {os.path.basename(final_path)}')
            return final_path

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def _to_camel_case(text: str) -> str:
    words = re.sub(r'[^a-zA-Z0-9]', ' ', text).split()
    return words[0].lower() + ''.join(word.title() for word in words[1:])

def _get_ydl_options(output_dir: str) -> dict:
    return {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_dir, '%(title)s-%(id)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
        'progress_hooks': [_progress_hook],
        'preprocess_filename': _to_camel_case,
    }

def _progress_hook(d):
    if d['status'] == 'downloading':
        print(f"Downloading... {d['_percent_str']} of {d.get('_total_bytes_str', 'Unknown size')}")
    elif d['status'] == 'finished':
        print("Download finished, now converting...")
