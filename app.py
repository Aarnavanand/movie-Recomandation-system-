import streamlit as st
import pandas as pd
import numpy as np
import json

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

movie_list = sorted(movies_df['title'].tolist() + tv_show['title'].tolist())

st.header('Movie Recommendation System')

st.image("movie-png.png", caption="Find Your Next Favorite Movie", width=300)

selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names = recommend(selected_movie)
    st.subheader("Top 10 Recommended Movies")

    st.dataframe(
        data=recommended_movie_names[['title', 'country', 'genres', 'description', 'release_year', 'cast']], 
        height=400
    )


st.markdown("""
<style>
    .streamlit-expanderHeader {
        font-size: 20px;
        font-weight: bold;
        color: #F39C12;
    }
    .stDataFrame {
        animation: fadeIn 0.5s;
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
