import streamlit as st
from movie_agent import MovieAgent
import os
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Movie Agent",
    page_icon="🎬",
    layout="wide"
)

# Initialize session state
if 'agent' not in st.session_state:
    omdb_key = os.getenv("OMDB_API_KEY")
    st.session_state.agent = MovieAgent(omdb_api_key=omdb_key)

agent = st.session_state.agent

# Custom CSS
st.markdown("""
    <style>
    .movie-card {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f0f2f6;
        margin-bottom: 0.5rem;
    }
    .stat-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #e8f4f8;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("🎬 Movie Agent")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("Navigation")
    page = st.radio(
        "Choose a page:",
        ["🏠 Home", "📋 All Movies", "➕ Add Movie", "🔍 Search", "📊 Statistics"],
        label_visibility="collapsed"
    )

    st.markdown("---")

    # API Status
    st.subheader("API Status")
    if agent.omdb_api_key:
        st.success("✓ OMDB API: Enabled")
    else:
        st.info("○ OMDB API: Not configured")
    st.success("✓ Ghibli API: Available")

    st.markdown("---")
    st.caption("Movie Agent v1.0")


# Helper function to display movies
def display_movie_card(movie, key_prefix=""):
    """Display a movie as a card"""
    col1, col2, col3 = st.columns([3, 1, 1])

    with col1:
        st.markdown(f"### {movie['title']}")
        st.write(f"**Year:** {movie['year']} | **Genre:** {movie['genre']}")

    with col2:
        st.metric("Rating", f"{movie['rating']}/10")

    with col3:
        if movie['watched']:
            st.success("✓ Watched")
        else:
            st.info("○ Not watched")

    # Action buttons
    col1, col2, col3 = st.columns([1, 1, 4])

    with col1:
        if not movie['watched']:
            if st.button("Mark Watched", key=f"{key_prefix}_watch_{movie['title']}"):
                agent.mark_as_watched(movie['title'])
                st.rerun()

    with col2:
        if st.button("Delete", key=f"{key_prefix}_del_{movie['title']}"):
            agent.delete_movie(movie['title'])
            st.success(f"Deleted '{movie['title']}'")
            st.rerun()

    st.markdown("---")


# HOME PAGE
if page == "🏠 Home":
    st.header("Welcome to Movie Agent!")

    stats = agent.get_statistics()

    # Statistics cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown('<div class="stat-box">', unsafe_allow_html=True)
        st.metric("Total Movies", stats['total'])
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="stat-box">', unsafe_allow_html=True)
        st.metric("Watched", stats['watched'])
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="stat-box">', unsafe_allow_html=True)
        st.metric("Not Watched", stats['unwatched'])
        st.markdown('</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="stat-box">', unsafe_allow_html=True)
        st.metric("Avg Rating", f"{stats['avg_rating']}/10")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Recent additions (last 5 movies)
    st.subheader("📚 Your Collection")
    movies = agent.list_movies()

    if movies:
        recent = movies[-5:][::-1]  # Last 5, reversed
        st.write(f"Showing {len(recent)} of {len(movies)} movies")

        for movie in recent:
            display_movie_card(movie, key_prefix="home")
    else:
        st.info("No movies yet. Add your first movie!")


# ALL MOVIES PAGE
elif page == "📋 All Movies":
    st.header("All Movies")

    movies = agent.list_movies()

    if movies:
        # Filters
        col1, col2 = st.columns(2)

        with col1:
            genres = ["All"] + agent.get_all_genres()
            selected_genre = st.selectbox("Filter by Genre", genres)

        with col2:
            watch_filter = st.selectbox("Filter by Status", ["All", "Watched", "Not Watched"])

        # Apply filters
        filtered_movies = movies

        if selected_genre != "All":
            filtered_movies = [m for m in filtered_movies if m['genre'] == selected_genre]

        if watch_filter == "Watched":
            filtered_movies = [m for m in filtered_movies if m['watched']]
        elif watch_filter == "Not Watched":
            filtered_movies = [m for m in filtered_movies if not m['watched']]

        st.write(f"Showing {len(filtered_movies)} movies")
        st.markdown("---")

        # Display movies
        for movie in filtered_movies:
            display_movie_card(movie, key_prefix="all")
    else:
        st.info("No movies in your collection yet.")


# ADD MOVIE PAGE
elif page == "➕ Add Movie":
    st.header("Add New Movie")

    tab1, tab2 = st.tabs(["🔍 Search from API", "✍️ Manual Entry"])

    with tab1:
        st.subheader("Search from API")

        search_title = st.text_input("Enter movie title to search")

        if st.button("Search", type="primary"):
            if search_title:
                with st.spinner("Searching..."):
                    movie_data = agent.fetch_movie_from_api(search_title)

                if movie_data:
                    st.success("Movie found!")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.write(f"**Title:** {movie_data['title']}")
                        st.write(f"**Genre:** {movie_data['genre']}")
                        st.write(f"**Rating:** {movie_data['rating']}/10")
                        st.write(f"**Year:** {movie_data['year']}")

                    with col2:
                        st.write(f"**Source:** {movie_data.get('source', 'API')}")
                        if movie_data.get('director'):
                            st.write(f"**Director:** {movie_data['director']}")

                    if movie_data.get('description'):
                        st.write(f"**Description:** {movie_data['description']}")

                    if st.button("Add this movie", type="primary"):
                        result = agent.add_movie_from_api(search_title)
                        if result:
                            st.success(f"✓ '{movie_data['title']}' added successfully!")
                            st.balloons()
                        else:
                            st.error("Failed to add movie. It might already exist.")
                else:
                    st.error("Movie not found in API. Try manual entry or a different title.")
            else:
                st.warning("Please enter a movie title.")

    with tab2:
        st.subheader("Manual Entry")

        with st.form("add_movie_form"):
            title = st.text_input("Movie Title*")

            col1, col2 = st.columns(2)

            with col1:
                genre = st.text_input("Genre*")
                rating = st.slider("Rating", 0.0, 10.0, 7.0, 0.1)

            with col2:
                year = st.number_input("Year*", min_value=1900, max_value=2030, value=2024)
                watched = st.checkbox("Already watched?")

            submitted = st.form_submit_button("Add Movie", type="primary")

            if submitted:
                if title and genre:
                    agent.add_movie(title, genre, rating, year, watched)
                    st.success(f"✓ '{title}' added successfully!")
                    st.balloons()
                else:
                    st.error("Please fill in all required fields (marked with *).")


# SEARCH PAGE
elif page == "🔍 Search":
    st.header("Search Movies")

    tab1, tab2, tab3 = st.tabs(["🔤 By Title", "🎭 By Genre", "⭐ Recommendations"])

    with tab1:
        st.subheader("Search by Title")
        search_term = st.text_input("Enter title to search")

        if search_term:
            results = agent.search_by_title(search_term)

            if results:
                st.success(f"Found {len(results)} movie(s)")
                st.markdown("---")
                for movie in results:
                    display_movie_card(movie, key_prefix="search_title")
            else:
                st.info("No movies found matching your search.")

    with tab2:
        st.subheader("Search by Genre")

        genres = agent.get_all_genres()

        if genres:
            selected_genre = st.selectbox("Select Genre", genres)

            if selected_genre:
                results = agent.search_by_genre(selected_genre)

                st.success(f"Found {len(results)} movie(s) in '{selected_genre}' genre")
                st.markdown("---")

                for movie in results:
                    display_movie_card(movie, key_prefix="search_genre")
        else:
            st.info("No genres available yet. Add some movies first!")

    with tab3:
        st.subheader("Get Recommendations")

        min_rating = st.slider("Minimum Rating", 0.0, 10.0, 8.0, 0.5)

        results = agent.recommend(min_rating)

        if results:
            st.success(f"Found {len(results)} recommended movie(s) with rating >= {min_rating}")
            st.markdown("---")

            for movie in results:
                display_movie_card(movie, key_prefix="recommend")
        else:
            st.info(f"No movies found with rating >= {min_rating}")


# STATISTICS PAGE
elif page == "📊 Statistics":
    st.header("Collection Statistics")

    stats = agent.get_statistics()
    movies = agent.list_movies()

    # Overview stats
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Total Movies", stats['total'])

    with col2:
        st.metric("Watched", stats['watched'])

    with col3:
        st.metric("Not Watched", stats['unwatched'])

    with col4:
        st.metric("Avg Rating", f"{stats['avg_rating']}/10")

    with col5:
        st.metric("Genres", stats['genres'])

    st.markdown("---")

    if movies:
        # Genre distribution
        st.subheader("Genre Distribution")
        genre_counts = {}
        for movie in movies:
            genre = movie['genre']
            genre_counts[genre] = genre_counts.get(genre, 0) + 1

        genre_df = pd.DataFrame(list(genre_counts.items()), columns=['Genre', 'Count'])
        genre_df = genre_df.sort_values('Count', ascending=False)

        st.bar_chart(genre_df.set_index('Genre'))

        st.markdown("---")

        # Rating distribution
        st.subheader("Rating Distribution")
        rating_ranges = {
            "0-2": 0, "2-4": 0, "4-6": 0, "6-8": 0, "8-10": 0
        }

        for movie in movies:
            rating = movie['rating']
            if rating < 2:
                rating_ranges["0-2"] += 1
            elif rating < 4:
                rating_ranges["2-4"] += 1
            elif rating < 6:
                rating_ranges["4-6"] += 1
            elif rating < 8:
                rating_ranges["6-8"] += 1
            else:
                rating_ranges["8-10"] += 1

        rating_df = pd.DataFrame(list(rating_ranges.items()), columns=['Rating Range', 'Count'])
        st.bar_chart(rating_df.set_index('Rating Range'))

        st.markdown("---")

        # Top rated movies
        st.subheader("🏆 Top 5 Rated Movies")
        top_movies = sorted(movies, key=lambda x: x['rating'], reverse=True)[:5]

        for i, movie in enumerate(top_movies, 1):
            st.write(f"{i}. **{movie['title']}** - {movie['rating']}/10 ({movie['year']})")
    else:
        st.info("Add some movies to see statistics!")