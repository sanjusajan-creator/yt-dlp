import os
import json
import tempfile
from yt_dlp import YoutubeDL

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.youtube.com/",
}

PLAYER_CLIENTS = ["tv", "mweb", "web"]

# Load cookies from env var (set YOUTUBE_COOKIES in Vercel dashboard)
COOKIES_RAW = os.environ.get("YOUTUBE_COOKIES", "")
_cookies_file = None


def _get_cookies_file():
    global _cookies_file
    if _cookies_file and os.path.exists(_cookies_file):
        return _cookies_file
    if not COOKIES_RAW:
        return None

    # Support both Netscape cookie format (raw text) and JSON format
    content = COOKIES_RAW.strip()
    if content.startswith("["):
        # JSON format — convert to Netscape format
        cookies = json.loads(content)
        lines = ["# Netscape HTTP Cookie File"]
        for c in cookies:
            domain = c.get("domain", "")
            flag = "TRUE" if domain.startswith(".") else "FALSE"
            path = c.get("path", "/")
            secure = "TRUE" if c.get("secure", False) else "FALSE"
            expires = str(int(c.get("expirationDate", 0)))
            name = c.get("name", "")
            value = c.get("value", "")
            lines.append(
                f"{domain}\t{flag}\t{path}\t{secure}\t{expires}\t{name}\t{value}"
            )
        content = "\n".join(lines)

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w")
    tmp.write(content)
    tmp.close()
    _cookies_file = tmp.name
    return _cookies_file


def _try_extract(video_id: str, player_client: str) -> str:
    url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts = {
        "format": "ba/b",
        "quiet": True,
        "skip_download": True,
        "noplaylist": True,
        "no_check_certificates": True,
        "http_headers": HEADERS,
        "extractor_args": {"youtube": {"player_client": [player_client]}},
    }

    cookies_file = _get_cookies_file()
    if cookies_file:
        ydl_opts["cookiefile"] = cookies_file

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
            "format": "ba/b",
            "quiet": True,
            "skip_download": True,
            "noplaylist": True,
            "no_check_certificates": True,
            "http_headers": HEADERS,
        }
        cookies_file = _get_cookies_file()
        if cookies_file:
            ydl_opts["cookiefile"] = cookies_file
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info["url"]
    except Exception as e:
        raise last_error or e
