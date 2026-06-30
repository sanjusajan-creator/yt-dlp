import os
import json
import base64
import tempfile
from yt_dlp import YoutubeDL

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.youtube.com/",
}

PLAYER_CLIENTS = ["tv", "mweb", "web"]

# Supports two env vars:
#   YOUTUBE_COOKIES      - raw Netscape/JSON cookie content (may lose newlines on Vercel)
#   YOUTUBE_COOKIES_B64  - base64-encoded cookie content (safe for env vars)
COOKIES_RAW = os.environ.get("YOUTUBE_COOKIES", "")
COOKIES_B64 = os.environ.get("YOUTUBE_COOKIES_B64", "")
_cookies_file = None


def _get_cookies_file():
    global _cookies_file
    if _cookies_file and os.path.exists(_cookies_file):
        return _cookies_file

    content = ""

    # Prefer base64 (no newline issues)
    if COOKIES_B64:
        try:
            content = (
                base64.b64decode(COOKIES_B64).decode("utf-8", errors="replace").strip()
            )
        except Exception:
            pass

    # Fallback to raw
    if not content and COOKIES_RAW:
        content = COOKIES_RAW.strip()

    if not content:
        return None

    # Convert JSON cookie format to Netscape if needed
    if content.startswith("["):
        try:
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
        except json.JSONDecodeError:
            pass

    tmp = tempfile.NamedTemporaryFile(
        delete=False, suffix=".txt", mode="w", encoding="utf-8"
    )
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


def cookies_status():
    """Debug: check if cookies are loaded"""
    has_raw = bool(COOKIES_RAW)
    has_b64 = bool(COOKIES_B64)
    file_path = _get_cookies_file()
    file_exists = file_path and os.path.exists(file_path)
    file_lines = 0
    if file_exists:
        with open(file_path, "r") as f:
            file_lines = len(f.readlines())
    return {
        "has_raw_env": has_raw,
        "has_b64_env": has_b64,
        "cookies_file": file_path,
        "file_exists": file_exists,
        "cookie_lines": file_lines,
    }
