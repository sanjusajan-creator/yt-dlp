from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
from ytmusicapi import YTMusic
from app.utils.audio_extractor import get_audio_url
import httpx
import asyncio

router = APIRouter()
ytmusic = YTMusic()


@router.get("/hits")
def get_daily_hits():
    charts = ytmusic.get_charts()
    songs = charts.get("tracks", [])
    return [
        {
            "title": song["title"],
            "videoId": song["videoId"],
            "artists": [a["name"] for a in song["artists"]],
            "thumbnails": song["thumbnails"],
            "url": f"https://www.youtube.com/watch?v={song['videoId']}",
        }
        for song in songs[:200]
    ]


@router.get("/explore")
def explore_genre(
    genre: str = Query(..., description="Search genre like pop, sufi, etc"),
):
    search_results = ytmusic.search(genre, filter="songs")
    return [
        {
            "title": song["title"],
            "videoId": song.get("videoId"),
            "artists": [a["name"] for a in song.get("artists", [])],
            "thumbnails": song.get("thumbnails"),
            "url": f"https://www.youtube.com/watch?v={song['videoId']}",
        }
        for song in search_results[:200]
    ]


@router.get("/audio")
def fetch_audio_url(video_id: str = Query(..., description="YouTube video ID")):
    try:
        audio_url = get_audio_url(video_id)
        return {"audio_url": audio_url}
    except Exception as e:
        return {"error": f"Failed to extract audio URL: {str(e)}"}


@router.get("/audio/stream")
async def stream_audio(video_id: str = Query(..., description="YouTube video ID")):
    """Proxy audio through the server to bypass YouTube IP restrictions."""
    try:
        audio_url = get_audio_url(video_id)
    except Exception as e:
        return {"error": f"Failed to extract audio URL: {str(e)}"}

    async def iter_audio():
        async with httpx.AsyncClient(timeout=60) as client:
            async with client.stream("GET", audio_url) as resp:
                async for chunk in resp.aiter_bytes(chunk_size=65536):
                    yield chunk

    return StreamingResponse(
        iter_audio(),
        media_type="audio/webm",
        headers={"Content-Disposition": f'inline; filename="{video_id}.webm"'},
    )
