import streamlit as st
import pickle
from myfunction_67130701928 import get_movie_recommendations

# Load data
with open('recommendation_data.pkl', 'rb') as file:
    user_similarity_df, user_movie_ratings = pickle.load(file)

# Streamlit app
st.title("🎬 Movie Recommendation System")

# Input section
st.sidebar.header("User Settings")
user_id = st.sidebar.number_input("Enter User ID", min_value=1, step=1, value=1)
num_recommendations = st.sidebar.slider("Number of Recommendations", 1, 20, 10)

# Get recommendations button
if st.button("Get Recommendations"):
    recommendations = get_movie_recommendations(user_id, user_similarity_df, user_movie_ratings, num_recommendations)
    
    if recommendations:
        st.subheader(f"Top {num_recommendations} Movie Recommendations for User {user_id}:")
        for i, movie_title in enumerate(recommendations, start=1):
            st.write(f"**{i}.** {movie_title}")
    else:
        st.warning("No recommendations found for this user. Please check the data or try another User ID.")


