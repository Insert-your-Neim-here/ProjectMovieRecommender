import os
import requests

TMDB_API_BASE = "https://api.themoviedb.org/3"
TMDB_TOKEN = os.environ.get("TMDB_TOKEN")

def _headers():
    return {
        "Authorization": f"Bearer {TMDB_TOKEN}",
        "Content-Type": "application/json;charset=utf-8",
    }

def search_movies(query: str):
    r = requests.get(
        f"{TMDB_API_BASE}/search/movie",
        headers=_headers(),
        params={"query": query, "include_adult": "false"},
        timeout=10,
    )
    r.raise_for_status()
    return r.json()["results"]

def popular_movies():
    r = requests.get(
        f"{TMDB_API_BASE}/movie/popular",
        headers=_headers(),
        params={"page": 1},
        timeout=10,
    )
    r.raise_for_status()
    return r.json()["results"]

def movie_details(tmdb_id: int):
    r = requests.get(
        f"{TMDB_API_BASE}/movie/{tmdb_id}",
        headers=_headers(),
        params={"append_to_response": "keywords"},
        timeout=10,
    )
    r.raise_for_status()
    return r.json()
