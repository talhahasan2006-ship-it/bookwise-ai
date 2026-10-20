import pandas as pd

class PopularityRecommender:
    def __init__(self, m_percentile: float = 0.50):
        self.m_percentile = m_percentile
        self.df_books = None
        self.C = 0.0 # global mean rating
        self.m = 0   # minimum votes required

    def fit(self, df_books: pd.DataFrame):
        self.df_books = df_books.copy()
        self.C = float(self.df_books['average_rating'].mean())
        self.m = float(self.df_books['rating_count'].quantile(self.m_percentile))

        # Calculate Bayesian Weighted Rating
        def weighted_rating(row):
            v = float(row['rating_count'])
            R = float(row['average_rating'])
            return (v / (v + self.m)) * R + (self.m / (v + self.m)) * self.C

        self.df_books['weighted_rating'] = self.df_books.apply(weighted_rating, axis=1)

    def get_top_popular(self, top_n: int = 8, genre: str = None):
        """
        Returns top books ranked by statistically balanced Bayesian Weighted Rating.
        """
        filtered = self.df_books
        if genre and genre.lower() != 'all':
            filtered = filtered[filtered['genre'].str.lower() == genre.lower()]

        sorted_books = filtered.sort_values('weighted_rating', ascending=False).head(top_n)

        results = []
        for _, row in sorted_books.iterrows():
            wr = round(float(row['weighted_rating']), 3)
            results.append({
                'book': row.to_dict(),
                'score': wr,
                'explanation': f"Ranked high based on Bayesian Weighted Score ({wr}/5.0) balancing {row['rating_count']:,} reader reviews with a {row['average_rating']} raw average.",
                'algorithm': 'Bayesian Weighted Popularity Ranking'
            })
        return results
