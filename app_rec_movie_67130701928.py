import streamlit as st
import pickle
from pathlib import Path
from myfunction_67130701928 import get_movie_recommendations

# Try to load data from the same directory as this script
DATA_PATH = Path(__file__).parent / 'recommendation_data.pkl'
user_similarity_df = None
user_movie_ratings = None

st.title("🎬 Movie Recommendation System")

st.sidebar.header("User Settings")
user_id = st.sidebar.number_input("Enter User ID", min_value=1, step=1, value=1)
num_recommendations = st.sidebar.slider("Number of Recommendations", 1, 20, 10)

if not DATA_PATH.exists():
    st.error(f"Data file not found: {DATA_PATH}. Make sure `recommendation_data.pkl` is placed next to this app.")
else:
    try:
        with DATA_PATH.open('rb') as file:
            loaded = pickle.load(file)
            # support both list/tuple and direct two-object pickles
            if isinstance(loaded, (list, tuple)) and len(loaded) >= 2:
                user_similarity_df, user_movie_ratings = loaded[0], loaded[1]
            else:
                st.error("Unexpected data format in pickle. Expected (user_similarity_df, user_movie_ratings).")
    except Exception as e:
        st.error(f"Error loading data: {e}")

# Get recommendations button
if st.button("Get Recommendations"):
    if user_similarity_df is None or user_movie_ratings is None:
        st.error("Recommendation data not loaded. Fix the data file and try again.")
    else:
        # Validate user id exists in the data
        if user_id not in user_similarity_df.index or user_id not in user_movie_ratings.index:
            st.error(f"User ID {user_id} not found in the dataset. Try an ID between {user_similarity_df.index.min()} and {user_similarity_df.index.max()}.")
        else:
            try:
                recommendations = get_movie_recommendations(int(user_id), user_similarity_df, user_movie_ratings, int(num_recommendations))
            except Exception as e:
                st.error(f"Error computing recommendations: {e}")
                recommendations = None

            if recommendations:
                st.subheader(f"Top {len(recommendations)} Movie Recommendations for User {user_id}:")
                for i, movie_title in enumerate(recommendations, start=1):
                    st.write(f"**{i}.** {movie_title}")
            else:
                st.warning("No recommendations found for this user. Please check the data or try another User ID.")




