# BookWise AI — Testing & Quality Assurance Report

## 1. Test Suite Execution Summary
- **Testing Framework:** Pytest 9.1.1
- **Python Environment:** Python 3.14.7 (Apple Silicon ARM64, macOS)
- **Total Tests Executed:** 13
- **Passed:** 13
- **Failed:** 0
- **Execution Duration:** 0.95 seconds

## 2. Test Cases Breakdown

### A. Backend API Integration Tests (`backend/tests/test_api.py`)
1. `test_health_endpoint`: Verifies `/api/health` returns status `200`, engine initialized `true`, and non-zero books in SQLite.
2. `test_books_pagination_and_search`: Validates query searching, genre filtering, and page size constraints.
3. `test_book_details`: Verifies single item retrieval and strict `404 Not Found` response for non-existent IDs.
4. `test_similar_books`: Verifies `/api/books/<id>/similar` returns recommendations excluding the source book itself.
5. `test_recommendations_content`: Validates content-based route returning similarity scores and explanation strings.
6. `test_recommendations_popular`: Verifies Bayesian weighted popularity rankings.
7. `test_personalized_recommendations`: Tests interactive hybrid recommendation ensembling and cold-start requests.
8. `test_stats_endpoint`: Validates real dataset statistics, genre counts, and rating distributions.
9. `test_library_crud_endpoints`: Verifies SQLite creation, retrieval, updates, and deletion for local demo reading lists.

### B. Machine Learning Algorithmic Tests (`backend/tests/test_recommender.py`)
10. `test_content_based_engine`: Asserts that semantically related technical books (e.g. Machine Learning & Deep Learning) receive higher similarity than disparate genres (Romance), and verifies keyword extraction.
11. `test_collaborative_filtering`: Tests item-to-item rating vector similarity on synthetic user interaction profiles.
12. `test_popularity_bayesian_ranking`: Validates that Bayesian scores stay bounded within $[1.0, 5.0]$ and penalize low-count books.
13. `test_hybrid_recommender`: Asserts that hybrid ensembling balances multiple score components with explainable breakdowns.

## 3. Frontend Static Analysis & Bundle Verification
- **TypeScript Typecheck:** `tsc -b` -> Passed (0 errors).
- **Vite Production Build:** `npm run build` -> Passed (Bundle generated in 1.48s).
