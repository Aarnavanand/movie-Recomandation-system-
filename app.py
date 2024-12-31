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

# Centered image using columns
col1, col2, col3 = st.columns([1, 2, 1]) 
with col2:st.image("movie-system.jpg", caption="Best Recommendation By Your Last Watch", width=600)  # Increased width

# Selectbox for movie selection
selected_movie = st.selectbox(
    "Select a movie from the dropdown",
    movie_list
)

# Button to show recommendations
if st.button('Show Recommendation'):
    recommended_movie_names = recommend(selected_movie)
    st.subheader("Here are your Top 10 Movies")

    # Display recommendations in a table format
    st.dataframe(
        data=recommended_movie_names[['title', 'country', 'genres', 'release_year', 'cast']], 
        height=400
    )

# Custom CSS for styling
st.markdown("""
<style>
    body {
        background-color: #141414; /* Dark background */
        color: #FFFFFF; /* White text */
    }
    .stDataFrame {
        background-color: #333333; /* Dark table background */
        color: #FFFFFF; /* White text in table */
        border-radius: 10px; /* Rounded corners */
    }
    .stDataFrame th {
        background-color: #E50914; /* Netflix red for header */
        color: white; /* White text for header */
    }
    .stDataFrame td {
        background-color: #333333; /* Dark background for table cells */
        color: #FFFFFF; /* White text for table cells */
    }
    .stDataFrame tr:hover {
        background-color: #444444; /* Slightly lighter on hover */
    }
</style>
""", unsafe_allow_html=True)
