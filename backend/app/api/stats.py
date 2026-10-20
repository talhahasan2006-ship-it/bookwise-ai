from flask import Blueprint, jsonify
from sqlalchemy import func
from backend.app.models import Book, Rating

stats_bp = Blueprint('stats', __name__, url_prefix='/api/stats')

@stats_bp.route('', methods=['GET'])
def get_stats():
    """
    Computes and returns real statistics derived from the loaded dataset.
    No hardcoded or fabricated metrics.
    """
    total_books = Book.query.count()
    if total_books == 0:
        return jsonify({
            'total_books': 0,
            'unique_authors': 0,
            'unique_genres': 0,
            'average_rating': 0.0,
            'total_ratings_volume': 0,
            'genres_distribution': [],
            'ratings_distribution': [],
            'publication_year_distribution': [],
            'top_rated_books': []
        }), 200

    unique_authors = Book.query.with_entities(func.count(func.distinct(Book.author))).scalar() or 0
    unique_genres = Book.query.with_entities(func.count(func.distinct(Book.genre))).scalar() or 0
    avg_rating = Book.query.with_entities(func.avg(Book.average_rating)).scalar() or 0.0
    total_ratings_vol = Book.query.with_entities(func.sum(Book.rating_count)).scalar() or 0

    # 1. Genres distribution
    genres_data = (
        Book.query.with_entities(Book.genre, func.count(Book.id))
        .group_by(Book.genre)
        .order_by(func.count(Book.id).desc())
        .all()
    )
    genres_distribution = [{'genre': row[0], 'count': row[1]} for row in genres_data]

    # 2. Rating distribution bins (1.0-3.0, 3.0-3.5, 3.5-4.0, 4.0-4.5, 4.5-5.0)
    bins = [
        {'range': '3.0 - 3.5', 'count': Book.query.filter(Book.average_rating >= 3.0, Book.average_rating < 3.5).count()},
        {'range': '3.5 - 3.9', 'count': Book.query.filter(Book.average_rating >= 3.5, Book.average_rating < 4.0).count()},
        {'range': '4.0 - 4.2', 'count': Book.query.filter(Book.average_rating >= 4.0, Book.average_rating < 4.2).count()},
        {'range': '4.2 - 4.5', 'count': Book.query.filter(Book.average_rating >= 4.2, Book.average_rating < 4.5).count()},
        {'range': '4.5 - 5.0', 'count': Book.query.filter(Book.average_rating >= 4.5).count()},
    ]

    # 3. Publication Year eras / decades
    eras = [
        {'era': 'Pre-1950 (Classics)', 'count': Book.query.filter(Book.publication_year < 1950).count()},
        {'era': '1950 - 1979 (Golden Age)', 'count': Book.query.filter(Book.publication_year >= 1950, Book.publication_year < 1980).count()},
        {'era': '1980 - 1999 (Cyberpunk / Modern)', 'count': Book.query.filter(Book.publication_year >= 1980, Book.publication_year < 2000).count()},
        {'era': '2000 - 2014 (Digital Era)', 'count': Book.query.filter(Book.publication_year >= 2000, Book.publication_year < 2015).count()},
        {'era': '2015 - Present (AI Revolution)', 'count': Book.query.filter(Book.publication_year >= 2015).count()},
    ]

    # 4. Top Rated Books
    top_rated_books = (
        Book.query.order_by(Book.average_rating.desc(), Book.rating_count.desc())
        .limit(6)
        .all()
    )

    # 5. User interaction matrix stats
    total_user_ratings = Rating.query.count()
    unique_active_users = Rating.query.with_entities(func.count(func.distinct(Rating.user_id))).scalar() or 0

    return jsonify({
        'total_books': total_books,
        'unique_authors': unique_authors,
        'unique_genres': unique_genres,
        'average_rating': round(float(avg_rating), 2),
        'total_ratings_volume': int(total_ratings_vol),
        'collaborative_ratings_count': total_user_ratings,
        'unique_active_users': unique_active_users,
        'genres_distribution': genres_distribution,
        'ratings_distribution': bins,
        'publication_era_distribution': eras,
        'top_rated_books': [b.to_dict() for b in top_rated_books]
    }), 200
