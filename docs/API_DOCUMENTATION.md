# BookWise AI — REST API Documentation

Base URL: `http://127.0.0.1:5000/api`

---

### 1. Health Status
- **Endpoint:** `GET /health`
- **Description:** Verifies service health, database connection, and recommender engine state.
- **Response `200 OK`:**
```json
{
  "status": "healthy",
  "application": "BookWise AI Backend",
  "database_connected": true,
  "total_books_in_db": 165,
  "recommender_engine_initialized": true,
  "algorithms_available": [
    "Content-Based Filtering (TF-IDF + Cosine Similarity)",
    "Collaborative Filtering (Item-Based Interaction Vectors)",
    "Bayesian Weighted Popularity Ranking",
    "Hybrid Linear Combination Recommender"
  ]
}
```

---

### 2. Book Catalogue
- **Endpoint:** `GET /books`
- **Query Parameters:**
  - `page` (int, default: 1)
  - `per_page` (int, default: 12)
  - `q` (string, optional: search query)
  - `genre` (string, optional: genre filter)
  - `min_rating` (float, optional: minimum rating threshold)
  - `sort_by` (string, optional: 'popular' | 'highest_rated' | 'title_asc' | 'year_desc' | 'year_asc')
- **Response `200 OK`:**
```json
{
  "books": [
    {
      "id": 1,
      "book_id": 1,
      "title": "Dune",
      "author": "Frank Herbert",
      "genre": "Science Fiction",
      "publication_year": 1965,
      "publisher": "Chilton Books",
      "isbn": "9780441172719",
      "average_rating": 4.26,
      "rating_count": 1245000,
      "description": "Set on the desert planet Arrakis...",
      "cover_url": "https://covers.openlibrary.org/b/isbn/9780441172719-L.jpg"
    }
  ],
  "total": 165,
  "page": 1,
  "per_page": 12,
  "total_pages": 14,
  "has_prev": false,
  "has_next": true
}
```

---

### 3. Book Details
- **Endpoint:** `GET /books/<book_id>`
- **Response `200 OK`:**
```json
{
  "book": {
    "id": 1,
    "title": "Dune",
    "author": "Frank Herbert",
    "genre": "Science Fiction",
    "publication_year": 1965,
    "average_rating": 4.26,
    "rating_count": 1245000,
    "description": "...",
    "cover_url": "..."
  }
}
```

---

### 4. Similar Books
- **Endpoint:** `GET /books/<book_id>/similar?limit=6`
- **Response `200 OK`:**
```json
{
  "source_book": { "id": 1, "title": "Dune" },
  "recommendations": [
    {
      "book": { "id": 7, "title": "Foundation", "author": "Isaac Asimov" },
      "similarity_score": 0.4851,
      "shared_keywords": ["empire", "galactic", "science", "future"],
      "explanation": "Recommended with 48.5% affinity because it shares the 'Science Fiction' genre and matches prominent themes ('empire', 'galactic').",
      "algorithm": "Hybrid Recommendation Engine"
    }
  ]
}
```

---

### 5. Personalized Recommendations Laboratory
- **Endpoint:** `POST /recommendations/personalized`
- **Request Body:**
```json
{
  "seed_book_id": 1,
  "preferred_genres": ["Science Fiction", "Computer Science & AI"],
  "min_rating": 4.0,
  "limit": 6,
  "algorithm": "hybrid"
}
```
- **Response `200 OK`:**
```json
{
  "algorithm": "hybrid",
  "seed_book": { "id": 1, "title": "Dune" },
  "count": 6,
  "recommendations": [
    {
      "book": { "id": 4, "title": "Neuromancer" },
      "similarity_score": 0.5218,
      "score_breakdown": {
        "content": 0.4812,
        "collaborative": 0.6120,
        "popularity": 0.4430
      },
      "explanation": "Generated via Hybrid Model (Content Match: 48%, Reader Overlap: 61%, Bayesian Rating: 44%)."
    }
  ]
}
```

---

### 6. User Library Management
- **Endpoint:** `GET /library?status=want_to_read&favorites=true`
- **Endpoint:** `POST /library`
```json
{
  "book_id": 1,
  "status": "want_to_read",
  "is_favorite": true,
  "notes": "Must read before seeing the movie."
}
```
- **Endpoint:** `DELETE /library/<book_id>`
