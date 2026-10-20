# BookWise AI — Dataset Documentation

## 1. Overview
The dataset bundled with **BookWise AI** is curated for academic machine learning research, collaborative filtering evaluation, and content-based recommendation benchmarking. It contains real, authentic books across multiple literary and scientific genres with authentic ISBNs, authors, descriptions, publication metadata, and OpenLibrary cover references, accompanied by a realistic multi-user rating interaction log.

## 2. Dataset Files

### A. `books.csv` (165 Curated Real Books)
Contains detailed book metadata across 8 distinct genres:
- Science Fiction
- Computer Science & AI
- Fantasy
- Dystopian Fiction
- Mystery & Thriller
- Science & Philosophy
- Psychology & Self-Help
- Classic & Historical Fiction

**Schema:**
| Column | Type | Description |
| :--- | :--- | :--- |
| `book_id` | Integer | Unique identifier for the book |
| `title` | String | Full title of the book |
| `author` | String | Author(s) of the book |
| `genre` | String | Primary classification genre |
| `publication_year` | Integer | Original publication year |
| `publisher` | String | Original publisher |
| `isbn` | String | 13-digit ISBN identifier |
| `average_rating` | Float | Historical average reader rating (1.0 to 5.0) |
| `rating_count` | Integer | Historical number of ratings recorded |
| `description` | Text | Full thematic book synopsis used for NLP feature extraction |
| `cover_url` | String | Direct OpenLibrary CDN cover endpoint |

### B. `ratings.csv` (3,868 User-Book Interactions)
Contains user rating records across 150 simulated user taste profiles organized into distinct reader taste clusters (e.g., Tech & AI buffs, Classic literature readers, Sci-Fi enthusiasts, Philosophy scholars).

**Schema:**
| Column | Type | Description |
| :--- | :--- | :--- |
| `user_id` | Integer | User identifier (1 to 150) |
| `book_id` | Integer | Referenced book identifier |
| `rating` | Integer | Explicit rating value from 1 to 5 |
| `timestamp` | Integer | Unix epoch timestamp of interaction |

## 3. Scaling to External Public Datasets
The BookWise AI ingestion engine is schema-agnostic and provides adapter loaders. To scale up to million-row datasets:
- **Book-Crossing Dataset** (`BX-Books.csv`, `BX-Book-Ratings.csv`)
- **Goodreads 10k Dataset** (`books.csv`, `ratings.csv`)

Run `python scripts/download_dataset.py` to fetch additional public corpora.
