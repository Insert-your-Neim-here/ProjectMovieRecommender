# from django.core.management.base import BaseCommand
# from app.services.tmdb_client import popular_movies
# from app.services.movie_ingest import upsert_movie_from_tmdb

# class Command(BaseCommand):
#     help = "Preload and embed popular movies into the database."

#     def add_arguments(self, parser):
#         parser.add_argument("--pages", type=int, default=5)

#     def handle(self, *args, **options):
#         pages = options["pages"]

#         # popular_movies() currently returns page=1 only
#         # quick hack: call movie_ingest on whatever you get for now
#         # (If you want multi-page, we can extend tmdb_client next)
#         count = 0
#         for _ in range(pages):
#             results = popular_movies()  # currently just page 1
#             for m in results:
#                 upsert_movie_from_tmdb(m["id"])
#                 count += 1
#                 self.stdout.write(self.style.SUCCESS(f"Embedded movie {count}: {m['title']}"))

#         self.stdout.write(self.style.SUCCESS(f"Done. Embedded {count} movies."))
from django.core.management.base import BaseCommand
from app.services.tmdb_client import popular_movies
from app.services.movie_ingest import upsert_movie_from_tmdb


class Command(BaseCommand):
    help = "Preload and embed popular movies into the database."

    def add_arguments(self, parser):
        parser.add_argument(
            "--pages",
            type=int,
            default=5,
            help="Number of TMDB popular pages to ingest (20 movies per page)",
        )

    def handle(self, *args, **options):
        # Import here to avoid Django setup issues
        from app.services.movie_ingest import upsert_movie_from_tmdb
        
        pages = options["pages"]
        total = 0

        for p in range(1, pages + 1):
            self.stdout.write(self.style.NOTICE(f"Fetching popular movies page {p}"))
            results = popular_movies(page=p)

            for m in results:
                self.stdout.write(f"Upserting {m['id']} - {m['title']}...")
                upsert_movie_from_tmdb(m["id"])
                total += 1
                self.stdout.write(self.style.SUCCESS(f"Embedded: {m['title']}"))

        self.stdout.write(self.style.SUCCESS(f"Done. Embedded {total} movies."))
