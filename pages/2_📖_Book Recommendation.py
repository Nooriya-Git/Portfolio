import streamlit as st
import pandas as pd
from recommender import load_data, get_recommendations
from api_utils import get_goodreads_reviews
import pickle

# Load data and model
@st.cache_resource
def load_model():
    books = load_data()
    tfidf_matrix = pickle.load(open("data/model.pkl", "rb"))
    return books, tfidf_matrix

books, tfidf_matrix = load_model()

# UI Layout
st.title("📚 Book Recommendation Engine")
st.markdown("Discover your next favorite book based on content similarity")

# Book selection
selected_book = st.selectbox(
    "Choose a book you like:",
    books['title'].values
)

# Show book info
if selected_book:
    book_info = books[books['title'] == selected_book].iloc[0]
    st.subheader(book_info['title'])
    st.caption(f"by {book_info['author']} | Genre: {book_info['genre']}")
    
    with st.expander("📖 Book Details"):
        st.write(book_info['description'])
        
        st.markdown("**Reviews from Goodreads:**")
        reviews = get_goodreads_reviews(book_info['title'])
        for review in reviews:
            st.write(review)

# Get recommendations
if st.button("Get Recommendations"):
    recommendations = get_recommendations(selected_book, tfidf_matrix, books)
    
    st.subheader("Recommended Books:")
    for _, row in recommendations.iterrows():
        with st.container():
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image("./data/books.png", width=100)
            with col2:
                st.subheader(row['title'])
                st.caption(f"by {row['author']} | {row['genre']}")
                with st.expander("See details"):
                    st.write(row['description'])
