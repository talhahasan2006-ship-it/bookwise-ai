import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "bookwise-ai-dev-secret-key-2026")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(BASE_DIR, 'backend', 'app', 'bookwise.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    DATASETS_DIR = os.path.join(BASE_DIR, "datasets")
    BOOKS_CSV = os.path.join(DATASETS_DIR, "books.csv")
    RATINGS_CSV = os.path.join(DATASETS_DIR, "ratings.csv")

    # Recommender defaults
    BAYESIAN_MIN_RATINGS_PERCENTILE = 0.50
    DEFAULT_RECOMMENDATION_LIMIT = 8
    CORS_ORIGINS = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]
