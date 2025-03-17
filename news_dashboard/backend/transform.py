import re
import nltk
from nltk.corpus import stopwords
from transformers import pipeline

nltk.download("stopwords")
stop_words = set(stopwords.words("english"))

# Load Sentiment Model
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")

def clean_text(text):
    """Clean text by removing special characters and stopwords."""
    text = re.sub(r"[^a-zA-Z\s]", "", text).lower()
    words = [word for word in text.split() if word not in stop_words]
    return " ".join(words)

def get_sentiment(text):
    """Analyze sentiment and detect neutral categories."""
    if len(text.strip()) == 0:
        return "neutral", 0.0  # Handle empty text safely

    result = sentiment_pipeline(text[:512])[0]  # BERT limit is 512 tokens
    sentiment = result["label"]
    score = result["score"]

    # Convert scores to include "neutral"
    if sentiment == "POSITIVE":
        if score > 0.8:
            return "positive", score
        else:
            return "neutral", score
    elif sentiment == "NEGATIVE":
        if score > 0.8:
            return "negative", -score
        else:
            return "neutral", -score
    else:
        return "neutral", 0.0
