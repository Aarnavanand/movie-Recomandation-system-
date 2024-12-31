import streamlit as st
import pandas as pd
import numpy as np
import json

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
st.header('🎬 Movie Recommendation System')

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

    # Display recommendations in a larger DataFrame
    st.dataframe(
        data=recommended_movie_names[['title', 'country', 'genres', 'release_year', 'cast']], 
        height=600  # Increased height
    )

# Custom CSS for styling
st.markdown("""
<style>
    .streamlit-expanderHeader {
        font-size: 50px;
        font-weight: bold;
        color: #F39C12;
    }
    .stDataFrame {
        animation: fadeIn 0.5s;
        font-size: 18px;  /* Increase font size in the DataFrame */
    }
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
</style>
""", unsafe_allow_html=True)
