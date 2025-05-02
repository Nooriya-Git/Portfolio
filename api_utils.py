import requests
from bs4 import BeautifulSoup
import wikipediaapi

def get_wikipedia_summary(title):
    wiki_wiki = wikipediaapi.Wikipedia('en')
    page = wiki_wiki.page(title)
    if page.exists():
        return page.summary[:500] + "..."  # Truncate summary
    return "No Wikipedia summary available"

def get_goodreads_reviews(book_title):
    try:
        url = f"https://www.goodreads.com/search?q={book_title.replace(' ', '+')}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find first search result link
        first_result = soup.find('a', class_='bookTitle')
        if not first_result:
            return []
            
        book_url = "https://www.goodreads.com" + first_result['href']
        response = requests.get(book_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract reviews
        reviews = []
        review_elements = soup.find_all('div', class_='reviewText')
        for i, review in enumerate(review_elements[:3]):  # Get top 3 reviews
            reviews.append(f"Review {i+1}: {review.get_text(strip=True)[:300]}...")
        return reviews
    except:
        return ["Could not load reviews"]