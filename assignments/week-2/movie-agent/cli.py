#!/usr/bin/env python3
"""
Movie Agent CLI - Command-line interface for movie management
"""

from movie_agent import MovieAgent
import os
from pathlib import Path


def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_movie(movie, index=None):
    """Print a single movie in a formatted way"""
    prefix = f"{index}. " if index else "  "
    status = "✓ Watched" if movie["watched"] else "○ Not watched"
    print(f"{prefix}{movie['title']} ({movie['year']})")
    print(f"   Genre: {movie['genre']} | Rating: {movie['rating']}/10 | {status}")


def print_movies(movies, title="Movies"):
    """Print a list of movies"""
    if not movies:
        print("\n  No movies found.")
        return

    print(f"\n  {title} ({len(movies)} total):")
    print("-" * 60)
    for i, movie in enumerate(movies, 1):
        print_movie(movie, i)


def add_movie_menu(agent):
    """Menu for adding a movie"""
    print_header("Add New Movie")

    choice = input("\n  1. Add manually\n  2. Search from API\n\n  Choose option (1-2): ").strip()

    if choice == "1":
        # Manual entry
        title = input("\n  Movie title: ").strip()
        genre = input("  Genre: ").strip()
        rating = float(input("  Rating (0-10): ").strip())
        year = int(input("  Year: ").strip())
        watched = input("  Watched? (y/n): ").strip().lower() == 'y'

        agent.add_movie(title, genre, rating, year, watched)
        print(f"\n  ✓ '{title}' added successfully!")

    elif choice == "2":
        # API search
        title = input("\n  Enter movie title to search: ").strip()
        print("\n  Searching...")

        movie_data = agent.fetch_movie_from_api(title)

        if movie_data:
            print("\n  Movie found!")
            print(f"  Title: {movie_data['title']}")
            print(f"  Genre: {movie_data['genre']}")
            print(f"  Rating: {movie_data['rating']}/10")
            print(f"  Year: {movie_data['year']}")
            if movie_data.get('description'):
                print(f"  Description: {movie_data['description'][:100]}...")
            print(f"  Source: {movie_data.get('source', 'API')}")

            confirm = input("\n  Add this movie? (y/n): ").strip().lower()
            if confirm == 'y':
                result = agent.add_movie_from_api(title)
                if result:
                    print(f"\n  ✓ '{movie_data['title']}' added successfully!")
        else:
            print("\n  ✗ Movie not found in API. Try manual entry.")


def search_menu(agent):
    """Menu for searching movies"""
    print_header("Search Movies")

    choice = input(
        "\n  1. Search by title\n  2. Search by genre\n  3. Get recommendations (rating >= 8)\n\n  Choose option (1-3): ").strip()

    if choice == "1":
        title = input("\n  Enter title to search: ").strip()
        results = agent.search_by_title(title)
        print_movies(results, f"Search results for '{title}'")

    elif choice == "2":
        genres = agent.get_all_genres()
        if genres:
            print("\n  Available genres:", ", ".join(genres))
        genre = input("\n  Enter genre: ").strip()
        results = agent.search_by_genre(genre)
        print_movies(results, f"Movies in '{genre}' genre")

    elif choice == "3":
        min_rating = input("\n  Minimum rating (default 8.0): ").strip()
        min_rating = float(min_rating) if min_rating else 8.0
        results = agent.recommend(min_rating)
        print_movies(results, f"Recommended movies (rating >= {min_rating})")


def manage_movies_menu(agent):
    """Menu for managing movies"""
    print_header("Manage Movies")

    choice = input("\n  1. Mark movie as watched\n  2. Delete movie\n\n  Choose option (1-2): ").strip()

    if choice == "1":
        title = input("\n  Enter movie title: ").strip()
        if agent.mark_as_watched(title):
            print(f"\n  ✓ '{title}' marked as watched!")
        else:
            print(f"\n  ✗ Movie '{title}' not found.")

    elif choice == "2":
        title = input("\n  Enter movie title to delete: ").strip()
        confirm = input(f"  Are you sure you want to delete '{title}'? (y/n): ").strip().lower()
        if confirm == 'y':
            if agent.delete_movie(title):
                print(f"\n  ✓ '{title}' deleted successfully!")
            else:
                print(f"\n  ✗ Movie '{title}' not found.")


def show_statistics(agent):
    """Display collection statistics"""
    print_header("Collection Statistics")

    stats = agent.get_statistics()

    print(f"\n  Total Movies: {stats['total']}")
    print(f"  Watched: {stats['watched']}")
    print(f"  Not Watched: {stats['unwatched']}")
    print(f"  Average Rating: {stats['avg_rating']}/10")
    print(f"  Different Genres: {stats['genres']}")


def main():
    """Main CLI loop"""
    # Load OMDB API key from environment if available
    omdb_key = os.getenv("OMDB_API_KEY")

    # Initialize agent
    agent = MovieAgent(omdb_api_key=omdb_key)

    print_header("🎬 Movie Agent CLI")
    print("\n  Welcome to Movie Agent!")
    if omdb_key:
        print("  OMDB API: Enabled")
    else:
        print("  OMDB API: Not configured (only Ghibli API available)")

    while True:
        print("\n" + "-" * 60)
        print("\n  MENU:")
        print("  1. View all movies")
        print("  2. Add movie")
        print("  3. Search movies")
        print("  4. Manage movies")
        print("  5. View statistics")
        print("  6. Exit")

        choice = input("\n  Choose option (1-6): ").strip()

        if choice == "1":
            movies = agent.list_movies()
            print_movies(movies, "All Movies")

        elif choice == "2":
            add_movie_menu(agent)

        elif choice == "3":
            search_menu(agent)

        elif choice == "4":
            manage_movies_menu(agent)

        elif choice == "5":
            show_statistics(agent)

        elif choice == "6":
            print("\n  Goodbye! 👋\n")
            break

        else:
            print("\n  Invalid option. Please try again.")


if __name__ == "__main__":
    main()