from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from app.services.tmdb_client import popular_movies, search_movies, movie_details

def browse(request):
    q = request.GET.get("q", "").strip()
    if q:
        movies = search_movies(q)
    else:
        movies = popular_movies()
    return render(request, "browse.html", {"movies": movies, "q": q})

# def movie_detail(request, tmdb_id):
#     movie = movie_details(tmdb_id)
#     return render(request, "movie_detail.html", {"movie": movie})

from django.shortcuts import render, redirect
from app.services.tmdb_client import movie_details
from app.services.profile_service import get_or_create_profile
from app.models import JournalEntry

#  def movie_detail(request, tmdb_id: int):
#     profile = get_or_create_profile(request)
#     movie = movie_details(tmdb_id)

#     if request.method == "POST":
#         text = request.POST.get("text", "").strip()
#         if text:
#             JournalEntry.objects.create(
#                 profile=profile,
#                 tmdb_id=tmdb_id,
#                 movie_title=movie.get("title", ""),
#                 text=text,
#             )
#         return redirect("journals")

#     return render(request, "movie_detail.html", {"movie": movie})
from django.shortcuts import render, redirect
from app.models import JournalEntry
from app.services.profile_service import get_or_create_profile
from app.services.tmdb_client import movie_details
from app.services.embedding_service import embed_text
from app.services.movie_ingest import upsert_movie_from_tmdb

def movie_detail(request, tmdb_id: int):
    profile = get_or_create_profile(request)
    movie = movie_details(tmdb_id)

    # Ensure movie exists in DB + embedded (helps recs later)
    upsert_movie_from_tmdb(tmdb_id)

    if request.method == "POST":
        text = request.POST.get("text", "").strip()
        if text:
            JournalEntry.objects.create(
                profile=profile,
                tmdb_id=tmdb_id,
                movie_title=movie.get("title", ""),
                text=text,
                embedding=embed_text(text),
            )
        return redirect("journals")

    return render(request, "movie_detail.html", {"movie": movie})


from app.models import JournalEntry
from app.services.profile_service import get_or_create_profile

def journals(request):
    profile = get_or_create_profile(request)
    entries = JournalEntry.objects.filter(profile=profile).order_by("-created_at")
    return render(request, "journals.html", {"entries": entries})


from app.services.profile_service import get_or_create_profile
from app.models import JournalEntry
from app.services.tmdb_client import movie_details
import random

# def recommendations(request):
#     profile = get_or_create_profile(request)
#     entries = list(JournalEntry.objects.filter(profile=profile).order_by("-created_at"))

#     if not entries:
#         return render(request, "recommendations.html", {"recs": [], "message": "Write a journal entry first."})

#     # Take the most recent movie and ask TMDB for similar movies
#     seed_tmdb_id = entries[0].tmdb_id

#     # TMDB has /movie/{id}/similar — add this function in tmdb_client.py
#     from app.services.tmdb_client import similar_movies
#     candidates = similar_movies(seed_tmdb_id)

#     # pick 3 random for now (works immediately)
#     recs = random.sample(candidates, k=min(3, len(candidates)))

#     return render(request, "recommendations.html", {"recs": recs, "message": ""})

from django.shortcuts import render
from app.services.profile_service import get_or_create_profile
from app.services.recommender import recommend

def recommendations(request):
    profile = get_or_create_profile(request)

    max_runtime = request.GET.get("max_runtime")
    max_runtime = int(max_runtime) if max_runtime and max_runtime.isdigit() else None

    picked, explanations = recommend(profile, k=3, max_runtime=max_runtime)

    return render(request, "recommendations.html", {
        "picked": picked,
        "explanations": explanations,
        "max_runtime": max_runtime or "",
    })
from django.shortcuts import redirect, get_object_or_404
from app.models import JournalEntry
from app.services.profile_service import get_or_create_profile

def delete_journal(request, entry_id: int):
    profile = get_or_create_profile(request)

    entry = get_object_or_404(JournalEntry, id=entry_id, profile=profile)

    if request.method == "POST":
        entry.delete()
        return redirect("journals")

    # Simple confirmation page
    return render(request, "confirm_delete.html", {"entry": entry})

