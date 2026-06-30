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

# tv = DRM protected, web = needs PO token, so use web_embedded which is less restricted
PLAYER_CLIENTS = ["web_embedded", "web", "mweb"]

COOKIES_RAW = os.environ.get("YOUTUBE_COOKIES", "")
COOKIES_B64 = os.environ.get("YOUTUBE_COOKIES_B64", "")
_cookies_file = None


def _get_cookies_file():
    global _cookies_file
    if _cookies_file and os.path.exists(_cookies_file):
        return _cookies_file

    content = ""

    # Try base64 env var first
    if COOKIES_B64:
        try:
            content = (
                base64.b64decode(COOKIES_B64).decode("utf-8", errors="replace").strip()
            )
        except Exception:
            pass

    # Try raw env var
    if not content and COOKIES_RAW:
        content = COOKIES_RAW.strip()

    # Try local cookies.txt file
    if not content:
        local_path = os.path.join(
            os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            ),
            "cookies.txt",
        )
        if os.path.exists(local_path):
            with open(local_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read().strip()

    if not content:
        return None

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


def _base_opts():
    """Common yt-dlp options"""
    opts = {
        "format": "ba/b",
        "quiet": True,
        "skip_download": True,
        "noplaylist": True,
        "no_check_certificates": True,
        "http_headers": HEADERS,
        "js_runtimes": {"nodejs": {}},
    }
    cookies_file = _get_cookies_file()
    if cookies_file:
        opts["cookiefile"] = cookies_file
    return opts


def _try_extract(video_id: str, player_client: str) -> str:
    url = f"https://www.youtube.com/watch?v={video_id}"
    opts = _base_opts()
    opts["extractor_args"] = {"youtube": {"player_client": [player_client]}}

    with YoutubeDL(opts) as ydl:
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

    # Final attempt with no client restriction
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"
        opts = _base_opts()
        with YoutubeDL(opts) as ydl:
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
