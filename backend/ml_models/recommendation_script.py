import sys
import json
import pandas as pd
from pymongo import MongoClient
from sklearn.metrics.pairwise import cosine_similarity
import joblib

# Connexion à MongoDB
def get_movies_from_db():
    client = MongoClient("mongodb+srv://jeanalexistaddei:3AtAGveoDeHmxqNv@targetdummybdd.4jjdl.mongodb.net/MovieRandomizer?retryWrites=true&w=majority")
    db = client.MovieRandomizer
    collection = db.movies
    movies = pd.DataFrame(list(collection.find()))
    return movies

# Générer des recommandations
def recommend_movies(watched_titles, model_path, tfidf_path):
    # Charger les modèles
    tfidf = joblib.load(tfidf_path)

    # Charger les films depuis MongoDB
    movies = get_movies_from_db()

    # Préparer les données pour TF-IDF
    genres_matrix = tfidf.transform(movies['genres'].apply(lambda x: ' '.join(x)))

    # Trouver les indices des films vus
    watched_indices = movies[movies['title'].isin(watched_titles)].index.tolist()

    if not watched_indices:
        return []

    # Calculer les similarités cosinus entre les films vus et tous les films
    watched_vectors = genres_matrix[watched_indices]
    similarities = cosine_similarity(watched_vectors, genres_matrix)

    # Moyenne des similarités pour les films vus
    mean_similarities = similarities.mean(axis=0)

    # Trier les films par similarité
    similar_indices = mean_similarities.argsort()[::-1]

    # Exclure les films déjà vus
    recommended_indices = [i for i in similar_indices if i not in watched_indices][:10]

    # Retourner les titres des films recommandés
    recommended_movies = movies.iloc[recommended_indices]['title'].tolist()
    return recommended_movies

if __name__ == "__main__":
    # Récupérer les arguments depuis Node.js
    watched_titles = json.loads(sys.argv[1])
    model_path = sys.argv[2]
    tfidf_path = sys.argv[3]

    # Générer des recommandations
    recommendations = recommend_movies(watched_titles, model_path, tfidf_path)

    # Retourner les recommandations sous forme de JSON
    print(json.dumps(recommendations))
