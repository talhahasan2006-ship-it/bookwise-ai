"""
BookWise AI — Static Data Exporter for GitHub Pages Deployment
Exports datasets/books.csv and dataset statistics to frontend/src/data/
so the application can run 100% autonomously on static hosting (GitHub Pages).
"""
import os
import json
import pandas as pd

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "datasets")
FRONTEND_DATA_DIR = os.path.join(BASE_DIR, "frontend", "src", "data")
os.makedirs(FRONTEND_DATA_DIR, exist_ok=True)

def export_data():
    books_csv = os.path.join(DATA_DIR, "books.csv")
    ratings_csv = os.path.join(DATA_DIR, "ratings.csv")

    df_books = pd.read_csv(books_csv, dtype={'isbn': str})
    df_ratings = pd.read_csv(ratings_csv)

    df_books['isbn'] = df_books['isbn'].astype(str)
    books_list = df_books.to_dict(orient="records")

    # Generate TypeScript file with books data
    books_ts_path = os.path.join(FRONTEND_DATA_DIR, "booksData.ts")
    with open(books_ts_path, "w", encoding="utf-8") as f:
        f.write("// Auto-generated dataset for GitHub Pages static execution\n")
        f.write("import { Book } from '../types';\n\n")
        f.write("export const STATIC_BOOKS: Book[] = ")
        f.write(json.dumps(books_list, indent=2))
        f.write(";\n")
    print(f"Exported {len(books_list)} books to: {books_ts_path}")

    # Generate Stats
    total_books = len(df_books)
    unique_authors = int(df_books['author'].nunique())
    unique_genres = int(df_books['genre'].nunique())
    avg_rating = round(float(df_books['average_rating'].mean()), 2)
    total_ratings_vol = int(df_books['rating_count'].sum())
    total_ratings = len(df_ratings)
    unique_users = int(df_ratings['user_id'].nunique())

    # Genre distribution
    genre_counts = df_books['genre'].value_counts()
    genres_distribution = [{"genre": g, "count": int(c)} for g, c in genre_counts.items()]

    # Ratings distribution
    bins = [
        {"range": "3.0 - 3.5", "count": int(((df_books['average_rating'] >= 3.0) & (df_books['average_rating'] < 3.5)).sum())},
        {"range": "3.5 - 3.9", "count": int(((df_books['average_rating'] >= 3.5) & (df_books['average_rating'] < 4.0)).sum())},
        {"range": "4.0 - 4.2", "count": int(((df_books['average_rating'] >= 4.0) & (df_books['average_rating'] < 4.2)).sum())},
        {"range": "4.2 - 4.5", "count": int(((df_books['average_rating'] >= 4.2) & (df_books['average_rating'] < 4.5)).sum())},
        {"range": "4.5 - 5.0", "count": int((df_books['average_rating'] >= 4.5).sum())},
    ]

    # Eras
    eras = [
        {"era": "Pre-1950 (Classics)", "count": int((df_books['publication_year'] < 1950).sum())},
        {"era": "1950 - 1979 (Golden Age)", "count": int(((df_books['publication_year'] >= 1950) & (df_books['publication_year'] < 1980)).sum())},
        {"era": "1980 - 1999 (Cyberpunk / Modern)", "count": int(((df_books['publication_year'] >= 1980) & (df_books['publication_year'] < 2000)).sum())},
        {"era": "2000 - 2014 (Digital Era)", "count": int(((df_books['publication_year'] >= 2000) & (df_books['publication_year'] < 2015)).sum())},
        {"era": "2015 - Present (AI Revolution)", "count": int((df_books['publication_year'] >= 2015).sum())},
    ]

    top_rated = df_books.sort_values(by=["average_rating", "rating_count"], ascending=[False, False]).head(6).to_dict(orient="records")

    stats_obj = {
        "total_books": total_books,
        "unique_authors": unique_authors,
        "unique_genres": unique_genres,
        "average_rating": avg_rating,
        "total_ratings_volume": total_ratings_vol,
        "collaborative_ratings_count": total_ratings,
        "unique_active_users": unique_users,
        "genres_distribution": genres_distribution,
        "ratings_distribution": bins,
        "publication_era_distribution": eras,
        "top_rated_books": top_rated
    }

    stats_ts_path = os.path.join(FRONTEND_DATA_DIR, "statsData.ts")
    with open(stats_ts_path, "w", encoding="utf-8") as f:
        f.write("// Auto-generated statistics for GitHub Pages static execution\n")
        f.write("import { StatsResponse } from '../types';\n\n")
        f.write("export const STATIC_STATS: StatsResponse = ")
        f.write(json.dumps(stats_obj, indent=2))
        f.write(";\n")
    print(f"Exported statistics to: {stats_ts_path}")

if __name__ == '__main__':
    export_data()
