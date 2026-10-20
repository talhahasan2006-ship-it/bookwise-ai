from flask import Blueprint, request, jsonify
from sqlalchemy import or_, desc, asc
from backend.app.models import db, Book
from backend.app.recommender import engine

books_bp = Blueprint('books', __name__, url_prefix='/api/books')

@books_bp.route('', methods=['GET'])
def get_books():
    """
    Returns paginated book catalog supporting search, filters, and sorting.
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)
    search_query = request.args.get('q', '', type=str).strip()
    genre = request.args.get('genre', '', type=str).strip()
    author = request.args.get('author', '', type=str).strip()
    min_rating = request.args.get('min_rating', 0.0, type=float)
    year_from = request.args.get('year_from', None, type=int)
    year_to = request.args.get('year_to', None, type=int)
    sort_by = request.args.get('sort_by', 'popular', type=str).strip()

    # Base query
    query = Book.query

    # Search filter
    if search_query:
        search_pattern = f"%{search_query}%"
        query = query.filter(
            or_(
                Book.title.ilike(search_pattern),
                Book.author.ilike(search_pattern),
                Book.genre.ilike(search_pattern),
                Book.description.ilike(search_pattern)
            )
        )

    # Genre filter
    if genre and genre.lower() != 'all':
        query = query.filter(Book.genre.ilike(f"%{genre}%"))

    # Author filter
    if author and author.lower() != 'all':
        query = query.filter(Book.author.ilike(f"%{author}%"))

    # Minimum rating filter
    if min_rating > 0.0:
        query = query.filter(Book.average_rating >= min_rating)

    # Year filter
    if year_from is not None:
        query = query.filter(Book.publication_year >= year_from)
    if year_to is not None:
        query = query.filter(Book.publication_year <= year_to)

    # Sorting
    if sort_by == 'highest_rated':
        query = query.order_by(desc(Book.average_rating))
    elif sort_by == 'title_asc':
        query = query.order_by(asc(Book.title))
    elif sort_by == 'year_desc':
        query = query.order_by(desc(Book.publication_year))
    elif sort_by == 'year_asc':
        query = query.order_by(asc(Book.publication_year))
    else: # Default: most popular (rating count)
        query = query.order_by(desc(Book.rating_count))

    paginated = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'books': [book.to_dict() for book in paginated.items],
        'total': paginated.total,
        'page': paginated.page,
        'per_page': paginated.per_page,
        'total_pages': paginated.pages,
        'has_prev': paginated.has_prev,
        'has_next': paginated.has_next
    }), 200

@books_bp.route('/<int:book_id>', methods=['GET'])
def get_book_details(book_id):
    """
    Returns full details for a specific book.
    """
    book = db.session.get(Book, book_id)
    if not book:
        return jsonify({'error': 'Book not found', 'book_id': book_id}), 404
    return jsonify({'book': book.to_dict()}), 200

@books_bp.route('/<int:book_id>/similar', methods=['GET'])
def get_similar_books(book_id):
    """
    Returns books similar to the requested book using the recommendation engine.
    """
    limit = request.args.get('limit', 6, type=int)
    min_rating = request.args.get('min_rating', 0.0, type=float)

    book = db.session.get(Book, book_id)
    if not book:
        return jsonify({'error': 'Book not found', 'book_id': book_id}), 404

    try:
        similar = engine.recommend(
            algorithm="hybrid",
            seed_book_id=book_id,
            min_rating=min_rating,
            top_n=limit
        )
        return jsonify({
            'source_book': book.to_dict(),
            'recommendations': similar
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
