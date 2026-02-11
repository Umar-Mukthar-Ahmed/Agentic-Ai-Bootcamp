"""
Library Agent Module
Contains the core LibraryAgent class for managing books.
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import requests


class LibraryAgent:
    """
    Library Agent class for managing a book collection.

    Attributes:
        storage_path (Path): Path to the JSON storage file
        books (List[Dict]): List of book dictionaries
        logger (Logger): Logger instance for this agent
    """

    def __init__(self, storage_path: str = "data/books.json"):
        """
        Initialize the LibraryAgent.

        Args:
            storage_path (str): Path to JSON storage file
        """
        self.storage_path = Path(storage_path)
        self.logger = self._setup_logger()
        self.books = self.load_books()
        self.logger.info("LibraryAgent initialized with %d books", len(self.books))

    @staticmethod
    def _setup_logger() -> logging.Logger:
        """
        Set up logger for the LibraryAgent.

        Returns:
            logging.Logger: Configured logger instance
        """
        logger = logging.getLogger('LibraryAgent')
        logger.setLevel(logging.INFO)

        # Create logs directory if it doesn't exist
        Path('logs').mkdir(exist_ok=True)

        # File handler
        file_handler = logging.FileHandler('logs/library.log')
        file_handler.setLevel(logging.INFO)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)

        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers if not already added
        if not logger.handlers:
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)

        return logger

    def load_books(self) -> List[Dict]:
        """
        Load books from JSON storage.

        Returns:
            List[Dict]: List of book dictionaries
        """
        try:
            if self.storage_path.exists():
                with open(self.storage_path, 'r', encoding='utf-8') as file:
                    books = json.load(file)
                    self.logger.info("Loaded %d books from storage", len(books))
                    return books
            self.logger.info("No existing storage found. Starting with empty library")
            return []
        except json.JSONDecodeError as error:
            self.logger.error("JSON decode error: %s", error)
            print("⚠️  Warning: Storage file corrupted. Starting fresh.")
            return []
        except Exception as error:
            self.logger.error("Error loading books: %s", error)
            return []

    def save_books(self) -> bool:
        """
        Save books to JSON storage.

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.storage_path, 'w', encoding='utf-8') as file:
                json.dump(self.books, file, indent=2, ensure_ascii=False)
            self.logger.info("Saved %d books to storage", len(self.books))
            return True
        except Exception as error:
            self.logger.error("Error saving books: %s", error)
            print(f"❌ Error saving books: {error}")
            return False

    def add_book(
            self,
            title: str,
            author: str,
            genre: str = "Unknown",
            year: Optional[int] = None,
            isbn: Optional[str] = None
    ) -> Dict:
        """
        Add a new book to the library.

        Args:
            title (str): Book title
            author (str): Author name
            genre (str): Book genre
            year (int, optional): Publication year
            isbn (str, optional): ISBN number

        Returns:
            Dict: The newly added book dictionary
        """
        book = {
            "id": self._generate_book_id(),
            "title": title.strip(),
            "author": author.strip(),
            "genre": genre.strip(),
            "year": year,
            "isbn": isbn,
            "rating": None,
            "status": "unread",
            "added_date": datetime.now().strftime("%Y-%m-%d"),
            "notes": ""
        }

        self.books.append(book)
        self.save_books()
        self.logger.info("Added book: '%s' by %s", title, author)
        print(f"✅ Added: '{title}' by {author}")
        return book

    def _generate_book_id(self) -> int:
        """
        Generate a unique book ID.

        Returns:
            int: New unique book ID
        """
        if not self.books:
            return 1
        return max(book['id'] for book in self.books) + 1

    def get_book_by_id(self, book_id: int) -> Optional[Dict]:
        """
        Get a book by its ID.

        Args:
            book_id (int): Book ID

        Returns:
            Optional[Dict]: Book dictionary or None if not found
        """
        for book in self.books:
            if book['id'] == book_id:
                return book
        return None

    def list_books(self, filter_by: str = "all") -> List[Dict]:
        """
        List books with optional filtering.

        Args:
            filter_by (str): Filter type ('all', 'read', 'reading', 'unread')

        Returns:
            List[Dict]: Filtered list of books
        """
        if filter_by == "all":
            return self.books
        filtered = [book for book in self.books if book.get("status") == filter_by]
        self.logger.info("Listed %d books with filter: %s", len(filtered), filter_by)
        return filtered

    def search_books(self, query: str, search_by: str = "title") -> List[Dict]:
        """
        Search books by field.

        Args:
            query (str): Search query
            search_by (str): Field to search ('title', 'author', 'genre')

        Returns:
            List[Dict]: List of matching books
        """
        query_lower = query.lower().strip()
        results = [
            book for book in self.books
            if query_lower in str(book.get(search_by, "")).lower()
        ]
        self.logger.info(
            "Search '%s' in %s returned %d results",
            query, search_by, len(results)
        )
        return results

    def update_status(self, book_id: int, status: str) -> bool:
        """
        Update the reading status of a book.

        Args:
            book_id (int): Book ID
            status (str): New status ('unread', 'reading', 'read')

        Returns:
            bool: True if successful, False otherwise
        """
        book = self.get_book_by_id(book_id)
        if book:
            old_status = book['status']
            book['status'] = status
            self.save_books()
            self.logger.info(
                "Updated book ID %d status: %s -> %s",
                book_id, old_status, status
            )
            print(f"✅ Updated '{book['title']}' status to: {status}")
            return True

        self.logger.warning("Book ID %d not found for status update", book_id)
        print(f"❌ Book ID {book_id} not found")
        return False

    def rate_book(self, book_id: int, rating: float) -> bool:
        """
        Rate a book.

        Args:
            book_id (int): Book ID
            rating (float): Rating value (0-5)

        Returns:
            bool: True if successful, False otherwise
        """
        if not 0 <= rating <= 5:
            self.logger.warning("Invalid rating attempted: %f", rating)
            print("❌ Rating must be between 0 and 5")
            return False

        book = self.get_book_by_id(book_id)
        if book:
            book['rating'] = rating
            self.save_books()
            self.logger.info("Rated book ID %d: %f stars", book_id, rating)
            print(f"✅ Rated '{book['title']}': {rating}⭐")
            return True

        self.logger.warning("Book ID %d not found for rating", book_id)
        print(f"❌ Book ID {book_id} not found")
        return False

    def get_recommendations(
            self,
            genre: Optional[str] = None,
            min_rating: float = 4.0
    ) -> List[Dict]:
        """
        Get book recommendations.

        Args:
            genre (str, optional): Filter by genre
            min_rating (float): Minimum rating threshold

        Returns:
            List[Dict]: List of recommended books
        """
        recommendations = [
            book for book in self.books
            if book.get("rating") and book["rating"] >= min_rating
               and (genre is None or book["genre"].lower() == genre.lower())
        ]

        recommendations.sort(key=lambda x: x.get("rating", 0), reverse=True)
        self.logger.info(
            "Generated %d recommendations (genre: %s, min_rating: %f)",
            len(recommendations), genre, min_rating
        )
        return recommendations

    def organize_by_genre(self) -> Dict[str, List[Dict]]:
        """
        Organize books by genre.

        Returns:
            Dict[str, List[Dict]]: Dictionary with genres as keys
        """
        organized = {}
        for book in self.books:
            genre = book.get("genre", "Unknown")
            if genre not in organized:
                organized[genre] = []
            organized[genre].append(book)

        self.logger.info("Organized books into %d genres", len(organized))
        return organized

    def organize_by_author(self) -> Dict[str, List[Dict]]:
        """
        Organize books by author.

        Returns:
            Dict[str, List[Dict]]: Dictionary with authors as keys
        """
        organized = {}
        for book in self.books:
            author = book.get("author", "Unknown")
            if author not in organized:
                organized[author] = []
            organized[author].append(book)

        self.logger.info("Organized books by %d authors", len(organized))
        return organized

    def get_statistics(self) -> Dict:
        """
        Get library statistics.

        Returns:
            Dict: Dictionary containing statistics
        """
        total = len(self.books)
        read = sum(1 for book in self.books if book.get("status") == "read")
        reading = sum(1 for book in self.books if book.get("status") == "reading")
        unread = sum(1 for book in self.books if book.get("status") == "unread")

        rated_books = [book for book in self.books if book.get("rating")]
        avg_rating = (
            sum(book["rating"] for book in rated_books) / len(rated_books)
            if rated_books else 0
        )

        genres = {book.get("genre", "Unknown") for book in self.books}
        authors = {book.get("author", "Unknown") for book in self.books}

        return {
            "total_books": total,
            "read": read,
            "reading": reading,
            "unread": unread,
            "average_rating": round(avg_rating, 2),
            "unique_genres": len(genres),
            "unique_authors": len(authors)
        }

    def fetch_book_details(self, isbn: str) -> Optional[Dict]:
        """
        Fetch book details from Open Library API.

        Args:
            isbn (str): ISBN number

        Returns:
            Optional[Dict]: Book details or None
        """
        try:
            url = (
                f"https://openlibrary.org/api/books?"
                f"bibkeys=ISBN:{isbn}&format=json&jscmd=data"
            )
            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                data = response.json()
                key = f"ISBN:{isbn}"

                if key in data:
                    book_data = data[key]
                    self.logger.info("Fetched book details for ISBN: %s", isbn)
                    return {
                        "title": book_data.get("title", "Unknown"),
                        "authors": [
                            author["name"]
                            for author in book_data.get("authors", [])
                        ],
                        "publish_date": book_data.get("publish_date", "Unknown"),
                        "publishers": [
                            pub["name"]
                            for pub in book_data.get("publishers", [])
                        ],
                        "number_of_pages": book_data.get(
                            "number_of_pages", "Unknown"
                        ),
                        "cover": book_data.get("cover", {}).get("medium", None)
                    }

            self.logger.warning("No data found for ISBN: %s", isbn)
            return None

        except requests.exceptions.Timeout:
            self.logger.error("API timeout for ISBN: %s", isbn)
            print("⚠️  API request timed out")
            return None
        except Exception as error:
            self.logger.error("Error fetching book details: %s", error)
            print(f"⚠️  Error fetching book details: {error}")
            return None

    def add_book_from_api(self, isbn: str) -> Optional[Dict]:
        """
        Add a book by fetching details from API.

        Args:
            isbn (str): ISBN number

        Returns:
            Optional[Dict]: Added book or None
        """
        print(f"🔍 Fetching details for ISBN: {isbn}...")
        details = self.fetch_book_details(isbn)

        if details:
            author = details["authors"][0] if details["authors"] else "Unknown"
            title = details["title"]

            # Extract year from publish_date
            year = None
            try:
                year = int(details["publish_date"].split()[-1])
            except (ValueError, IndexError, AttributeError):
                pass

            return self.add_book(
                title=title,
                author=author,
                genre="Unknown",
                year=year,
                isbn=isbn
            )

        self.logger.warning("Could not fetch details for ISBN: %s", isbn)
        print(f"❌ Could not fetch details for ISBN: {isbn}")
        return None

    def delete_book(self, book_id: int) -> bool:
        """
        Delete a book from the library.

        Args:
            book_id (int): Book ID to delete

        Returns:
            bool: True if successful, False otherwise
        """
        for i, book in enumerate(self.books):
            if book["id"] == book_id:
                deleted_book = self.books.pop(i)
                self.save_books()
                self.logger.info(
                    "Deleted book ID %d: '%s'",
                    book_id, deleted_book['title']
                )
                print(f"✅ Deleted: '{deleted_book['title']}'")
                return True

        self.logger.warning("Book ID %d not found for deletion", book_id)
        print(f"❌ Book ID {book_id} not found")
        return False