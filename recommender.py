import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os

def load_data():
    return pd.read_csv("data/books.csv")

def train_model():
    books = load_data()
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(books['description'])
    
    # Save model
    os.makedirs("data", exist_ok=True)
    pickle.dump(tfidf_matrix, open("data/model.pkl", "wb"))
    pickle.dump(tfidf, open("data/tfidf.pkl", "wb"))
    return tfidf_matrix

def get_recommendations(title, tfidf_matrix, books, n=5):
    try:
        idx = books[books['title'] == title].index[0]
    except:
        return []
        
    cosine_sim = cosine_similarity(tfidf_matrix[idx], tfidf_matrix)
    sim_scores = list(enumerate(cosine_sim[0]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:n+1]  # Skip self
    book_indices = [i[0] for i in sim_scores]
    return books.iloc[book_indices]