import pytest
import pandas as pd
from backend.app.recommender.content_based import ContentBasedRecommender
from backend.app.recommender.collaborative import CollaborativeRecommender
from backend.app.recommender.popularity import PopularityRecommender
from backend.app.recommender.hybrid import HybridRecommender

@pytest.fixture
def sample_data():
    df_books = pd.DataFrame([
        {
            "book_id": 1,
            "title": "Machine Learning Fundamentals",
            "author": "Alan Turing",
            "genre": "Computer Science",
            "publication_year": 2020,
            "publisher": "Tech Press",
            "isbn": "1111111111",
            "average_rating": 4.5,
            "rating_count": 1000,
            "description": "Comprehensive guide to neural networks, machine learning algorithms, and artificial intelligence.",
            "cover_url": ""
        },
        {
            "book_id": 2,
            "title": "Deep Learning Architectures",
            "author": "Alan Turing",
            "genre": "Computer Science",
            "publication_year": 2021,
            "publisher": "Tech Press",
            "isbn": "2222222222",
            "average_rating": 4.7,
            "rating_count": 800,
            "description": "Advanced neural networks, deep learning models, backpropagation, and artificial intelligence systems.",
            "cover_url": ""
        },
        {
            "book_id": 3,
            "title": "Pride and Romance",
            "author": "Jane Austen",
            "genre": "Romance",
            "publication_year": 1813,
            "publisher": "Classic Press",
            "isbn": "3333333333",
            "average_rating": 4.2,
            "rating_count": 5000,
            "description": "A classic romance novel depicting 19th-century social customs, love, and marriage in England.",
            "cover_url": ""
        }
    ])

    df_ratings = pd.DataFrame([
        {"user_id": 1, "book_id": 1, "rating": 5.0, "timestamp": 1000},
        {"user_id": 1, "book_id": 2, "rating": 5.0, "timestamp": 1001},
        {"user_id": 2, "book_id": 1, "rating": 4.0, "timestamp": 1002},
        {"user_id": 2, "book_id": 2, "rating": 4.0, "timestamp": 1003},
        {"user_id": 3, "book_id": 3, "rating": 5.0, "timestamp": 1004},
    ])

    return df_books, df_ratings

def test_content_based_engine(sample_data):
    df_books, _ = sample_data
    engine = ContentBasedRecommender()
    engine.fit(df_books)

    # Book 1 should recommend Book 2 higher than Book 3
    recs = engine.get_similar_books(book_id=1, top_n=2)
    assert len(recs) == 2
    assert recs[0]['book']['book_id'] == 2 # Deep learning is closer to ML than Romance
    assert recs[0]['similarity_score'] > recs[1]['similarity_score']
    assert any(k in str(recs[0]['shared_keywords']) for k in ['science', 'computer', 'turing', 'learning', 'artificial'])

def test_collaborative_filtering(sample_data):
    df_books, df_ratings = sample_data
    engine = CollaborativeRecommender()
    engine.fit(df_books, df_ratings)

    # Book 1 and Book 2 have identical user rating patterns
    recs = engine.get_similar_books(book_id=1, top_n=2)
    assert len(recs) >= 1
    assert recs[0]['book']['book_id'] == 2

def test_popularity_bayesian_ranking(sample_data):
    df_books, _ = sample_data
    engine = PopularityRecommender(m_percentile=0.50)
    engine.fit(df_books)

    top_pop = engine.get_top_popular(top_n=3)
    assert len(top_pop) == 3
    # Scores must be within 1.0 - 5.0
    for item in top_pop:
        assert 1.0 <= item['score'] <= 5.0

def test_hybrid_recommender(sample_data):
    df_books, df_ratings = sample_data
    c_eng = ContentBasedRecommender()
    c_eng.fit(df_books)

    collab_eng = CollaborativeRecommender()
    collab_eng.fit(df_books, df_ratings)

    pop_eng = PopularityRecommender()
    pop_eng.fit(df_books)

    hybrid = HybridRecommender(c_eng, collab_eng, pop_eng)
    hybrid.set_books(df_books)

    recs = hybrid.recommend(seed_book_id=1, top_n=2)
    assert len(recs) > 0
    assert 'score_breakdown' in recs[0]
    assert recs[0]['similarity_score'] > 0
