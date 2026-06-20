
# Movie Recommendation Engine

## Overview

The Movie Recommendation Engine is a content-based recommendation system that suggests movies similar to a user's selected movie. The system analyzes movie metadata such as genres, keywords, cast, and overview to identify similarities between movies and provide personalized recommendations.

## Features

* Recommend similar movies based on user selection.
* Content-based filtering using movie metadata.
* Interactive web interface built with Streamlit.
* Fast movie similarity search using Cosine Similarity.
* Movie posters fetched using TMDB API.

## Technologies Used

* Python
* Pandas
* NumPy
* Scikit-learn
* Streamlit
* TMDB API

## Dataset

The project uses the TMDB 5000 Movies Dataset containing:

* Movie titles
* Genres
* Cast
* Crew
* Keywords
* Movie overviews

## Project Workflow

### 1. Data Collection

Movie datasets are loaded and merged using movie IDs.

### 2. Data Preprocessing

* Handle missing values
* Extract relevant features
* Combine features into a single text column

### 3. Feature Engineering

Text features are converted into numerical vectors using CountVectorizer.

### 4. Similarity Calculation

Cosine Similarity is used to calculate similarity scores between movies.

### 5. Recommendation Generation

When a user selects a movie, the system identifies the most similar movies and displays recommendations.

## How to Run

1. Clone the repository:

```bash
git clone <repository-url>
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the Streamlit application:

```bash
streamlit run app.py
```

## Results

* Generates top movie recommendations based on similarity scores.
* Provides an interactive and user-friendly recommendation interface.
* Achieves fast recommendation generation for large movie datasets.

## Future Enhancements

* Hybrid recommendation system.
* User-based collaborative filtering.
* Movie rating prediction.
* Personalized user profiles.

## Author
Abhishek 

