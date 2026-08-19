import streamlit as st
import pandas as pd
import joblib


# --------------------------------------------------
# Load saved model artifacts
# --------------------------------------------------

@st.cache_resource
def load_model():

    similarity_matrix = joblib.load(
        'final_similarity.pkl'
    )

    movies = pd.read_pickle(
        'movies.pkl'
    )

    title_lookup = joblib.load(
        'title_indices.pkl'
    )

    return similarity_matrix, movies, title_lookup


# Load the model
final_similarity, df, title_indices = load_model()


# --------------------------------------------------
# Recommendation function
# --------------------------------------------------

def recommend_movie(title, top_n=10):

    # Normalize user input
    normalized_title = title.lower().strip()

    # Check whether movie exists
    if normalized_title not in title_indices:
        return None

    # Get movie index
    idx = title_indices[normalized_title]

    # Get similarity scores
    sim_scores = list(
        enumerate(final_similarity[idx])
    )

    # Sort from highest to lowest
    sim_scores = sorted(
        sim_scores,
        key=lambda x: x[1],
        reverse=True
    )

    # Remove the selected movie itself
    sim_scores = [
        item for item in sim_scores
        if item[0] != idx
    ]

    # Select top N
    sim_scores = sim_scores[:top_n]

    # Extract movie indices
    movie_indices = [
        item[0]
        for item in sim_scores
    ]

    # Extract similarity scores
    similarity_scores = [
        item[1]
        for item in sim_scores
    ]

    # Create result table
    recommendations = df.iloc[
        movie_indices
    ][['title']].copy()

    recommendations['similarity_score'] = (
        similarity_scores
    )

    return recommendations.reset_index(drop=True)


# --------------------------------------------------
# Streamlit interface
# --------------------------------------------------

st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="centered"
)


st.title("🎬 Movie Recommendation System")

st.write(
    "Enter a movie title to get the top 10 "
    "movies recommended by the content-based "
    "recommendation model."
)


# Movie input
movie_title = st.text_input(
    "Enter movie title:",
    placeholder="Example: Avatar"
)


# Number of recommendations
top_n = st.slider(
    "Number of recommendations:",
    min_value=5,
    max_value=20,
    value=10
)


# Recommendation button
if st.button("Recommend Movies"):

    if not movie_title.strip():

        st.warning(
            "Please enter a movie title."
        )

    else:

        recommendations = recommend_movie(
            movie_title,
            top_n
        )

        if recommendations is None:

            st.error(
                f"'{movie_title}' was not found "
                "in the dataset."
            )

        else:

            st.subheader(
                f"Movies similar to {movie_title.strip()}"
            )

            for i, row in recommendations.iterrows():

                st.write(
                    f"**{i + 1}. {row['title']}**"
                )

                st.caption(
                    f"Similarity score: "
                    f"{row['similarity_score']:.4f}"
                )