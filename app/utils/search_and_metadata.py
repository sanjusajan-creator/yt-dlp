from youtubesearchpython import VideosSearch
import yt_dlp


def search_youtube(query: str, total_results: int = 100):
    all_results = []
    search = VideosSearch(query, limit=20)
    
    while len(all_results) < total_results:
        result = search.result()
        all_results.extend(result["result"])
        if "next" in result:
            search.next()
        else:
            break

    return all_results[:total_results]


def fetch_metadata(video_url: str):
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "extract_flat": "in_playlist",
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(video_url, download=False)
            return {
                "title": info.get("title"),
                "duration": info.get("duration"),
                "uploader": info.get("uploader"),
                "upload_date": info.get("upload_date"),
                "thumbnail": info.get("thumbnail"),
                "description": info.get("description"),
                "view_count": info.get("view_count"),
                "like_count": info.get("like_count"),
                "url": info.get("webpage_url"),
            }
        except Exception as e:
            return {"error": str(e)}