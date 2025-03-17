import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
NYT_KEY = os.getenv("NYT_KEY")
GNEWS_KEY = os.getenv("GNEWS_KEY")
CURRENTS_API_KEY = os.getenv("CURRENTS_API_KEY")
GUARDIAN_API_KEY = os.getenv("GUARDIAN_API_KEY")


def fetch_newsapi():
    """Fetch news from NewsAPI."""
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWSAPI_KEY}"
    response = requests.get(url)
    data = response.json()
    
    articles = []
    if "articles" in data:
        for item in data["articles"]:
            articles.append({
                "title": item.get("title"),
                "description": item.get("description"),
                "source": item.get("source", {}).get("name", "Unknown"),
                "url": item.get("url")  # Ensure URL is extracted
            })
    
    return articles



def fetch_nyt():
    all_articles = []
    page = 0  # NYT starts from page 0
    max_pages = 5

    while page < max_pages:
        url = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q=technology&page={page}&api-key={os.getenv('NYT_KEY')}"
        response = requests.get(url).json()

        articles = response.get("response", {}).get("docs", [])
        if not articles:
            break

        all_articles.extend(articles)
        page += 1

    print(f"📰 NYTimes returned: {len(all_articles)} articles")
    return all_articles



def fetch_gnews():
    url = f"https://gnews.io/api/v4/top-headlines?token={os.getenv('GNEWS_KEY')}&max=100"
    response = requests.get(url).json()
    articles = response.get("articles", [])
    print(f"📰 GNews returned: {len(articles)} articles")
    return articles



def fetch_currents():
    all_articles = []
    page = 1
    limit = 100  # Max allowed
    max_pages = 3

    while page <= max_pages:
        url = f"https://api.currentsapi.services/v1/latest-news?apiKey={os.getenv('CURRENTS_API_KEY')}&page={page}&limit={limit}"
        response = requests.get(url).json()

        articles = response.get("news", [])
        if not articles:
            break

        all_articles.extend(articles)
        page += 1

    print(f"📰 Currents API returned: {len(all_articles)} articles")
    return all_articles



def fetch_guardian():
    all_articles = []
    page = 1
    page_size = 100
    max_pages = 3

    while page <= max_pages:
        url = f"https://content.guardianapis.com/search?page={page}&page-size={page_size}&api-key={os.getenv('GUARDIAN_API_KEY')}"
        response = requests.get(url).json()

        articles = response.get("response", {}).get("results", [])
        if not articles:
            break

        all_articles.extend(articles)
        page += 1

    print(f"📰 The Guardian returned: {len(all_articles)} articles")
    return all_articles

