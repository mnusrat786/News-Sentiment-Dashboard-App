from urllib.parse import urlparse
from database import get_db

def fetch_news_articles():
    """Fetch latest news articles and normalize sources."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT title, sentiment_label, sentiment_score, source, url 
        FROM news 
        ORDER BY published_at DESC 
    """)

    articles = cur.fetchall()
    conn.close()

    def extract_source(url):
        """Extract source name from URL and map to proper source names."""
        try:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc.replace("www.", "") if parsed_url.netloc else "Unknown"
            
            # Define readable names for common news domains
            domain_mapping = {
                "bbc.com": "BBC News",
                "cnn.com": "CNN",
                "nytimes.com": "The New York Times",
                "theguardian.com": "The Guardian",
                "aljazeera.com": "Al Jazeera",
                "reuters.com": "Reuters",
                "foxnews.com": "Fox News",
                "washingtonpost.com": "The Washington Post",
                "npr.org": "NPR",
                "forbes.com": "Forbes",
                "bloomberg.com": "Bloomberg",
                "cbsnews.com": "CBS News",
                "nbcnews.com": "NBC News",
                "abcnews.go.com": "ABC News",
                "politico.com": "Politico",
                "theverge.com": "The Verge"
            }
            return domain_mapping.get(domain, domain)  # Use readable name or fallback to domain
        except:
            return "Unknown"

    processed_articles = []
    
    for row in articles:
        # 🔥 Fix: Replace "Unknown" sources with extracted sources from URLs
        source = row[3].strip() if row[3] and row[3].strip().lower() != "unknown" else extract_source(row[4])
        
        processed_articles.append({
            "title": row[0],
            "sentiment_label": row[1],
            "sentiment_score": row[2],
            "source": source,  # 🔥 Now stores extracted source properly
            "url": row[4]
        })
    
    # 🔹 DEBUG: Print first 10 sources after processing
    print("🔹 DEBUG: First 10 sources after processing:", [a["source"] for a in processed_articles[:10]])

    return processed_articles
