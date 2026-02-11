"""
Main entry point for the Mini Library Manager application.
"""

import logging
from typing import List, Dict
from src.library_agent import LibraryAgent


def setup_main_logger() -> logging.Logger:
    """
    Set up the main application logger.

    Returns:
        logging.Logger: Configured logger
    """
    logger = logging.getLogger('MainApp')
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler('logs/library.log')
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(file_handler)

    return logger


def display_books_table(books: List[Dict]) -> None:
    """
    Display books in a formatted table.

    Args:
        books (List[Dict]): List of book dictionaries
    """
    if not books:
        print("\n📚 No books found.")
        return

    print(f"\n{'=' * 100}")
    print(
        f"{'ID':<5} {'Title':<30} {'Author':<20} "
        f"{'Genre':<15} {'Status':<10} {'Rating':<8}"
    )
    print(f"{'=' * 100}")

    for book in books:
        rating = f"{book.get('rating', '-')}⭐" if book.get('rating') else "-"
        print(
            f"{book['id']:<5} {book['title'][:28]:<30} "
            f"{book['author'][:18]:<20} {book['genre'][:13]:<15} "
            f"{book['status']:<10} {rating:<8}"
        )

    print(f"{'=' * 100}")
    print(f"Total: {len(books)} book(s)\n")


def display_menu() -> None:
    """Display the main menu."""
    print("\n" + "=" * 60)
    print("MENU:")
    print("1.  Add Book (Manual)")
    print("2.  Add Book (From ISBN)")
    print("3.  List All Books")
    print("4.  Search Books")
    print("5.  Update Reading Status")
    print("6.  Rate a Book")
    print("7.  Get Recommendations")
    print("8.  Organize by Genre")
    print("9.  Organize by Author")
    print("10. View Statistics")
    print("11. Delete Book")
    print("0.  Exit")
    print("=" * 60)


def handle_add_book_manual(agent: LibraryAgent) -> None:
    """Handle manual book addition."""
    print("\n➕ ADD NEW BOOK")
    title = input("Title: ").strip()
    if not title:
        print("❌ Title cannot be empty")
        return

    author = input("Author: ").strip()
    if not author:
        print("❌ Author cannot be empty")
        return

    genre = input("Genre: ").strip() or "Unknown"
    year_input = input("Year (optional): ").strip()
    year = int(year_input) if year_input.isdigit() else None
    isbn = input("ISBN (optional): ").strip() or None

    agent.add_book(title, author, genre, year, isbn)


def handle_add_book_isbn(agent: LibraryAgent) -> None:
    """Handle book addition via ISBN."""
    print("\n🔍 ADD BOOK FROM ISBN")
    isbn = input("Enter ISBN: ").strip()
    if isbn:
        agent.add_book_from_api(isbn)
    else:
        print("❌ ISBN cannot be empty")


def handle_list_books(agent: LibraryAgent) -> None:
    """Handle listing books."""
    print("\n📚 ALL BOOKS")
    filter_choice = input(
        "Filter by (all/read/reading/unread) [all]: "
    ).strip() or "all"
    books = agent.list_books(filter_choice)
    display_books_table(books)


def handle_search_books(agent: LibraryAgent) -> None:
    """Handle book search."""
    print("\n🔍 SEARCH BOOKS")
    search_by = input(
        "Search by (title/author/genre) [title]: "
    ).strip() or "title"
    query = input(f"Enter {search_by}: ").strip()

    if query:
        results = agent.search_books(query, search_by)
        display_books_table(results)
    else:
        print("❌ Search query cannot be empty")


def handle_update_status(agent: LibraryAgent) -> None:
    """Handle status update."""
    print("\n📖 UPDATE READING STATUS")
    try:
        book_id = int(input("Enter Book ID: ").strip())
        status = input("Status (unread/reading/read): ").strip()

        if status in ['unread', 'reading', 'read']:
            agent.update_status(book_id, status)
        else:
            print("❌ Invalid status. Use: unread, reading, or read")
    except ValueError:
        print("❌ Invalid Book ID")


def handle_rate_book(agent: LibraryAgent) -> None:
    """Handle book rating."""
    print("\n⭐ RATE A BOOK")
    try:
        book_id = int(input("Enter Book ID: ").strip())
        rating = float(input("Rating (0-5): ").strip())
        agent.rate_book(book_id, rating)
    except ValueError:
        print("❌ Invalid input")


