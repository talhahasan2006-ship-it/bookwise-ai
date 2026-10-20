import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

class CollaborativeRecommender:
    def __init__(self):
        self.df_books = None
        self.df_ratings = None
        self.user_item_matrix = None
        self.item_sim_matrix = None
        self.book_id_to_idx = {}
        self.idx_to_book_id = {}

    def fit(self, df_books: pd.DataFrame, df_ratings: pd.DataFrame):
        """
        Builds the user-item rating matrix and computes item-to-item
        cosine similarity based on normalized user rating patterns.
        """
        self.df_books = df_books.copy().reset_index(drop=True)
        self.df_ratings = df_ratings.copy()

        if self.df_ratings.empty:
            return

        # Create user-item interaction matrix
        # rows: book_id, cols: user_id
        pivot = self.df_ratings.pivot_table(
            index='book_id',
            columns='user_id',
            values='rating'
        )

        # Center ratings by subtracting each user's mean to adjust for optimistic vs harsh raters
        user_means = pivot.mean(axis=0)
        pivot_centered = pivot.sub(user_means, axis=1).fillna(0)

        # Compute cosine similarity between centered item vectors
        sim_centered = cosine_similarity(pivot_centered)

        # Fallback/blend with raw normalized ratings if centered variance is zero
        pivot_raw = pivot.fillna(0)
        sim_raw = cosine_similarity(pivot_raw)

        # If centered similarity is all zeros/nans for an item, use raw cosine similarity
        final_sim = np.where(np.isnan(sim_centered) | (sim_centered == 0), sim_raw, sim_centered)

        self.item_sim_matrix = pd.DataFrame(
            final_sim,
            index=pivot.index,
            columns=pivot.index
        )
        self.user_item_matrix = pivot

    def get_similar_books(self, book_id: int, top_n: int = 6, min_rating: float = 0.0):
        """
        Retrieves books with similar user rating profiles using item-based collaborative filtering.
        """
        if self.item_sim_matrix is None or book_id not in self.item_sim_matrix.index:
            return []

        sim_series = self.item_sim_matrix.loc[book_id].drop(book_id, errors='ignore')
        sim_series = sim_series.sort_values(ascending=False)

        results = []
        for cand_id, score in sim_series.items():
            if score <= 0:
                continue

            book_rows = self.df_books[self.df_books['book_id'] == cand_id]
            if book_rows.empty:
                continue

            cand_book = book_rows.iloc[0]
            if cand_book['average_rating'] < min_rating:
                continue

            results.append({
                'book': cand_book.to_dict(),
                'similarity_score': round(float(score), 4),
                'explanation': f"Readers who rated this book favorably also gave high ratings to '{cand_book['title']}' (Item-based collaborative correlation: {round(score * 100, 1)}%).",
                'algorithm': 'Collaborative Filtering (Item-Item Pearson/Cosine Matrix)'
            })

            if len(results) >= top_n:
                break

        return results
