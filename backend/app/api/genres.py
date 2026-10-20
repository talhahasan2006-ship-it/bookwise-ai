from flask import Blueprint, jsonify
from sqlalchemy import func
from backend.app.models import Book

genres_bp = Blueprint('genres', __name__, url_prefix='/api/genres')

@genres_bp.route('', methods=['GET'])
def get_genres():
    """
    Returns unique genres derived from the actual books dataset with book counts.
    """
    results = (
        Book.query.with_entities(Book.genre, func.count(Book.id))
        .group_by(Book.genre)
        .order_by(func.count(Book.id).desc())
        .all()
    )

    genres = [{'genre': g[0], 'count': g[1]} for g in results if g[0]]
    return jsonify({'genres': genres}), 200
