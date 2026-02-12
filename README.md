# ProjectMovieRecommender
Django-based movie recommendation system that generates personalized movie suggestions based on users' journal entries.

Instead of relying on ratings, this system uses natural language processing and semantic embeddings to understand what users liked about previously watched movies and recommends similar ones.

Features:
Browse movies (fetched from TMDB API)
Write journal entries about watched movies
Delete journal entries
Semantic recommendation engine using embeddings
Vector similarity search using PostgreSQL + pgvector
Admin panel for database inspection
Dockerized PostgreSQL setup

How Recommendations Work:
User writes journal entries about movies.
Each journal entry is converted into a vector embedding using:
sentence-transformers/all-MiniLM-L6-v2
Movie overviews are also embedded.
A user profile vector is built from recent journal entries.
PostgreSQL + pgvector performs cosine similarity search.
Top similar movies (excluding already watched ones) are returned.
The system explains recommendations by showing the most similar journal entry.

1. Clone Repository
git clone https://github.com/Insert-your-Neim-here/ProjectMovieRecommender
cd ProjectMovieRecommender

2. Create Virtual Environment
python -m venv .venv
.venv\Scripts\activate

3. Install Dependencies
pip install -r requirements.txt

it will take a couple of minutes

4. Create Environment File
Create a .env file in the project root using the template below:

SECRET_KEY=your-secret-key
TMDB_TOKEN=your-tmdb-token

you can use my TMDB Token: eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4NDI0ODcwODkwYjUzZmZhODliM2EyMGM2MGZiMzdjYyIsIm5iZiI6MTc2OTI3MzYyMC4yODYsInN1YiI6IjY5NzRmOTE0NDgzNzQ2N2Q2YzEwNWQyYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.AKIulT3iyo0jz_NLnLr2vc-zFcDZZNygL6mwuAaAeJ0

DB_NAME=moviejournal
DB_USER=mj
DB_PASSWORD=mj
DB_HOST=127.0.0.1
DB_PORT=5432

5. Start PostgreSQL (Docker Required)
Make sure Docker is installed and running.
Start database:

docker compose up -d

This creates:
Database: moviejournal
User: mj
Password: mj

6. Enable pgvector Extension
docker exec -it projectmovierecommender-db-1 bash
psql -U mj -d moviejournal
CREATE EXTENSION IF NOT EXISTS vector;
\q
exit

7. Run Migrations
python manage.py migrate

8. Run Development Server
python manage.py runserver

CTRL+C to stop the server

9. Preloading Movie Data
python manage.py preload_movies --pages 10

going to take a couple of minutes, possibility to lower the number of pages if wanted