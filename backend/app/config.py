import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Detect Vercel / Serverless environment
is_vercel = bool(os.environ.get("VERCEL") or os.environ.get("AWS_LAMBDA_FUNCTION_NAME"))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "bookwise-ai-dev-secret-key-2026")
    
    # SQLite on Vercel must use /tmp since root filesystem is read-only
    _default_db = "sqlite:////tmp/bookwise.db" if is_vercel else f"sqlite:///{os.path.join(BASE_DIR, 'backend', 'app', 'bookwise.db')}"
    _db_url = os.environ.get("DATABASE_URL", _default_db)
    if _db_url.startswith("postgres://"):
        _db_url = _db_url.replace("postgres://", "postgresql://", 1)
        
    SQLALCHEMY_DATABASE_URI = _db_url
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
        "http://127.0.0.1:3000",
        "*"
    ]
