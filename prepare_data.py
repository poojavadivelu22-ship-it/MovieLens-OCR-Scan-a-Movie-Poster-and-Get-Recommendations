import pandas as pd
import ast

# Load the two CSV files
movies = pd.read_csv("data/tmdb_5000_movies.csv")
credits = pd.read_csv("data/tmdb_5000_credits.csv")

# Rename movie_id to id
credits = credits.rename(columns={"movie_id": "id"})

# Merge both datasets
movies = movies.merge(credits, on="id")


# Get names from genres and keywords
def get_names(text):
    try:
        data = ast.literal_eval(text)
        return " ".join(item["name"] for item in data)
    except:
        return ""


movies["genres"] = movies["genres"].apply(get_names)
movies["keywords"] = movies["keywords"].apply(get_names)


# Get first 5 cast members
def get_cast(text):
    try:
        data = ast.literal_eval(text)
        return " ".join(item["name"] for item in data[:5])
    except:
        return ""


movies["cast"] = movies["cast"].apply(get_cast)


# Get director
def get_director(text):
    try:
        data = ast.literal_eval(text)

        for item in data:
            if item["job"] == "Director":
                return item["name"]

        return ""
    except:
        return ""


movies["director"] = movies["crew"].apply(get_director)


# Select required columns
movies = movies[
    [
        "id",
        "title_x",
        "genres",
        "keywords",
        "overview",
        "cast",
        "director"
    ]
]


# Rename title column
movies = movies.rename(columns={"title_x": "title"})


# Fill empty values
movies = movies.fillna("")


# Create tags
movies["tags"] = (
    movies["genres"] + " "
    + movies["keywords"] + " "
    + movies["overview"] + " "
    + movies["cast"] + " "
    + movies["director"]
)


# Create movies.csv
movies.to_csv("data/movies.csv", index=False)

print("Movie dataset created successfully!")
print(f"Total movies: {len(movies)}")