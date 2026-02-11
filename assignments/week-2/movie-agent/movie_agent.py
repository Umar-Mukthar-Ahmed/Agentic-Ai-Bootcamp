import json
from pathlib import Path
import requests
from typing import List, Dict, Optional


class MovieAgent:
    """Movie management system with local storage and external API integration"""

    GHIBLI_API_URL = "https://ghibliapi.vercel.app/films"
    OMDB_API_URL = "http://www.omdbapi.com/"

    def __init__(self, data_path: str = "data/movies.json", omdb_api_key: Optional[str] = None,
                 use_session_state: bool = False, session_movies: Optional[List[Dict]] = None):
        self.data_path = Path(data_path)
        self.omdb_api_key = omdb_api_key
        self.use_session_state = use_session_state

        if use_session_state and session_movies is not None:
            # Use provided session state movies
            self.movies = session_movies
        else:
            # Use file-based storage (for CLI)
            self._ensure_data_directory()
            self.movies = self.load_movies()

    def _ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        self.data_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.data_path.exists():
            self.data_path.write_text("[]")

    def load_movies(self) -> List[Dict]:
        """Load movies from JSON file"""
        try:
            with open(self.data_path, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save_movies(self):
        """Save movies to JSON file (only if not using session state)"""
        if not self.use_session_state:
            with open(self.data_path, "w") as file:
                json.dump(self.movies, file, indent=2)

    def add_movie(self, title: str, genre: str, rating: float, year: int, watched: bool = False) -> Dict:
        """Add a new movie to the collection"""
        movie = {
            "title": title,
            "genre": genre,
            "rating": float(rating),
            "year": int(year),
            "watched": watched
        }
        self.movies.append(movie)
        self.save_movies()
        return movie

    def list_movies(self) -> List[Dict]:
        """Get all movies"""
        return self.movies

    def search_by_title(self, title: str) -> List[Dict]:
        """Search movies by title (partial match)"""
        return [
            movie for movie in self.movies
            if title.lower() in movie["title"].lower()
        ]

    def search_by_genre(self, genre: str) -> List[Dict]:
        """Search movies by genre"""
        return [
            movie for movie in self.movies
            if movie["genre"].lower() == genre.lower()
        ]

    def recommend(self, min_rating: float = 8.0) -> List[Dict]:
        """Get recommended movies above minimum rating"""
        return [
            movie for movie in self.movies
            if movie["rating"] >= min_rating
        ]

    def mark_as_watched(self, title: str) -> bool:
        """Mark a movie as watched"""
        for movie in self.movies:
            if movie["title"].lower() == title.lower():
                movie["watched"] = True
                self.save_movies()
                return True
        return False

    def delete_movie(self, title: str) -> bool:
        """Delete a movie by title"""
        original_length = len(self.movies)
        self.movies = [
            movie for movie in self.movies
            if movie["title"].lower() != title.lower()
        ]
        if len(self.movies) < original_length:
            self.save_movies()
            return True
        return False

    def get_all_genres(self) -> List[str]:
        """Get unique list of all genres"""
        genres = set(movie["genre"] for movie in self.movies)
        return sorted(list(genres))

    # External API methods

    def fetch_ghibli_movie(self, title: str) -> Optional[Dict]:
        """Fetch movie details from Studio Ghibli API"""
        try:
            response = requests.get(self.GHIBLI_API_URL, timeout=10)
            if response.status_code != 200:
                return None

            movies = response.json()
            for movie in movies:
                if movie["title"].lower() == title.lower():
                    return {
                        "title": movie["title"],
                        "genre": "Animation",
                        "rating": float(movie["rt_score"]) / 10,
                        "year": int(movie["release_date"]),
                        "watched": False,
                        "description": movie.get("description", ""),
                        "director": movie.get("director", ""),
                        "source": "Studio Ghibli"
                    }
            return None
        except requests.RequestException:
            return None

    def fetch_omdb_movie(self, title: str) -> Optional[Dict]:
        """Fetch movie details from OMDB API"""
        if not self.omdb_api_key:
            return None

        try:
            params = {
                "t": title,
                "apikey": self.omdb_api_key
            }
            response = requests.get(self.OMDB_API_URL, params=params, timeout=10)
            data = response.json()

            if data.get("Response") == "True":
                # Convert IMDB rating to our scale (0-10)
                imdb_rating = data.get("imdbRating", "N/A")
                rating = float(imdb_rating) if imdb_rating != "N/A" else 7.0

                return {
                    "title": data.get("Title", title),
                    "genre": data.get("Genre", "Unknown").split(",")[0].strip(),
                    "rating": rating,
                    "year": int(data.get("Year", "2000")[:4]),
                    "watched": False,
                    "description": data.get("Plot", ""),
                    "director": data.get("Director", ""),
                    "source": "OMDB"
                }
            return None
        except (requests.RequestException, ValueError):
            return None

    def fetch_movie_from_api(self, title: str) -> Optional[Dict]:
        """Try to fetch movie from available APIs (Ghibli first, then OMDB)"""
        # Try Ghibli first
        movie = self.fetch_ghibli_movie(title)
        if movie:
            return movie

        # Try OMDB if available
        movie = self.fetch_omdb_movie(title)
        if movie:
            return movie

        return None

    def add_movie_from_api(self, title: str) -> Optional[Dict]:
        """Fetch movie from API and add to collection"""
        movie_data = self.fetch_movie_from_api(title)
        if movie_data:
            # Remove extra fields before adding
            clean_data = {
                "title": movie_data["title"],
                "genre": movie_data["genre"],
                "rating": movie_data["rating"],
                "year": movie_data["year"],
                "watched": movie_data["watched"]
            }
            self.movies.append(clean_data)
            self.save_movies()
            return movie_data
        return None

    def get_statistics(self) -> Dict:
        """Get collection statistics"""
        if not self.movies:
            return {
                "total": 0,
                "watched": 0,
                "unwatched": 0,
                "avg_rating": 0,
                "genres": 0
            }

        total = len(self.movies)
        watched = sum(1 for m in self.movies if m["watched"])
        avg_rating = sum(m["rating"] for m in self.movies) / total if total > 0 else 0

        return {
            "total": total,
            "watched": watched,
            "unwatched": total - watched,
            "avg_rating": round(avg_rating, 2),
            "genres": len(self.get_all_genres())
        }