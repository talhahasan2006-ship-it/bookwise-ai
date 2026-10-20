# BookWise AI — System Architecture

## 1. High-Level Architecture Overview
BookWise AI is structured as a decoupled client-server architecture consisting of a **React 19 TypeScript Single Page Application (SPA)** and a **Python Flask RESTful Microservice API** backed by a **SQLite / SQLAlchemy database** and a **Scikit-learn Recommendation Engine**.

```
+-------------------------------------------------------------+
|                      PRESENTATION TIER                      |
|  React 19 + TypeScript + Vite + Tailwind CSS + Recharts     |
+-------------------------------------------------------------+
                              |
                     HTTPS / JSON REST
                              |
+-------------------------------------------------------------+
|                     APPLICATION TIER                        |
|  Flask Application Factory + Blueprint Routers             |
|  - /api/books          - /api/recommendations               |
|  - /api/genres         - /api/stats                         |
|  - /api/library        - /api/health                        |
+-------------------------------------------------------------+
                              |
         +--------------------+--------------------+
         |                                         |
+------------------------+             +----------------------+
|    INTELLIGENCE TIER   |             |   PERSISTENCE TIER   |
| Scikit-learn + NumPy   |             | SQLite + SQLAlchemy  |
| - TF-IDF Vectorizer    |             | - books table        |
| - Cosine Similarity    |             | - library_entries    |
| - Collaborative Matrix |             | - ratings table      |
| - Bayesian Re-ranker   |             +----------------------+
+------------------------+
```

## 2. Directory Modular Decomposition
```
bookwise-ai/
├── backend/
│   ├── app/
│   │   ├── __init__.py          # Flask App Factory & Blueprint registration
│   │   ├── config.py            # Environment & database configs
│   │   ├── api/                 # REST Route Blueprints
│   │   │   ├── books.py         # Catalog search, filter, details
│   │   │   ├── recommendations.py# Content, collaborative, hybrid recs
│   │   │   ├── genres.py        # Dataset taxonomy
│   │   │   ├── stats.py         # Real dataset metrics for dashboard
│   │   │   ├── library.py       # Reading lists and favorites persistence
│   │   │   └── health.py        # System health & engine state
│   │   ├── models/              # SQLAlchemy ORM definitions
│   │   │   ├── database.py      # SQLAlchemy db instance
│   │   │   ├── book.py          # Book model
│   │   │   ├── library.py       # Reading list & favorite model
│   │   │   └── rating.py        # User-item rating model
│   │   ├── recommender/         # Core Machine Learning Engine
│   │   │   ├── engine.py        # Engine Singleton Orchestrator
│   │   │   ├── content_based.py # TF-IDF & Cosine Similarity
│   │   │   ├── collaborative.py # Item-Item interaction matrix
│   │   │   ├── popularity.py    # Bayesian Weighted Rating
│   │   │   └── hybrid.py        # Linear ensembling & cold-start handler
│   │   └── data/
│   │       └── loader.py        # Data loading and SQLite synchronization
│   ├── tests/                   # Pytest automated test suites
│   ├── requirements.txt         # Python dependencies
│   └── run.py                   # Local development server runner
│
├── frontend/
│   ├── src/
│   │   ├── components/          # Reusable UI widgets
│   │   ├── pages/               # Application view screens
│   │   ├── services/            # Typed API client
│   │   ├── types/               # TypeScript interfaces
│   │   ├── App.tsx              # Root router & navigation manager
│   │   └── main.tsx             # DOM mount entrypoint
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.ts
│
├── datasets/
│   ├── books.csv                # Curated catalog (165 titles)
│   ├── ratings.csv              # Multi-user interaction logs (3,868 rows)
│   └── README.md
│
├── docs/                        # Complete academic project reports
├── scripts/                     # Seeding & evaluation scripts
├── start.sh                     # One-click startup script for macOS
└── README.md
```

## 3. Data Flow Diagram (DFD)
1. **User Discovery:** User accesses frontend -> Vite proxy routes request to Flask `/api/books` or `/api/recommendations/popular`.
2. **Personalized Recommendation:**
   - User inputs Seed Book and/or Preferred Genres.
   - Frontend calls `POST /api/recommendations/personalized`.
   - Engine extracts TF-IDF vector, calculates cosine similarities, inspects collaborative interaction overlap, applies Bayesian dampening, normalizes scores, and returns ranked list with explanation tags.
3. **Library Management:** User marks book as favorite -> `POST /api/library` saves entry to SQLite.
