import time
import pandas as pd
from .content_based import ContentBasedRecommender
from .collaborative import CollaborativeRecommender
from .popularity import PopularityRecommender
from .hybrid import HybridRecommender

class RecommenderEngine:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(RecommenderEngine, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def initialize(self, df_books: pd.DataFrame, df_ratings: pd.DataFrame):
        """
        Initializes and pre-computes TF-IDF matrices, cosine similarities,
        and collaborative matrices.
        """
        start_time = time.time()
        print("Initializing BookWise AI Recommendation Engine...")

        self.df_books = df_books
        self.df_ratings = df_ratings

        # 1. Content-Based Recommender
        self.content_engine = ContentBasedRecommender()
        self.content_engine.fit(df_books)

        # 2. Collaborative Recommender
        self.collab_engine = CollaborativeRecommender()
        self.collab_engine.fit(df_books, df_ratings)

        # 3. Popularity Recommender
        self.popularity_engine = PopularityRecommender()
        self.popularity_engine.fit(df_books)

        # 4. Hybrid Recommender
        self.hybrid_engine = HybridRecommender(
            self.content_engine,
            self.collab_engine,
            self.popularity_engine
        )
        self.hybrid_engine.set_books(df_books)

        self.initialized = True
        elapsed = time.time() - start_time
        print(f"Recommendation Engine initialized successfully in {elapsed:.2f} seconds!")

    def recommend(
        self,
        algorithm: str = "hybrid",
        seed_book_id: int = None,
        preferred_genres: list = None,
        min_rating: float = 0.0,
        top_n: int = 8
    ):
        if not self.initialized:
            raise RuntimeError("Recommendation engine is not initialized yet.")

        algo = (algorithm or "hybrid").lower()

        if algo == "content" and seed_book_id:
            genre_filter = preferred_genres[0] if (preferred_genres and len(preferred_genres) == 1) else None
            return self.content_engine.get_similar_books(
                book_id=seed_book_id,
                top_n=top_n,
                min_rating=min_rating,
                genre=genre_filter
            )

        elif algo == "collaborative" and seed_book_id:
            results = self.collab_engine.get_similar_books(
                book_id=seed_book_id,
                top_n=top_n,
                min_rating=min_rating
            )
            # Fallback to content-based if collaborative data is sparse
            if not results:
                print(f"Collaborative data sparse for book_id {seed_book_id}; falling back to content-based.")
                return self.content_engine.get_similar_books(
                    book_id=seed_book_id,
                    top_n=top_n,
                    min_rating=min_rating
                )
            return results

        elif algo == "popular":
            genre_filter = preferred_genres[0] if (preferred_genres and len(preferred_genres) == 1) else None
            return self.popularity_engine.get_top_popular(top_n=top_n, genre=genre_filter)

        else: # Default: Hybrid
            return self.hybrid_engine.recommend(
                seed_book_id=seed_book_id,
                preferred_genres=preferred_genres,
                min_rating=min_rating,
                top_n=top_n
            )

engine = RecommenderEngine()
