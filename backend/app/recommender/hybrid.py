import pandas as pd
from typing import List, Optional

class HybridRecommender:
    def __init__(self, content_engine, collab_engine, popularity_engine):
        self.content_engine = content_engine
        self.collab_engine = collab_engine
        self.popularity_engine = popularity_engine
        self.df_books = None

    def set_books(self, df_books: pd.DataFrame):
        self.df_books = df_books.copy()

    def recommend(
        self,
        seed_book_id: Optional[int] = None,
        preferred_genres: Optional[List[str]] = None,
        min_rating: float = 0.0,
        top_n: int = 8,
        w_content: float = 0.55,
        w_collab: float = 0.30,
        w_pop: float = 0.15
    ):
        """
        Generates hybrid recommendations blending content similarity,
        collaborative interaction patterns, and Bayesian popularity.
        Handles cold-start states seamlessly.
        """
        preferred_genres = preferred_genres or []
        preferred_genres_lower = [g.lower() for g in preferred_genres]

        # Case 1: Cold start — No seed book chosen, but user selected genres or wants top discoveries
        if not seed_book_id:
            return self._cold_start_recommendations(preferred_genres_lower, min_rating, top_n)

        # Retrieve candidates from Content-Based Engine
        content_recs = self.content_engine.get_similar_books(
            seed_book_id,
            top_n=30,
            min_rating=min_rating
        )

        # Retrieve candidates from Collaborative Engine
        collab_recs = self.collab_engine.get_similar_books(
            seed_book_id,
            top_n=30,
            min_rating=min_rating
        )

        # Candidate pool aggregation
        book_scores = {}
        book_metadata = {}
        content_details = {}
        collab_details = {}

        for item in content_recs:
            b_id = item['book']['book_id']
            book_scores[b_id] = {'content': item['similarity_score'], 'collab': 0.0, 'pop': 0.0}
            book_metadata[b_id] = item['book']
            content_details[b_id] = item

        for item in collab_recs:
            b_id = item['book']['book_id']
            if b_id not in book_scores:
                book_scores[b_id] = {'content': 0.0, 'collab': item['similarity_score'], 'pop': 0.0}
                book_metadata[b_id] = item['book']
            else:
                book_scores[b_id]['collab'] = item['similarity_score']
            collab_details[b_id] = item

        # If collaborative data is sparse for this book, adjust weights dynamically
        has_collab = any(s['collab'] > 0 for s in book_scores.values())
        eff_w_content = w_content if has_collab else 0.75
        eff_w_collab = w_collab if has_collab else 0.0
        eff_w_pop = 1.0 - (eff_w_content + eff_w_collab)

        # Max popular score for normalization
        max_wr = self.popularity_engine.df_books['weighted_rating'].max()
        min_wr = self.popularity_engine.df_books['weighted_rating'].min()
        wr_range = (max_wr - min_wr) if (max_wr - min_wr) > 0 else 1.0

        # Calculate combined hybrid score
        hybrid_results = []
        for b_id, scores in book_scores.items():
            book = book_metadata[b_id]

            # Genre filter if specified
            if preferred_genres_lower and book['genre'].lower() not in preferred_genres_lower:
                continue

            # Popularity normalized score [0, 1]
            book_row = self.popularity_engine.df_books[self.popularity_engine.df_books['book_id'] == b_id]
            if not book_row.empty:
                raw_wr = book_row.iloc[0]['weighted_rating']
                norm_pop = (raw_wr - min_wr) / wr_range
            else:
                norm_pop = 0.5

            final_score = (
                eff_w_content * scores['content'] +
                eff_w_collab * scores['collab'] +
                eff_w_pop * norm_pop
            )

            # Build explainable explanation
            explanation_parts = []
            if scores['content'] > 0:
                explanation_parts.append(f"Content Match: {round(scores['content'] * 100)}%")
            if scores['collab'] > 0:
                explanation_parts.append(f"Reader Overlap: {round(scores['collab'] * 100)}%")
            explanation_parts.append(f"Bayesian Rating: {round(norm_pop * 100)}%")

            explanation = (
                f"Generated via Hybrid Model ({', '.join(explanation_parts)}). "
                f"{content_details.get(b_id, {}).get('explanation', '')}"
            )

            hybrid_results.append({
                'book': book,
                'similarity_score': round(float(final_score), 4),
                'score_breakdown': {
                    'content': round(float(scores['content']), 4),
                    'collaborative': round(float(scores['collab']), 4),
                    'popularity': round(float(norm_pop), 4)
                },
                'explanation': explanation,
                'algorithm': 'Hybrid Recommendation Engine (Weighted Linear Combination)'
            })

        # Sort by final score descending
        hybrid_results = sorted(hybrid_results, key=lambda x: x['similarity_score'], reverse=True)
        return hybrid_results[:top_n]

    def _cold_start_recommendations(self, preferred_genres_lower: List[str], min_rating: float, top_n: int):
        """
        Handles new user / cold-start recommendations using genre affinity
        and Bayesian popularity ranking.
        """
        filtered = self.popularity_engine.df_books.copy()
        if preferred_genres_lower:
            filtered = filtered[filtered['genre'].str.lower().isin(preferred_genres_lower)]
        if min_rating > 0.0:
            filtered = filtered[filtered['average_rating'] >= min_rating]

        sorted_books = filtered.sort_values('weighted_rating', ascending=False).head(top_n)

        results = []
        for _, row in sorted_books.iterrows():
            wr = round(float(row['weighted_rating']), 3)
            genres_desc = ", ".join(preferred_genres_lower) if preferred_genres_lower else "curated"
            results.append({
                'book': row.to_dict(),
                'similarity_score': round(wr / 5.0, 4),
                'score_breakdown': {'content': 0.0, 'collaborative': 0.0, 'popularity': round(wr / 5.0, 4)},
                'explanation': f"Cold-Start Recommendation: Ranked among the highest verified titles in your chosen genres ({genres_desc}) with a Bayesian rating of {wr}/5.0.",
                'algorithm': 'Cold-Start Bayesian & Genre Affinity Engine'
            })
        return results
