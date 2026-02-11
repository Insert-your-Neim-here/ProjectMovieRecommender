from django.urls import path
from . import views

urlpatterns = [
    path("", views.browse, name="browse"),
    path("movie/<int:tmdb_id>/", views.movie_detail, name="movie_detail"),
    path("journals/", views.journals, name="journals"), 
    path("recommendations/", views.recommendations, name="recommendations"),
    path("journals/<int:entry_id>/delete/", views.delete_journal, name="delete_journal"),

]
