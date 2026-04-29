<div align="center">
  <h1>🎵 YouTube Search API</h1>
  <p>A fast and lightweight REST API to search YouTube, extract audio streams, fetch daily hits, and explore music genres—built with <b>FastAPI</b>, <b>yt-dlp</b>, and <b>ytmusicapi</b>.</p>
</div>

---

## 📖 Overview

The **YouTube Search API** is a high-performance backend application designed for music apps, discord bots, or any platform that needs to interface with YouTube and YouTube Music. It provides endpoints to search for songs, fetch comprehensive metadata, extract direct audio streaming URLs, and browse daily charts and genres.

## ✨ Features

- 🔍 **Powerful Search:** Search for songs, videos, or keywords and return up to 150 results instantly.
- 🎧 **Audio Stream Extraction:** Get direct audio URLs from any YouTube video ID (useful for playing in audio players or Discord bots).
- 📈 **Daily Hits:** Fetch the top daily hits straight from YouTube Music charts.
- 🎸 **Genre Exploration:** Browse tracks by genre (e.g., Pop, Sufi, Lo-Fi, etc.).
- 📊 **Rich Metadata:** Extracts detailed metadata like view counts, likes, thumbnails, duration, and uploader information.

## 🛠️ Technology Stack

- **Framework:** [FastAPI](https://fastapi.tiangolo.com/) - High performance, easy to use, and automatic interactive API documentation.
- **Server:** [Uvicorn](https://www.uvicorn.org/) - ASGI web server implementation for Python.
- **Core Libraries:**
  - `yt-dlp`: For extracting audio URLs and deep video metadata.
  - `youtube-search-python`: For blazing-fast YouTube search results without official API limits.
  - `ytmusicapi`: For accessing YouTube Music charts and genre exploration.

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/YouTubesearch-main.git
   cd YouTubesearch-main
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the server:**
   ```bash
   uvicorn app.main:app --reload
   ```

The API will now be running at `http://127.0.0.1:8000`.

## 📡 API Endpoints

Once running, you can view the interactive Swagger documentation at `http://127.0.0.1:8000/docs`.

| Endpoint | Method | Description | Parameters |
| :--- | :---: | :--- | :--- |
| `/search` | `GET` | Searches for songs and returns video previews + metadata for the top result. | `query` (string) - Search term |
| `/hits` | `GET` | Returns up to 200 daily hits from YouTube Music charts. | None |
| `/explore` | `GET` | Explores a specific music genre. | `genre` (string) - Genre name |
| `/audio` | `GET` | Extracts the direct audio streaming URL. | `video_id` (string) - YouTube Video ID |

## 📁 Project Structure

```
YouTubesearch-main/
├── app/
│   ├── api/
│   │   └── explore.py             # Routes for /hits, /explore, /audio
│   ├── utils/
│   │   ├── audio_extractor.py     # Logic to extract audio streams via yt-dlp
│   │   └── search_and_metadata.py # Logic for YouTube search and metadata fetching
│   └── main.py                    # FastAPI application setup and /search route
├── requirements.txt               # Project dependencies
└── README.md                      # Project documentation
```

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/yourusername/YouTubesearch-main/issues) if you want to contribute.

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.
