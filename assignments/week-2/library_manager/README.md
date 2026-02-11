# 📚 Mini Library Manager

A Python-based stateful library management system with logging, clean architecture, and best practices.

## 🎯 Features

- **Book Management**: Add, search, update, and delete books
- **Persistent Storage**: JSON-based data storage
- **Reading Status Tracking**: Track books as unread, reading, or read
- **Rating System**: Rate books from 0-5 stars
- **Smart Search**: Search by title, author, or genre
- **Organization**: Group books by genre or author
- **Recommendations**: Get suggestions based on ratings and genres
- **API Integration**: Fetch book details from Open Library using ISBN
- **Statistics Dashboard**: View comprehensive library statistics
- **Logging**: Complete logging for debugging and monitoring

## 📋 Requirements

- Python 3.7+
- requests library

## 🚀 Installation

1. Clone or download this project
2. Navigate to the project directory
3. Install dependencies:
```bash
pip install -r requirements.txt
```

## 💻 Usage

Run the application:
```bash
python main.py
```

## 📁 Project Structure
```
library_manager/
│
├── src/
│   └── library_agent.py      # Core LibraryAgent class
│
├── data/
│   └── books.json            # Persistent storage
│
├── logs/
│   └── library.log           # Application logs (auto-created)
│
├── main.py                   # Application entry point
├── README.md                 # This file
├── requirements.txt          # Python dependencies
└── .gitignore               # Git ignore rules
```

## 🔧 Technical Details

### Architecture

- **Separation of Concerns**: Core logic in `src/`, entry point in `main.py`
- **OOP Principles**: Single responsibility, encapsulation
- **Logging**: File-based logging with rotation support
- **Error Handling**: Comprehensive try-except blocks
- **Type Hints**: Full type annotations for better code clarity
- **Pylint Friendly**: Follows PEP 8 and pylint recommendations

### Core Components

1. **LibraryAgent Class**: Manages all book operations
2. **JSON Storage**: Fault-tolerant persistence
3. **Logging System**: Tracks all operations
4. **API Integration**: Open Library API for ISBN lookups
5. **CLI Interface**: User-friendly command-line interface

## 🌐 API Integration

Uses [Open Library API](https://openlibrary.org/developers/api) for ISBN lookups.

Example ISBN: `9780140328721` (Fantastic Mr. Fox)

## 📝 Logging

All operations are logged to `logs/library.log`:
- Book additions/deletions
- Status updates
- API calls
- Errors and warnings

## 🎓 Learning Objectives

- OOP design patterns
- File I/O with JSON
- API consumption
- Error handling
- Logging best practices
- Clean code principles
- Type hints usage

## 👨‍💻 Author

Built following Python best practices and agent architecture patterns.

---

**Happy Reading! 📖**