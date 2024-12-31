import streamlit as st
import pandas as pd
import numpy as np

# Load data
movies_df = pd.read_csv('movies_df.csv')
movies_sim = np.load('movies_sim.npz')['m']
tv_show = pd.read_csv('tv_show.csv')
tv_sim = np.load('tv_sim.npz')['t']

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

# Combine movie and TV show titles
movie_list = sorted(movies_df['title'].tolist() + tv_show['title'].tolist())

# Set up Streamlit page
st.set_page_config(page_title="🎬 Movie Recommendation System", layout="wide")

# Header
st.markdown("<h1 style='text-align: center; color: #E50914;'>🎬 Movie Recommendation System</h1>", unsafe_allow_html=True)

# Image with increased size
st.image("movie-system.jpg", caption="Best Recommendation By Your Last Watch", width=600)  # Increased width

# Selectbox for movie selection
selected_movie = st.selectbox(
    "Select a movie from the dropdown",
    movie_list
)

# Button to show recommendations
if st.button('Show Recommendation'):
    recommended_movie_names = recommend(selected_movie)
    st.subheader("Here are your Top 10 Movies")

    # Display recommendations in a card layout
    cols = st.columns(5)
    for i, movie in enumerate(recommended_movie_names.iterrows()):
        with cols[i % 5]:
            st.markdown(f"""
            <div class="movie-card">
                <h3>{movie[1]['title']}</h3>
                <p><strong>Country:</strong> {movie[1]['country']}</p>
                <p><strong>Genres:</strong> {movie[1]['genres']}</p>
                <p><strong>Release Year:</strong> {movie[1]['release_year']}</p>
                <p><strong>Cast:</strong> {movie[1]['cast']}</p>
            </div>
            """, unsafe_allow_html=True)

# Custom CSS for styling
st.markdown("""
<style>
    body {
        background-color: #141414; /* Dark background */
        color: #FFFFFF; /* White text */
    }
    .movie-card {
        background-color: #333333; /* Dark card background */
        border-radius: 10px;
        padding: 15px;
        margin: 10px;
        transition: transform 0.2s, box-shadow 0.2s;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
        height: 300px; /* Fixed height for uniformity */
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .movie-card:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.7);
    }
    .stButton {
        background-color: #E50914; /* Netflix red */
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
    }
    .stButton:hover {
        background-color: #B00710; /* Darker red on hover */
    }
</style>
""", unsafe_allow_html=True)
