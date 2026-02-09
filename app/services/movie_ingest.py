from app.models import Movie
from app.services.tmdb_client import movie_details

def upsert_movie_from_tmdb(tmdb_id: int) -> Movie:
    tmdb = movie_details(tmdb_id)
    poster_path = tmdb.get("poster_path") or ""
    poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else ""

    movie, _ = Movie.objects.update_or_create(
        tmdb_id=tmdb_id,
        defaults={
            "title": tmdb.get("title", ""),
            "overview": tmdb.get("overview", "") or "",
            "runtime": tmdb.get("runtime"),
            "genres_json": tmdb.get("genres", []),
            "poster_url": poster_url,
        },
    )
    return movie
