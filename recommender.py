import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rapidfuzz import process, fuzz


# Load our prepared movie dataset
movies = pd.read_csv("data/movies.csv")

# Fill empty values
movies = movies.fillna("")


# Create TF-IDF vectors
vectorizer = TfidfVectorizer(
    stop_words="english"
)

vectors = vectorizer.fit_transform(
    movies["tags"]
)


# Calculate cosine similarity
similarity = cosine_similarity(vectors)


# Find the closest movie title
def find_closest_title(movie_title):

    titles = movies["title"].tolist()

    result = process.extractOne(
        movie_title,
        titles,
        scorer=fuzz.partial_ratio
    )

    if result:

        matched_title = result[0]
        score = result[1]

        return matched_title, score

    return None, 0


# Recommend similar movies
def recommend_movies(movie_title, number=5):

    movie_indexes = movies[
        movies["title"].str.lower()
        == movie_title.lower()
    ].index

    if len(movie_indexes) == 0:
        return []

    movie_index = movie_indexes[0]

    similarity_scores = similarity[movie_index]

    similar_movies = list(
        enumerate(similarity_scores)
    )

    similar_movies = sorted(
        similar_movies,
        key=lambda x: x[1],
        reverse=True
    )

    recommendations = []

    for index, score in similar_movies[1:number + 1]:

        movie = movies.iloc[index]

        recommendations.append({
            "title": movie["title"],
            "score": round(float(score) * 100, 2),
            "genres": movie["genres"],
            "overview": movie["overview"],
            "cast": movie["cast"],
            "director": movie["director"]
        })

    return recommendations