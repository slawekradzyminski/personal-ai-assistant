import os
import re

from pytube import YouTube


def download_audio(yt_url):
    print('Detected YouTube URL. Attempting to download the video...')
    yt = YouTube(yt_url, use_oauth=True, allow_oauth_cache=True)
    audio_streams = yt.streams.filter(only_audio=True)
    audio_stream = audio_streams.order_by("abr").desc().first()

    output_dir = "downloads"
    file_name = f"{yt.title}-{yt.video_id}.{audio_stream.subtype}"
    full_file_path = os.path.join(output_dir, file_name)

    if not os.path.exists(full_file_path):
        audio_stream.download(output_path=output_dir, filename=file_name)
        print(f'File downloaded: {file_name}')
    else:
        print(f'File already exists: {file_name}')

    return full_file_path


def is_youtube_url(url):
    youtube_pattern = re.compile(
        r'(https?://)?(www\.)?'
        r'(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    )
    return bool(youtube_pattern.match(url))
