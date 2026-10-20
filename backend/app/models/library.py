from datetime import datetime, timezone
from .database import db

class LibraryEntry(db.Model):
    __tablename__ = 'library_entries'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False, default="demo_user", index=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False, index=True)
    status = db.Column(db.String(50), nullable=False, default="want_to_read") # 'want_to_read', 'currently_reading', 'completed', 'favorite'
    is_favorite = db.Column(db.Boolean, default=False)
    user_rating = db.Column(db.Integer, nullable=True) # 1-5
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        db.UniqueConstraint('user_id', 'book_id', name='uq_user_book'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'book_id': self.book_id,
            'status': self.status,
            'is_favorite': self.is_favorite,
            'user_rating': self.user_rating,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'book': self.book.to_dict() if self.book else None
        }
