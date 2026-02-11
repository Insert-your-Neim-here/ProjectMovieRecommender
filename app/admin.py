from django.contrib import admin

# Register your models here.
from django.contrib import admin
from app.models import Movie, JournalEntry, Profile

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("tmdb_id", "title", "runtime", "updated_at")
    search_fields = ("title",)

@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ("movie_title", "profile", "created_at")
    search_fields = ("movie_title", "text")
    list_filter = ("created_at",)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at")
