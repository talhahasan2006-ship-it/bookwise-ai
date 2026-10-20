from flask import Blueprint, request, jsonify
from backend.app.models import db, Book
from backend.app.recommender import engine

recs_bp = Blueprint('recommendations', __name__, url_prefix='/api/recommendations')

@recs_bp.route('/content/<int:book_id>', methods=['GET'])
def get_content_recommendations(book_id):
    """
    Direct TF-IDF & Cosine Similarity content recommendations.
    """
    limit = request.args.get('limit', 8, type=int)
    min_rating = request.args.get('min_rating', 0.0, type=float)
    genre = request.args.get('genre', None, type=str)

    book = db.session.get(Book, book_id)
    if not book:
        return jsonify({'error': 'Book not found', 'book_id': book_id}), 404

    try:
        results = engine.recommend(
            algorithm="content",
            seed_book_id=book_id,
            preferred_genres=[genre] if genre else None,
            min_rating=min_rating,
            top_n=limit
        )
        return jsonify({
            'seed_book': book.to_dict(),
            'algorithm': 'Content-Based Filtering (TF-IDF & Cosine Similarity)',
            'recommendations': results
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@recs_bp.route('/popular', methods=['GET'])
def get_popular_recommendations():
    """
    Bayesian Weighted Rating popularity recommendations.
    """
    limit = request.args.get('limit', 8, type=int)
    genre = request.args.get('genre', None, type=str)

    try:
        results = engine.recommend(
            algorithm="popular",
            preferred_genres=[genre] if genre else None,
            top_n=limit
        )
        return jsonify({
            'algorithm': 'Bayesian Weighted Popularity Ranking',
            'recommendations': results
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@recs_bp.route('/personalized', methods=['POST'])
def get_personalized_recommendations():
    """
    Interactive multi-algorithm recommendation generator.
    Accepts:
    - seed_book_id (optional)
    - preferred_genres (list of strings)
    - min_rating (float)
    - limit (int)
    - algorithm ("hybrid" | "content" | "collaborative" | "popular")
    """
    data = request.get_json(silent=True) or {}
    seed_book_id = data.get('seed_book_id')
    preferred_genres = data.get('preferred_genres', [])
    min_rating = float(data.get('min_rating', 0.0))
    limit = int(data.get('limit', 8))
    algorithm = data.get('algorithm', 'hybrid').lower()

    if seed_book_id is not None:
        try:
            seed_book_id = int(seed_book_id)
            seed_book = db.session.get(Book, seed_book_id)
            seed_book_dict = seed_book.to_dict() if seed_book else None
        except ValueError:
            seed_book_dict = None
    else:
        seed_book_dict = None

    try:
        recommendations = engine.recommend(
            algorithm=algorithm,
            seed_book_id=seed_book_id,
            preferred_genres=preferred_genres,
            min_rating=min_rating,
            top_n=limit
        )

        return jsonify({
            'algorithm': algorithm,
            'seed_book': seed_book_dict,
            'filters': {
                'preferred_genres': preferred_genres,
                'min_rating': min_rating,
                'limit': limit
            },
            'count': len(recommendations),
            'recommendations': recommendations
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
