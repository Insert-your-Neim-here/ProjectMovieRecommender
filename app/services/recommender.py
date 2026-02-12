import math
from datetime import datetime, timezone
from app.models import JournalEntry, Movie
from pgvector.django import CosineDistance


def build_profile_vector(entries):
    if not entries:
        return None
    now = datetime.now(timezone.utc)
    weighted = None
    total_w = 0.0

    for e in entries:
        if e.embedding is None:
            continue
        age_days = (now - e.created_at).total_seconds() / (3600 * 24)
        w = math.exp(-age_days / 30.0)  # recency weighting
        total_w += w
        vec = e.embedding

        if weighted is None:
            weighted = [w * x for x in vec]
        else:
            for i in range(len(vec)):
                weighted[i] += w * vec[i]

    if not weighted or total_w == 0:
        return None
    return [x / total_w for x in weighted]

def recommend(profile, k=3, max_runtime=None):
    entries = list(
        JournalEntry.objects
        .filter(profile=profile)
        .exclude(embedding=None)
        .order_by("-created_at")[:50]
    )
    profile_vec = build_profile_vector(entries)
    if not profile_vec:
        return [], {}

    already = {e.tmdb_id for e in entries}

    # Candidate retrieval: nearest movies in vector space
    qs = Movie.objects.exclude(embedding=None)

    # Exclude watched/journaled movies
    qs = qs.exclude(tmdb_id__in=already)

    # Runtime filter
    if max_runtime:
        qs = qs.filter(runtime__isnull=False, runtime__lte=max_runtime)

    # Order by cosine distance (pgvector)
    candidates = list(qs.order_by(CosineDistance('embedding', profile_vec))[:200])

    # Score + pick diverse top 3 (simple genre diversity)
    scored = []
    for m in candidates:
        # embeddings are normalized, so dot product ~ cosine similarity
        score = sum(a*b for a, b in zip(profile_vec, m.embedding))
        scored.append((m, score))
    scored.sort(key=lambda x: x[1], reverse=True)

    picked = []
    used_primary = set()
    for m, s in scored:
        primary = (m.genres_json[0]["name"] if m.genres_json else None)
        if primary and primary in used_primary and len(picked) < k:
            continue
        picked.append((m, s))
        if primary:
            used_primary.add(primary)
        if len(picked) == k:
            break

    # Explanations: link to most similar journal entry
    explanations = {}
    for m, _ in picked:
        best = None
        best_sim = -1.0
        for e in entries:
            sim = sum(a*b for a, b in zip(e.embedding, m.embedding))
            if sim > best_sim:
                best_sim = sim
                best = e
        explanations[m.tmdb_id] = {
            "because": f"Closest to what you wrote about '{best.movie_title}'" if best else "Matches your journal themes",
            "evidence": (best.text[:140] + "...") if best and len(best.text) > 140 else (best.text if best else ""),
        }

    return picked, explanations
