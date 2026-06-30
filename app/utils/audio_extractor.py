from yt_dlp import YoutubeDL

def get_audio_url(video_id: str) -> str:
    url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "skip_download": True,
        "noplaylist": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info["url"]