def handle_recommendations(agent: LibraryAgent) -> None:
    """Handle recommendations."""
    print("\n💡 RECOMMENDATIONS")
    genre = input("Genre (optional): ").strip() or None
    min_rating_input = input("Minimum rating [4.0]: ").strip()

    try:
        min_rating = float(min_rating_input) if min_rating_input else 4.0
        recommendations = agent.get_recommendations(genre, min_rating)
        display_books_table(recommendations)
    except ValueError:
        print("❌ Invalid rating value")


def handle_organize_by_genre(agent: LibraryAgent) -> None:
    """Handle organization by genre."""
    print("\n🏷️  BOOKS BY GENRE")
    organized = agent.organize_by_genre()
    for genre, books in organized.items():
        print(f"\n📚 {genre} ({len(books)} books)")
        display_books_table(books)


def handle_organize_by_author(agent: LibraryAgent) -> None:
    """Handle organization by author."""
    print("\n✍️  BOOKS BY AUTHOR")
    organized = agent.organize_by_author()
    for author, books in organized.items():
        print(f"\n📚 {author} ({len(books)} books)")
        display_books_table(books)


def handle_view_statistics(agent: LibraryAgent) -> None:
    """Handle statistics display."""
    print("\n📊 LIBRARY STATISTICS")
    stats = agent.get_statistics()
    print(f"\n{'=' * 60}")
    print(f"Total Books: {stats['total_books']}")
    print(f"Read: {stats['read']}")
    print(f"Currently Reading: {stats['reading']}")
    print(f"Unread: {stats['unread']}")
    print(f"Average Rating: {stats['average_rating']}⭐")
    print(f"Unique Genres: {stats['unique_genres']}")
    print(f"Unique Authors: {stats['unique_authors']}")
    print(f"{'=' * 60}")


def handle_delete_book(agent: LibraryAgent) -> None:
    """Handle book deletion."""
    print("\n🗑️  DELETE BOOK")
    try:
        book_id = int(input("Enter Book ID: ").strip())
        agent.delete_book(book_id)
    except ValueError:
        print("❌ Invalid Book ID")


def main() -> None:
    """Main application loop."""
    logger = setup_main_logger()
    logger.info("Application started")

    print("\n" + "=" * 60)
    print("📚 MINI LIBRARY MANAGER")
    print("=" * 60)

    # Initialize agent
    agent = LibraryAgent()

    # Display initial statistics
    stats = agent.get_statistics()
    print(f"\n📊 Library Statistics:")
    print(f"   Total Books: {stats['total_books']}")
    print(
        f"   Read: {stats['read']} | "
        f"Reading: {stats['reading']} | "
        f"Unread: {stats['unread']}"
    )
    print(f"   Average Rating: {stats['average_rating']}⭐")
    print(
        f"   Genres: {stats['unique_genres']} | "
        f"Authors: {stats['unique_authors']}"
    )

    # Main loop
    while True:
        display_menu()
        choice = input("\nEnter your choice: ").strip()

        try:
            if choice == "1":
                handle_add_book_manual(agent)
            elif choice == "2":
                handle_add_book_isbn(agent)
            elif choice == "3":
                handle_list_books(agent)
            elif choice == "4":
                handle_search_books(agent)
            elif choice == "5":
                handle_update_status(agent)
            elif choice == "6":
                handle_rate_book(agent)
            elif choice == "7":
                handle_recommendations(agent)
            elif choice == "8":
                handle_organize_by_genre(agent)
            elif choice == "9":
                handle_organize_by_author(agent)
            elif choice == "10":
                handle_view_statistics(agent)
            elif choice == "11":
                handle_delete_book(agent)
            elif choice == "0":
                print("\n👋 Thank you for using Mini Library Manager!")
                print("📚 Your library has been saved.\n")
                logger.info("Application closed by user")
                break
            else:
                print("\n❌ Invalid choice. Please try again.")
        except Exception as error:
            logger.error("Error in main loop: %s", error)
            print(f"\n❌ An error occurred: {error}")


if __name__ == "__main__":
    main()