from fastapi import FastAPI
from database import get_db
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()


# CORS ko enable karna frontend ke liye
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Sab origins allow karna (Production me specific origin dena)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/news")
def fetch_news_articles():
    """Fetch ALL news articles from the database."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT title, sentiment_label, sentiment_score, source, url 
        FROM news 
        ORDER BY published_at DESC 
    """)  # ✅ LIMIT ko hata diya
    articles = cur.fetchall()
    conn.close()

    return [
        {
            "title": row[0],
            "sentiment_label": row[1],
            "sentiment_score": row[2],
            "source": row[3],
            "url": row[4]
        }
        for row in articles
    ]
