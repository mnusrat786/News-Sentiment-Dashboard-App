import psycopg2
from config import DB_CONFIG

def insert_into_db(data):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    for item in data:
        cur.execute("""
            INSERT INTO news (title, content, sentiment_label, sentiment_score, source, url, published_at)
            VALUES (%s, %s, %s, %s, %s, %s, NOW())
            """, (item["title"], item["content"], item["sentiment_label"], item["sentiment_score"], item["source"], item["url"]))

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    sample_data = [
        {
            "title": "Sample News",
            "content": "This is a sample content",
            "sentiment_label": "positive",
            "sentiment_score": 0.5,
            "source": "Test"
        }
    ]
    insert_into_db(sample_data)
