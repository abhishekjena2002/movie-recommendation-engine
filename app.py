from http.client import responses
from http.client import responses

import streamlit as st
import pickle
import pandas as pd
import requests
import time



if "poster_cache" not in st.session_state:
    st.session_state.poster_cache = {}

# ======================================
# TMDB API KEY (PUT YOUR KEY HERE)
# ======================================
API_KEY = "a5c5ffa5d63d50dccbe2589e49d14073"

@st.cache_data(show_spinner=False)
def cached_fetch_poster(movie_id, movie_title):
    return fetch_poster(movie_id, movie_title)

# ======================================
# FUNCTION: FETCH MOVIE POSTER
# ======================================
def fetch_poster(movie_id, movie_title):
    key = f"{movie_id}_{movie_title}"

    # ✅ Return cached poster if exists
    if key in st.session_state.poster_cache:
        return st.session_state.poster_cache[key]

    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    for attempt in range(2):  # 🔁 TRY TWICE
        try:
            # 1️⃣ TRY BY MOVIE ID
            url = f"https://api.themoviedb.org/3/movie/{int(movie_id)}"
            params = {"api_key": API_KEY, "language": "en-US"}
            data = requests.get(url, headers=headers, params=params, timeout=10).json()

            if data.get("poster_path"):
                poster = "https://image.tmdb.org/t/p/w500/" + data["poster_path"]
                st.session_state.poster_cache[key] = poster
                return poster
        except:
            pass

        try:
            # 2️⃣ SEARCH BY TITLE
            search_url = "https://api.themoviedb.org/3/search/movie"
            params = {
                "api_key": API_KEY,
                "query": movie_title,
                "include_adult": True,
                "language": "en-US"
            }
            data = requests.get(search_url, headers=headers, params=params, timeout=10).json()

            for m in data.get("results", []):
                if m.get("poster_path"):
                    poster = "https://image.tmdb.org/t/p/w500/" + m["poster_path"]
                    st.session_state.poster_cache[key] = poster
                    return poster
        except:
            pass

        try:
            # 3️⃣ CLEAN TITLE SEARCH
            params["query"] = clean_title(movie_title)
            data = requests.get(search_url, headers=headers, params=params, timeout=10).json()

            for m in data.get("results", []):
                if m.get("poster_path"):
                    poster = "https://image.tmdb.org/t/p/w500/" + m["poster_path"]
                    st.session_state.poster_cache[key] = poster
                    return poster
        except:
            pass

        # ⏳ WAIT A BIT BEFORE RETRY
        time.sleep(0.2)

    # ❌ After 2 attempts, give up
    return None
# ======================================
# FUNCTION: RECOMMEND MOVIES
# ======================================
def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].id   # column name is 'id'
        recommended_movies.append(movies.iloc[i[0]].title)
        movie_title = movies.iloc[i[0]].title
        recommended_posters.append(fetch_poster(movie_id, movie_title))

    return recommended_movies, recommended_posters


# ======================================
# LOAD DATA
# ======================================
movies_dict = pickle.load(open("movie_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open("similarity.pkl", "rb"))


# ======================================
# STREAMLIT UI
# ======================================
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title("🎬 Movie Recommendation System")

selected_movie = st.selectbox(
    "Select a movie",
    movies["title"].values
)

if st.button("Recommend"):
    with st.spinner("Finding best matches..."):
        names, posters = recommend(selected_movie)


    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            # FIXED HEIGHT TITLE (ALIGNMENT FIX)
            st.markdown(
                f"""
                <div style="
                    height: 60px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    text-align: center;
                    font-weight: 600;
                    font-size: 16px;
                ">
                    {names[i]}
                </div>
                """,
                unsafe_allow_html=True
            )

            # POSTER
            st.image(
                posters[i] if posters[i] else "https://via.placeholder.com/500x750?text=Loading...",
                use_container_width=True
            )




