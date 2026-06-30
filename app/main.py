from fastapi import FastAPI, Query
from app.utils.search_and_metadata import search_youtube, fetch_metadata
from app.utils.audio_extractor import cookies_status
from app.api import explore  # Import the explore router

app = FastAPI(title="YouTube Song Search API")

# Include explore router
app.include_router(explore.router)


@app.get("/search")
def search_songs(query: str = Query(..., description="Search term like 'lofi chill'")):
    results = search_youtube(query, total_results=150)
    if not results:
        return {"error": "No results found."}

    first_video_url = results[0]["link"]
    first_metadata = fetch_metadata(first_video_url)

    preview_list = [
        {
            "title": v["title"],
            "duration": v["duration"],
            "id": v["id"],
            "url": v["link"],
            "thumbnail": v["thumbnails"][0]["url"],
            "views": v.get("viewCount", {}).get("short"),
            "published": v.get("publishedTime"),
        }
        for v in results
    ]

    return {"top_result_metadata": first_metadata, "preview_results": preview_list}


@app.get("/debug/cookies")
def debug_cookies():
    return cookies_status()
