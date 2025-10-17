"""Return up to `n_recommendations` movie titles recommended for `user_id`.

This function looks at users most similar to `user_id`, gathers movies those
users rated above a threshold, and excludes movies the target user has
already rated. It avoids duplicate titles and is defensive about input data.

Parameters
----------
user_id : int or hashable
    The user identifier present in the index of the provided DataFrames.
user_similarity_df : pandas.DataFrame
    Square DataFrame of user-user similarities indexed and columned by user id.
user_movie_ratings : pandas.DataFrame
    DataFrame with users as index and movie titles as columns; values are ratings
n_recommendations : int
    Maximum number of recommendations to return.
rating_threshold : float
    Minimum rating (exclusive) from other users to consider a movie liked.

Returnsrun
-------
list
    List of movie title strings (may be empty).
"""
def get_movie_recommendations(user_id, user_similarity_df, user_movie_ratings, n_recommendations, rating_threshold=3.0):
    # Defensive checks
    try:
        import pandas as pd
    except Exception:
        pd = None

    if n_recommendations is None or int(n_recommendations) <= 0:
        return []

    # Ensure user exists in both inputs
    if user_id not in getattr(user_similarity_df, 'index', []) or user_id not in getattr(user_movie_ratings, 'index', []):
        return []

    # Get similar users in descending order, excluding the user themself
    try:
        sim_series = user_similarity_df.loc[user_id].sort_values(ascending=False)
    except Exception:
        return []

    similar_users = [uid for uid in sim_series.index if uid != user_id]

    # Target user's ratings (treat NaN as unseen -> 0)
    user_ratings = user_movie_ratings.loc[user_id].fillna(0)

    recommendations = []
    seen = set()

    for other_user in similar_users:
        if other_user not in user_movie_ratings.index:
            continue

        other_ratings = user_movie_ratings.loc[other_user].fillna(0)

        # Candidate movies: other user rated above threshold and target user hasn't rated (>0)
        try:
            mask = (other_ratings > rating_threshold) & (user_ratings <= 0)
        except Exception:
            # Fallback: elementwise comparisons might fail for strange dtypes
            mask = (other_ratings.apply(lambda x: float(x) if pd is None else float(x) if not pd.isna(x) else 0) > rating_threshold) & (user_ratings <= 0)

        movies = other_ratings[mask].sort_values(ascending=False).index.tolist()

        for m in movies:
            if m in seen:
                continue
            recommendations.append(m)
            seen.add(m)
            if len(recommendations) >= int(n_recommendations):
                return recommendations[:int(n_recommendations)]

    return recommendations[:int(n_recommendations)]  # Return up to n recommendations
