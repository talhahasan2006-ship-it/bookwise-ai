import pytest
from backend.app import create_app
from backend.app.models import db, Book, LibraryEntry

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_health_endpoint(client):
    res = client.get('/api/health')
    assert res.status_code == 200
    data = res.json
    assert data['status'] == 'healthy'
    assert data['recommender_engine_initialized'] is True
    assert data['total_books_in_db'] > 0

def test_books_pagination_and_search(client):
    # Test catalog pagination
    res = client.get('/api/books?page=1&per_page=6')
    assert res.status_code == 200
    data = res.json
    assert len(data['books']) == 6
    assert data['total'] >= 100

    # Test title search
    res_search = client.get('/api/books?q=Dune')
    assert res_search.status_code == 200
    assert any('Dune' in b['title'] for b in res_search.json['books'])

    # Test genre filter
    res_genre = client.get('/api/books?genre=Science Fiction')
    assert res_genre.status_code == 200
    assert all('Science Fiction' in b['genre'] for b in res_genre.json['books'])

def test_book_details(client):
    res = client.get('/api/books/1')
    assert res.status_code == 200
    assert res.json['book']['id'] == 1

    # 404 on nonexistent
    res_404 = client.get('/api/books/999999')
    assert res_404.status_code == 404

def test_similar_books(client):
    res = client.get('/api/books/1/similar?limit=4')
    assert res.status_code == 200
    assert 'recommendations' in res.json
    assert len(res.json['recommendations']) <= 4
    # Ensure source book is not in the recommendations
    rec_ids = [r['book']['book_id'] for r in res.json['recommendations']]
    assert 1 not in rec_ids

def test_recommendations_content(client):
    res = client.get('/api/recommendations/content/1?limit=5')
    assert res.status_code == 200
    assert len(res.json['recommendations']) <= 5
    for item in res.json['recommendations']:
        assert 'similarity_score' in item
        assert 'explanation' in item

def test_recommendations_popular(client):
    res = client.get('/api/recommendations/popular?limit=5')
    assert res.status_code == 200
    assert len(res.json['recommendations']) <= 5
    assert res.json['algorithm'] == 'Bayesian Weighted Popularity Ranking'

def test_personalized_recommendations(client):
    # Hybrid request
    payload = {
        'seed_book_id': 1,
        'algorithm': 'hybrid',
        'limit': 5
    }
    res = client.post('/api/recommendations/personalized', json=payload)
    assert res.status_code == 200
    assert len(res.json['recommendations']) <= 5

    # Cold start request (no seed book, just genres)
    cold_payload = {
        'preferred_genres': ['Science Fiction', 'Computer Science & AI'],
        'algorithm': 'hybrid',
        'limit': 4
    }
    cold_res = client.post('/api/recommendations/personalized', json=cold_payload)
    assert cold_res.status_code == 200
    assert len(cold_res.json['recommendations']) <= 4

def test_stats_endpoint(client):
    res = client.get('/api/stats')
    assert res.status_code == 200
    data = res.json
    assert data['total_books'] >= 100
    assert data['unique_authors'] > 20
    assert data['unique_genres'] > 3
    assert len(data['genres_distribution']) > 0
    assert len(data['ratings_distribution']) > 0

def test_library_crud_endpoints(client):
    # 1. Add / Update book in library
    add_payload = {
        'book_id': 2,
        'status': 'currently_reading',
        'is_favorite': True,
        'notes': 'Remarkable classic.'
    }
    post_res = client.post('/api/library', json=add_payload)
    assert post_res.status_code == 200
    assert post_res.json['entry']['book_id'] == 2
    assert post_res.json['entry']['is_favorite'] is True

    # 2. Get library
    get_res = client.get('/api/library')
    assert get_res.status_code == 200
    book_ids = [e['book_id'] for e in get_res.json['entries']]
    assert 2 in book_ids

    # 3. Delete from library
    del_res = client.delete('/api/library/2')
    assert del_res.status_code == 200

    # Verify deletion
    verify_res = client.get('/api/library')
    assert 2 not in [e['book_id'] for e in verify_res.json['entries']]
