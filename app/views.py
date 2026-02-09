from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from app.services.tmdb_client import popular_movies, search_movies

def browse(request):
    q = request.GET.get("q", "").strip()
    if q:
        movies = search_movies(q)
    else:
        movies = popular_movies()
    return render(request, "browse.html", {"movies": movies, "q": q})
