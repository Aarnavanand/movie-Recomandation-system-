import streamlit as st
import pandas as pd
import numpy as np
import json
from PIL import Image
import requests

# Load data (replace with your file paths)
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

# Load movie poster function (replace with your TMDb API key)
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
