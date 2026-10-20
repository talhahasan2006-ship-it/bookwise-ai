from flask import Blueprint, request, jsonify
from backend.app.models import db, LibraryEntry, Book

library_bp = Blueprint('library', __name__, url_prefix='/api/library')

DEMO_USER_ID = "demo_user"

@library_bp.route('', methods=['GET'])
def get_library():
    """
    Returns library entries for the local demo user profile grouped with book details.
    """
    status_filter = request.args.get('status', None)
    favorites_only = request.args.get('favorites', 'false').lower() == 'true'

    query = LibraryEntry.query.filter_by(user_id=DEMO_USER_ID)
    if status_filter and status_filter.lower() != 'all':
        query = query.filter_by(status=status_filter)
    if favorites_only:
        query = query.filter_by(is_favorite=True)

    entries = query.order_by(LibraryEntry.updated_at.desc()).all()
    return jsonify({
        'user_profile': {
            'username': 'Demo Scholar',
            'user_id': DEMO_USER_ID,
            'is_demo': True,
            'note': 'Local Academic Demonstration Profile. Entries are securely persisted to local SQLite database.'
        },
        'count': len(entries),
        'entries': [e.to_dict() for e in entries]
    }), 200

@library_bp.route('', methods=['POST'])
def add_or_update_library_entry():
    """
    Adds or updates a book entry in the demo user library.
    Body JSON:
    - book_id (required)
    - status ('want_to_read', 'currently_reading', 'completed')
    - is_favorite (bool)
    - user_rating (int 1-5, optional)
    - notes (string, optional)
    """
    data = request.get_json(silent=True) or {}
    book_id = data.get('book_id')

    if not book_id:
        return jsonify({'error': 'book_id is required'}), 400

    book = db.session.get(Book, book_id)
    if not book:
        return jsonify({'error': 'Book does not exist', 'book_id': book_id}), 404

    entry = LibraryEntry.query.filter_by(user_id=DEMO_USER_ID, book_id=book_id).first()

    if not entry:
        entry = LibraryEntry(
            user_id=DEMO_USER_ID,
            book_id=book_id,
            status=data.get('status', 'want_to_read'),
            is_favorite=bool(data.get('is_favorite', False)),
            user_rating=data.get('user_rating'),
            notes=data.get('notes', '')
        )
        db.session.add(entry)
    else:
        if 'status' in data:
            entry.status = data['status']
        if 'is_favorite' in data:
            entry.is_favorite = bool(data['is_favorite'])
        if 'user_rating' in data:
            entry.user_rating = data['user_rating']
        if 'notes' in data:
            entry.notes = data['notes']

    db.session.commit()
    return jsonify({
        'message': 'Library updated successfully',
        'entry': entry.to_dict()
    }), 200

@library_bp.route('/<int:book_id>', methods=['DELETE'])
def remove_from_library(book_id):
    """
    Removes a book from the demo user's library.
    """
    entry = LibraryEntry.query.filter_by(user_id=DEMO_USER_ID, book_id=book_id).first()
    if not entry:
        return jsonify({'error': 'Entry not found in library', 'book_id': book_id}), 404

    db.session.delete(entry)
    db.session.commit()
    return jsonify({
        'message': f'Book {book_id} removed from library',
        'book_id': book_id
    }), 200
