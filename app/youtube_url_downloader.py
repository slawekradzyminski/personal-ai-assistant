import yt_dlp
import re
import os

output_template = "downloads/%(title)s-%(id)s.%(ext)s"
ydl_opts = {
    "format": "m4a/bestaudio/best",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "m4a",
        }
    ],
    "outtmpl": output_template,
}


def download_audio(yt_url):
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(yt_url, download=False)
            filename = ydl.prepare_filename(info)
            final_path = os.path.splitext(filename)[0] + ".m4a"
            ydl.download([yt_url])

            return final_path

    except Exception as e:
        print(f"Error downloading video: {str(e)}")
        raise


def is_youtube_url(url):
    youtube_pattern = re.compile(
        r"(https?://)?(www\.)?"
        r"(youtube|youtu|youtube-nocookie)\.(com|be)/"
        r"(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})"
    )
    return bool(youtube_pattern.match(url))
