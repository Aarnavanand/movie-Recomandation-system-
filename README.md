Movie Recommendation System

This Streamlit application leverages collaborative filtering to provide personalized movie recommendations.
It utilizes pre-computed similarity scores between movies to suggest top 10 recommendations based on a user's selected movie.

Key Features:

User-Friendly Interface: Intuitive interface with a search bar and a dropdown for easy movie selection.
Personalized Recommendations: Provides tailored recommendations based on the selected movie's similarity to other movies in the dataset.
Visual Appeal: Incorporates visually appealing elements like movie posters and a clean, modern design.
Error Handling: Includes robust error handling for scenarios like invalid movie selections or missing data.
How to Use:

Clone the repository.
Install dependencies: pip install streamlit pandas numpy requests pillow
Replace placeholders:
Update the file paths in the code to match the location of your data files (movies_df.csv, movies_sim.npz, tv_show.csv, tv_sim.npz).
Replace "YOUR_TMDb_API_KEY" with your actual TMDb API key.
Run the app: streamlit run app.py (replace app.py with the actual filename)
Note:

This application requires pre-processed movie data and similarity matrices.
The quality of recommendations depends on the accuracy and completeness of the underlying data.
The TMDb API key is required to fetch movie posters.

Live on: https://arnavanand.streamlit.app/

