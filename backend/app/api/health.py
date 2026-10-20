from flask import Blueprint, jsonify
from backend.app.models import Book
from backend.app.recommender import engine

health_bp = Blueprint('health', __name__, url_prefix='/api/health')

@health_bp.route('', methods=['GET'])
def health_check():
    """
    Returns system health, database readiness, and recommender engine status.
    """
    total_books = Book.query.count()
    return jsonify({
        'status': 'healthy',
        'application': 'BookWise AI Backend',
        'database_connected': True,
        'total_books_in_db': total_books,
        'recommender_engine_initialized': engine.initialized,
        'algorithms_available': [
            'Content-Based Filtering (TF-IDF + Cosine Similarity)',
            'Collaborative Filtering (Item-Based Interaction Vectors)',
            'Bayesian Weighted Popularity Ranking',
            'Hybrid Linear Combination Recommender'
        ]
    }), 200
