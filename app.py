import streamlit as st
import pandas as pd
import numpy as np
import json
from PIL import Image
import requests

# Load data (Replace with your actual file paths)
movies_df = pd.read_csv('movies_df.csv')
movies_sim = np.load('movies_sim.npz')['m']
tv_show = pd.read_csv('tv_show.csv')
tv_sim = np.load('tv_sim.npz')['t']

# Recommendation function
def recommend(title):
    if title in movies_df['title'].values:
        movies_index = movies_df[movies_df['title'] == title].index.item()
        scores = dict(enumerate(movies_sim[movies_index]))
        sorted_scores = dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))
        selected_movies_index = [id for id, scores in sorted_scores.items()]
        selected_movies_score = [scores for id, scores in sorted_scores.items()]

        rec_movies = movies_df.iloc[selected_movies_index]
        rec_movies['similarity'] = selected_movies_score

        return rec_movies.reset_index(drop=True)[1:11]

    elif title in tv_show['title'].values:
        tv_index = tv_show[tv_show['title'] == title].index.item()
        scores = dict(enumerate(tv_sim[tv_index]))
        sorted_scores = dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))
        selected_tv_index = [id for id, scores in sorted_scores.items()]
        selected_tv_score = [scores for id, scores in sorted_scores.items()]

        rec_tv = tv_show.iloc[selected_tv_index]
        rec_tv['similarity'] = selected_tv_score

        return rec_tv.reset_index(drop=True)[1:11]

# Load movie poster function (Replace with your actual TMDb API key)
def get_poster_path(movie_title):
    api_key = "YOUR_TMDb_API_KEY"  # Replace with your actual TMDb API key
    base_url = "https://image.tmdb.org/t/p/w500/"
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_title}"
    response = requests.get(search_url).json()
    try:
        poster_path = response['results'][0]['poster_path']
        return base_url + poster_path
    except (IndexError, KeyError):
        return None

# Set up Streamlit page
st.set_page_config(page_title="🏆 Movie Recommender", layout="wide")

# Custom CSS for styling
st.markdown("""
<style>
.st-by {
    animation: fadeIn 0.5s ease-in-out;
}
@keyframes fadeIn {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}
.movie-card {
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    border-radius: 5px;
    padding: 10px;
    margin: 10px;
    display: flex;
    flex-direction: column;
    align-items: center;
    cursor: pointer;
    transition: transform 0.2s ease-in-out;
}
.movie-card:hover {
    transform: scale(1.05);
}
.movie-poster {
    width: 150px;
    height: 225px;
    object-fit: cover;
    border-radius: 5px;
}
.movie-title {
    font-weight: bold;
    margin-top: 10px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# Main page
st.title("🏆 Movie Recommendation System")

# Hero section with image
col1, col2 = st.columns([1, 2])
with col1:
    st.image("movie-png.png", caption="Best Recommendation By Your Last Watch", width=200)
with col2:
    st.subheader("Find your next favorite movie!")

# Search bar
search_term = st.text_input("Search for a movie:")
filtered_movies = [movie for movie in movies_df['title'].tolist() + tv_show['title'].tolist() if search_term.lower() in movie.lower()]

# Selectbox with placeholder
selected_movie = st.selectbox(
    "Select a movie",
    ["Select a movie"] + filtered_movies
)

# Button with animation
if st.button("Show Recommendations", key="recommend_button"):
    if selected_movie == "Select a movie":
        st.warning("Please select a movie.")
    else:
        with st.spinner("Generating recommendations..."):
            try:
                recommended_movies = recommend(selected_movie)
            except ValueError:
                st.error(f"No recommendations found for '{selected_movie}'. Please try another movie.")
                return

        st.subheader("Top 10 Recommendations")

        # Display recommendations in card layout
        cols = st.columns(5)
        for i, movie in enumerate(recommended_movies.iterrows()):
            with cols[i % 5]:
                st.markdown(f"<div class='movie-card'>", unsafe_allow_html=True)
                st.markdown(f"<div class='movie-title'>{movie[1]['title']}</div>", unsafe_allow_html=True)
                poster_path = get_poster_path(movie[1]['title'])
                if poster_path:
                    poster = Image.open(requests.get(poster_path, stream=True).raw)
                    st.image(poster, classes=['movie-poster'])
                st.write(f"**Genre:** {movie[1]['genres']}")
                st.write(f"**Release Year:** {movie[1]['release_year']}")
                st.markdown(f"</div>", unsafe_allow_html=True)
