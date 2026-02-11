# 🎬 Movie Agent

A simple movie management app with both CLI and Streamlit UI. Track your movies, search from external APIs, and get recommendations!

## Features

- ✅ Add movies manually or fetch from APIs (Studio Ghibli & OMDB)
- 🔍 Search by title, genre, or rating
- ⭐ Get personalized recommendations
- 📊 View collection statistics
- 💾 Persistent storage with JSON
- 🖥️ Both CLI and Web UI available

## Project Structure

```
movie-agent/
├── movie_agent.py      # Core movie management logic
├── cli.py              # Command-line interface
├── streamlit_app.py    # Streamlit web interface
├── requirements.txt    # Python dependencies
├── data/
│   └── movies.json    # Movie database (auto-created)
└── README.md
```

## Installation

### 1. Clone or Download

```bash
git clone <your-repo-url>
cd movie-agent
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. (Optional) Setup OMDB API Key

To enable OMDB movie search, get a free API key from [OMDb API](http://www.omdbapi.com/apikey.aspx)

Set it as an environment variable:

**Linux/Mac:**
```bash
export OMDB_API_KEY="your_api_key_here"
```

**Windows:**
```bash
set OMDB_API_KEY=your_api_key_here
```

## Running the App

### Option 1: Streamlit UI (Recommended)

```bash
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

### Option 2: CLI

```bash
python cli.py
```

Follow the interactive menu to manage your movies.

## Deployment to Streamlit Cloud

### Step-by-Step Guide:

1. **Create a GitHub Repository**
   - Go to [GitHub](https://github.com) and create a new repository
   - Upload all files: `movie_agent.py`, `streamlit_app.py`, `cli.py`, `requirements.txt`, `README.md`

2. **Go to Streamlit Cloud**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account

3. **Deploy Your App**
   - Click "New app"
   - Select your repository
   - Main file path: `streamlit_app.py`
   - Click "Deploy"

4. **(Optional) Add OMDB API Key**
   - In Streamlit Cloud, go to App settings → Secrets
   - Add:
     ```toml
     OMDB_API_KEY = "your_api_key_here"
     ```

5. **Done!** Your app is now live and accessible via a public URL!

## Usage Guide

### Streamlit UI

- **Home**: Overview of your collection with statistics
- **All Movies**: View and manage all your movies with filters
- **Add Movie**: Search from APIs or add manually
- **Search**: Find movies by title, genre, or get recommendations
- **Statistics**: View detailed analytics and charts

### CLI

Run `python cli.py` and choose from the menu:

1. **View all movies**: See your entire collection
2. **Add movie**: Add manually or search from API
3. **Search movies**: Search by title, genre, or rating
4. **Manage movies**: Mark as watched or delete
5. **View statistics**: See your collection stats
6. **Exit**: Close the app

## API Information

- **Studio Ghibli API**: Always available, no key needed
- **OMDB API**: Requires free API key (optional)

## Data Storage

All movies are stored in `data/movies.json` which is automatically created on first run.

## Troubleshooting

**Issue**: "Module not found" error  
**Solution**: Make sure you've run `pip install -r requirements.txt`

**Issue**: API not working  
**Solution**: Check your internet connection and API key (for OMDB)

**Issue**: Data not persisting  
**Solution**: Make sure the app has write permissions in the directory

## License

Free to use and modify!

## Contributing

Feel free to fork and submit pull requests!