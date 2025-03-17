from fastapi import APIRouter
from database import get_db

router = APIRouter()

@router.get("/news")
def get_news():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT title, sentiment_label, sentiment_score, source, url FROM news ORDER BY published_at DESC LIMIT 50")
    articles = cur.fetchall()
    conn.close()

    return [
        {"title": row[0], "sentiment_label": row[1], "sentiment_score": row[2], "source": row[3], "url": row[4]}
        for row in articles
    ]
