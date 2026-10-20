import os
import pandas as pd
from backend.app.models import db, Book, Rating

def load_data(app=None):
    """
    Loads books and ratings from CSV into pandas DataFrames,
    cleaning nulls and synchronizing with SQLite database if needed.
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    books_csv = os.path.join(base_dir, "datasets", "books.csv")
    ratings_csv = os.path.join(base_dir, "datasets", "ratings.csv")

    if not os.path.exists(books_csv):
        raise FileNotFoundError(f"Books dataset not found at {books_csv}. Please run scripts/seed_dataset.py.")

    df_books = pd.read_csv(books_csv)
    
    # Clean and sanitize fields
    df_books['book_id'] = pd.to_numeric(df_books['book_id'], errors='coerce').fillna(0).astype(int)
    df_books['title'] = df_books['title'].fillna('Untitled').astype(str)
    df_books['author'] = df_books['author'].fillna('Unknown Author').astype(str)
    df_books['genre'] = df_books['genre'].fillna('General').astype(str)
    df_books['publication_year'] = pd.to_numeric(df_books['publication_year'], errors='coerce').fillna(2000).astype(int)
    df_books['publisher'] = df_books['publisher'].fillna('Independent').astype(str)
    df_books['isbn'] = df_books['isbn'].fillna('').astype(str)
    df_books['average_rating'] = pd.to_numeric(df_books['average_rating'], errors='coerce').fillna(4.0).astype(float)
    df_books['rating_count'] = pd.to_numeric(df_books['rating_count'], errors='coerce').fillna(100).astype(int)
    df_books['description'] = df_books['description'].fillna('').astype(str)
    df_books['cover_url'] = df_books['cover_url'].fillna('').astype(str)

    # Load ratings
    if os.path.exists(ratings_csv):
        df_ratings = pd.read_csv(ratings_csv)
        df_ratings['user_id'] = pd.to_numeric(df_ratings['user_id'], errors='coerce').astype(int)
        df_ratings['book_id'] = pd.to_numeric(df_ratings['book_id'], errors='coerce').astype(int)
        df_ratings['rating'] = pd.to_numeric(df_ratings['rating'], errors='coerce').astype(float)
    else:
        df_ratings = pd.DataFrame(columns=['user_id', 'book_id', 'rating', 'timestamp'])

    # Sync to SQLite if DB is empty (non-fatal if DB unavailable on serverless)
    if app:
        try:
            with app.app_context():
                if Book.query.count() == 0:
                    print("Seeding SQLite database with books from CSV...")
                    book_objects = []
                    for _, row in df_books.iterrows():
                        book = Book(
                            id=int(row['book_id']),
                            title=row['title'],
                            author=row['author'],
                            genre=row['genre'],
                            publication_year=int(row['publication_year']),
                            publisher=row['publisher'],
                            isbn=row['isbn'],
                            average_rating=float(row['average_rating']),
                            rating_count=int(row['rating_count']),
                            description=row['description'],
                            cover_url=row['cover_url']
                        )
                        book_objects.append(book)
                    db.session.bulk_save_objects(book_objects)
                    db.session.commit()
                    print(f"Successfully seeded {len(book_objects)} books to SQLite.")

                if Rating.query.count() == 0 and not df_ratings.empty:
                    print("Seeding ratings into SQLite...")
                    rating_objects = []
                    for _, row in df_ratings.head(5000).iterrows():
                        r = Rating(
                            user_id=int(row['user_id']),
                            book_id=int(row['book_id']),
                            rating=float(row['rating']),
                            timestamp=int(row.get('timestamp', 0)) if pd.notnull(row.get('timestamp')) else None
                        )
                        rating_objects.append(r)
                    db.session.bulk_save_objects(rating_objects)
                    db.session.commit()
                    print(f"Successfully seeded {len(rating_objects)} ratings to SQLite.")
        except Exception as db_err:
            print(f"DB seeding/sync skipped (expected if DB unavailable on serverless): {db_err}")

    return df_books, df_ratings
