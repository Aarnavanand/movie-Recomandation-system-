### 🎬 Movie Recommendation System
This Streamlit application leverages collaborative filtering to provide personalized movie recommendations based on user input.
It utilizes pre-computed similarity scores between movies to suggest the top 10 recommendations according to the selected movie.

✨ Key Features
- User-Friendly Interface:
- Intuitive design with a search bar and dropdown for easy movie selection.
- Personalized Recommendations:
- Tailored movie suggestions based on pre-computed similarity.
- Visual Appeal:
- Displays movie posters and maintains a clean, modern UI.
- Robust Error Handling:
- Handles invalid selections, missing data, and API errors gracefully.

### 🛠️ How to Use
Clone the Repository
   ```
   git clone https://github.com/your-username/movie-recommendation-system.git
   cd movie-recommendation-system
   ```
Install Dependencies
```
  pip install streamlit pandas numpy requests pillow
```
Update Configurations
  File Paths:
  Update the paths in the code to match your local files:
  movies_df.csv
  movies_sim.npz
  tv_show.csv
  tv_sim.npz
  TMDb API Key:
  Replace "YOUR_TMDb_API_KEY" in the code with your actual TMDb API key to fetch movie posters.

Run the Application
```
streamlit run app.py
```
Live: https://arnavanand.streamlit.app/
