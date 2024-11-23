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
            file_path = os.path.join(
                output_dir,
                f"{info['title']}-{info['id']}.mp3"
            )
            print(f'Download completed: {os.path.basename(file_path)}')
            return file_path

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def _get_ydl_options(output_dir: str) -> dict:
    return {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_dir, '%(title)s-%(id)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
        'progress_hooks': [_progress_hook],
    }

def _progress_hook(d):
    if d['status'] == 'downloading':
        print(f"Downloading... {d['_percent_str']} of {d.get('_total_bytes_str', 'Unknown size')}")
    elif d['status'] == 'finished':
        print("Download finished, now converting...")
