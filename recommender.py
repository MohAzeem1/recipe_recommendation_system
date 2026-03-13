import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
df = pd.read_csv("recipes_small.csv")

df['features'] =  df['ingredients'].astype(str) + " " + df['name'].astype(str)

# Fill missing names
df['name'] = df['name'].fillna('')

# TF-IDF Vectorization
tfidf = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf.fit_transform(df["features"])


# Recipe name recommendation
def recommend_recipes(recipe_name, top_n=5):

    recipe_name = recipe_name.lower()

    matches = df[df["name"].str.lower().str.contains(recipe_name, na=False)]

    if matches.empty:
        return []

    idx = matches.index[0]

    recipe_vector = tfidf_matrix[idx]

    similarity_scores = cosine_similarity(recipe_vector, tfidf_matrix).flatten()

    similar_indices = similarity_scores.argsort()[-top_n-1:-1][::-1]

    return df["name"].iloc[similar_indices].tolist()


# Ingredient based recommendation
def recommend_by_ingredients(ingredients, top_n=5):

    ingredients = ingredients.lower()

    query_vector = tfidf.transform([ingredients])

    similarity_scores = cosine_similarity(query_vector, tfidf_matrix).flatten()

    similar_indices = similarity_scores.argsort()[-top_n:][::-1]

    return df["name"].iloc[similar_indices].tolist()
