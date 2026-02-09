from django.db import models

# Create your models here.

import uuid
from django.db import models
from pgvector.django import VectorField

EMBED_DIM = 384  # for all-MiniLM-L6-v2

class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    profile_embedding = VectorField(dimensions=EMBED_DIM, null=True, blank=True)
    embedding_updated_at = models.DateTimeField(null=True, blank=True)

class Movie(models.Model):
    tmdb_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=300)
    overview = models.TextField(blank=True)
    runtime = models.IntegerField(null=True, blank=True)
    genres_json = models.JSONField(default=list, blank=True)
    poster_url = models.URLField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    embedding = VectorField(dimensions=EMBED_DIM, null=True, blank=True)

class JournalEntry(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tmdb_id = models.IntegerField()
    movie_title = models.CharField(max_length=300)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    embedding = VectorField(dimensions=EMBED_DIM, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["profile", "-created_at"]),
        ]

