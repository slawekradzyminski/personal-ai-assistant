import yt_dlp
import re
import os
import re
from typing import Optional
from yt_dlp import YoutubeDL

def download_audio(yt_url: str, output_dir: str = "downloads") -> Optional[str]:
    """
    Download audio from a YouTube video URL
    
    Args:
        yt_url: YouTube video URL
        output_dir: Directory to save downloaded files (default: "downloads")
        
    Returns:
        Path to downloaded file or None if download fails
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Configure yt-dlp options
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_dir, '%(title)s-%(id)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
            'progress_hooks': [lambda d: print(f'Downloading... {d["_percent_str"]}' if d["status"] == "downloading" else "")],
        }

        # Download the audio
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(yt_url, download=True)
            # Get the downloaded file path
            file_path = os.path.join(
                output_dir,
                f"{info['title']}-{info['id']}.mp3"
            )
            print(f'Download completed: {os.path.basename(file_path)}')
            return file_path

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def is_youtube_url(url: str) -> bool:
    """
    Check if URL is a valid YouTube URL
    
    Args:
        url: URL to check
        
    Returns:
        True if valid YouTube URL, False otherwise
    """
    youtube_pattern = re.compile(
        r'^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$'
    )
    return bool(youtube_pattern.match(url))