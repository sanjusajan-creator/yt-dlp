from yt_dlp import YoutubeDL

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.youtube.com/",
}

# Player clients to try in order (tv and mweb are less restricted than web)
PLAYER_CLIENTS = ["tv", "mweb", "web"]


def _try_extract(video_id: str, player_client: str) -> str:
    url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "skip_download": True,
        "noplaylist": True,
        "no_check_certificates": True,
        "http_headers": HEADERS,
        "extractor_args": {"youtube": {"player_client": [player_client]}},
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info["url"]


def get_audio_url(video_id: str) -> str:
    last_error = None
    for client in PLAYER_CLIENTS:
        try:
            return _try_extract(video_id, client)
        except Exception as e:
            last_error = e
            continue

    # Final attempt with default settings
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"
        ydl_opts = {
            "format": "bestaudio/best",
            "quiet": True,
            "skip_download": True,
            "noplaylist": True,
            "no_check_certificates": True,
            "http_headers": HEADERS,
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info["url"]
    except Exception as e:
        raise last_error or e
