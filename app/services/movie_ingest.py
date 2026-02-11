# from app.models import Movie
# from app.services.tmdb_client import movie_details

# def upsert_movie_from_tmdb(tmdb_id: int) -> Movie:
#     tmdb = movie_details(tmdb_id)
#     poster_path = tmdb.get("poster_path") or ""
#     poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else ""

#     movie, _ = Movie.objects.update_or_create(
#         tmdb_id=tmdb_id,
#         defaults={
#             "title": tmdb.get("title", ""),
#             "overview": tmdb.get("overview", "") or "",
#             "runtime": tmdb.get("runtime"),
#             "genres_json": tmdb.get("genres", []),
#             "poster_url": poster_url,
#         },
#     )
#     return movie

from app.models import Movie
from app.services.tmdb_client import movie_details
from app.services.embedding_service import embed_text

def build_movie_doc(tmdb: dict) -> str:
    title = tmdb.get("title", "")
    overview = tmdb.get("overview", "") or ""
    genres = ", ".join([g["name"] for g in tmdb.get("genres", [])])

    # keywords may be present depending on your append_to_response
    kws = []
    kw_block = tmdb.get("keywords")
    if isinstance(kw_block, dict):
        kws = [k["name"] for k in kw_block.get("keywords", [])][:20]
    keywords = ", ".join(kws)

    return f"Title: {title}\nGenres: {genres}\nKeywords: {keywords}\nOverview: {overview}"

def upsert_movie_from_tmdb(tmdb_id: int) -> Movie:
    tmdb = movie_details(tmdb_id)
    poster_path = tmdb.get("poster_path") or ""
    poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else ""

    doc = build_movie_doc(tmdb)
    vec = embed_text(doc)

    movie, _ = Movie.objects.update_or_create(
        tmdb_id=tmdb_id,
        defaults={
            "title": tmdb.get("title", ""),
            "overview": tmdb.get("overview", "") or "",
            "runtime": tmdb.get("runtime"),
            "genres_json": tmdb.get("genres", []),
            "poster_url": poster_url,
            "embedding": vec,
        },
    )
    return movie

