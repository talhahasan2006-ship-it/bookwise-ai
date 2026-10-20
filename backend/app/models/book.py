from .database import db

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, index=True)
    author = db.Column(db.String(255), nullable=False, index=True)
    genre = db.Column(db.String(100), nullable=False, index=True)
    publication_year = db.Column(db.Integer, nullable=True)
    publisher = db.Column(db.String(255), nullable=True)
    isbn = db.Column(db.String(30), nullable=True, unique=True)
    average_rating = db.Column(db.Float, default=0.0)
    rating_count = db.Column(db.Integer, default=0)
    description = db.Column(db.Text, nullable=True)
    cover_url = db.Column(db.String(500), nullable=True)

    # Relationships
    library_entries = db.relationship('LibraryEntry', backref='book', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'book_id': self.id,
            'title': self.title,
            'author': self.author,
            'genre': self.genre,
            'publication_year': self.publication_year,
            'publisher': self.publisher,
            'isbn': self.isbn,
            'average_rating': round(float(self.average_rating), 2) if self.average_rating else 0.0,
            'rating_count': self.rating_count,
            'description': self.description,
            'cover_url': self.cover_url
        }
