from tmdbv3api import TMDb, Discover
from dotenv import load_dotenv
import os
import random

load_dotenv()
tmdb = TMDb()
tmdb.api_key = os.getenv('TMDB_API_KEY')

mood_to_genre = {
    'happy': [35, 10751, 16],  # Comedy, Family, Animation
    'sad': [18, 10749],        # Drama, Romance
    'scary': [27, 53],         # Horror, Thriller
    'excited': [28, 12]        # Action, Adventure
}

def get_movies_by_mood(mood, num_recommendations=5):
    """Fetch movies based on user mood with randomization.

    Args:
        mood (str): User's selected mood (e.g., 'happy', 'surprise').
        num_recommendations (int): Number of movies to return (default: 5).

    Returns:
        list: List of movie dictionaries with title, poster, overview, and fun fact.
        dict: Error message if mood is invalid.
    """
    if mood not in mood_to_genre and mood != 'surprise':
        return {"error": "Mood not recognized."}

    discover = Discover()
    if mood == 'surprise':
        genres = [g for sublist in mood_to_genre.values() for g in sublist]
    else:
        genres = mood_to_genre[mood]

    try:
        movies = discover.discover_movies(params={'with_genres': ','.join(map(str, genres))})
        random.shuffle(movies)  # Randomize results
        results = []
        for m in movies[:num_recommendations]:
            results.append({
                'title': m.title,
                'poster': f"https://image.tmdb.org/t/p/w500{m.poster_path}" if m.poster_path else None,
                'overview': m.overview,
                'fun_fact': get_movie_fun_fact(m.id)
            })
        return results
    except Exception as e:
        return {"error": f"Error fetching movies: {str(e)}"}

def get_movie_fun_fact(movie_id):
    """Fetch a fun fact about the movie (mocked for simplicity).

    Args:
        movie_id (int): TMDB movie ID.

    Returns:
        str: A fun fact about the movie.
    """
    # Placeholder: TMDB doesn't provide fun facts; use a static fact or external API
    return f"Did you know? This movie (ID: {movie_id}) has an interesting story behind its production!"
