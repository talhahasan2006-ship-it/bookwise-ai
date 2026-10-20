import re
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ContentBasedRecommender:
    def __init__(self):
        self.df_books = None
        self.vectorizer = None
        self.tfidf_matrix = None
        self.cosine_sim = None
        self.book_id_to_idx = {}
        self.idx_to_book_id = {}

    def fit(self, df_books: pd.DataFrame):
        """
        Fits TF-IDF on the combined book representation and precomputes
        cosine similarity matrix with memory-efficient structures.
        """
        self.df_books = df_books.copy().reset_index(drop=True)
        self.book_id_to_idx = {int(row['book_id']): idx for idx, row in self.df_books.iterrows()}
        self.idx_to_book_id = {idx: int(row['book_id']) for idx, row in self.df_books.iterrows()}

        # Build combined content feature text representation
        def build_soup(row):
            title = re.sub(r'[^\w\s]', ' ', str(row['title']).lower())
            author = re.sub(r'[^\w\s]', ' ', str(row['author']).lower())
            genre = re.sub(r'[^\w\s]', ' ', str(row['genre']).lower())
            desc = re.sub(r'[^\w\s]', ' ', str(row['description']).lower())
            # Weighted repeats to emphasize author and genre signals
            return f"{title} {author} {author} {genre} {genre} {genre} {desc}"

        soup_series = self.df_books.apply(build_soup, axis=1)

        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),
            max_features=5000,
            sublinear_tf=True
        )
        self.tfidf_matrix = self.vectorizer.fit_transform(soup_series)
        self.cosine_sim = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)

    def get_similar_books(self, book_id: int, top_n: int = 6, min_rating: float = 0.0, genre: str = None):
        """
        Retrieves top similar books based on cosine similarity with explainability.
        """
        if book_id not in self.book_id_to_idx:
            return []

        idx = self.book_id_to_idx[book_id]
        target_book = self.df_books.iloc[idx]
        sim_scores = list(enumerate(self.cosine_sim[idx]))

        # Sort descending by similarity score, excluding target book itself
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = [item for item in sim_scores if item[0] != idx]

        results = []
        feature_names = np.array(self.vectorizer.get_feature_names_out())
        target_vec = self.tfidf_matrix[idx].toarray().flatten()

        for candidate_idx, score in sim_scores:
            candidate_book = self.df_books.iloc[candidate_idx]

            # Filter conditions
            if candidate_book['average_rating'] < min_rating:
                continue
            if genre and genre.lower() != 'all' and candidate_book['genre'].lower() != genre.lower():
                continue

            # Compute shared top TF-IDF keywords for explainability
            cand_vec = self.tfidf_matrix[candidate_idx].toarray().flatten()
            shared_weights = target_vec * cand_vec
            top_shared_indices = shared_weights.argsort()[::-1][:4]
            top_terms = [feature_names[i] for i in top_shared_indices if shared_weights[i] > 0]

            explanation = self._build_explanation(target_book, candidate_book, top_terms, score)

            results.append({
                'book': candidate_book.to_dict(),
                'similarity_score': round(float(score), 4),
                'shared_keywords': top_terms,
                'explanation': explanation,
                'algorithm': 'Content-Based Filtering (TF-IDF & Cosine Similarity)'
            })

            if len(results) >= top_n:
                break

        return results

    def _build_explanation(self, source, target, top_terms, score):
        reasons = []
        if source['author'] == target['author']:
            reasons.append(f"written by the same author ({source['author']})")
        if source['genre'] == target['genre']:
            reasons.append(f"shares the '{source['genre']}' genre")
        if top_terms:
            terms_str = ", ".join([f"'{t}'" for t in top_terms[:3]])
            reasons.append(f"matches prominent themes ({terms_str})")

        if not reasons:
            return f"Calculated a {round(score * 100, 1)}% contextual narrative similarity based on TF-IDF word embeddings."

        return f"Recommended with {round(score * 100, 1)}% affinity because it " + " and ".join(reasons) + "."
