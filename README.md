# BookWise AI — Intelligent Book Recommendation System Using Machine Learning

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Flask 3.1](https://img.shields.io/badge/Flask-3.1-black.svg)](https://flask.palletsprojects.com/)
[![React 19](https://img.shields.io/badge/React-19.0-61DAFB.svg)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.7-blue.svg)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/TailwindCSS-3.4-38B2AC.svg)](https://tailwindcss.com/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.5%2B-F7931E.svg)](https://scikit-learn.org/)
[![Tests Passed](https://img.shields.io/badge/Pytest-13%20Passed-brightgreen.svg)](https://docs.pytest.org/)

An academic, full-stack, and production-grade AI-based book recommendation system built for a **B.Tech Computer Science and Engineering (Artificial Intelligence and Machine Learning) Non-Teaching Credit Course (NTCC) project**.

BookWise AI combines natural language processing (NLP), collaborative filtering, and statistical Bayesian estimation to recommend personalized books and explain **why** each title was selected.

---

## 🌟 Key Features

1. **Hybrid Ensembling Recommendation Engine:**
   - **Content-Based Filtering:** Sublinear TF-IDF vectorization with (1,2) n-grams and cosine similarity over narrative synopses, genres, and authors.
   - **Item-Based Collaborative Filtering:** User-item interaction vectors adjusted for user rating bias via mean-centering.
   - **Bayesian Weighted Rating:** Eliminates rating outliers using the IMDb/Goodreads formula.
   - **Cold-Start Resolution:** Automatic fallback to Bayesian popularity and genre affinity for new readers and items.

2. **Transparent Explainability:**
   - Every recommendation generates natural language explanation tags and identifies top shared thematic keywords.

3. **Modern Dark Navy UI / UX:**
   - Dark aesthetic (`#0B1020`, `#11182B`, `#171F35`) with purple (`#8B5CF6`) and cyan (`#38BDF8`) accents.
   - Fallback book cover generators ensuring no broken image states.
   - Responsive layout with loading skeletons, filter badges, and smooth transitions.

4. **Multi-View Application:**
   - **Discover (Home):** Hero search with live suggestions dropdown, mood selector, and genre cards.
   - **Book Explorer:** Catalog with multi-attribute filtering (genre, author, min rating) and sorting.
   - **Book Details:** Comprehensive metadata, reading list status toggle, and "Readers Also Explore" section.
   - **AI Recommender Lab:** Interactive control console with algorithm switcher.
   - **My Library:** Persistent SQLite reading list (Want to Read, Currently Reading, Completed, Favorites).
   - **Analytics Dashboard:** Recharts visualizations of real dataset distributions and ML performance metrics.

---

## 📊 Offline Academic Evaluation Results

Evaluated on an 80/20 train/test split of user interaction logs with zero data leakage:

| Evaluation Metric | Measured Score | Academic Interpretation |
| :--- | :--- | :--- |
| **Precision@5** | **0.2000** | 1 in 5 items in top-5 recommendations is an exact held-out test match |
| **Recall@5** | **0.2493** | Recovers ~25% of the user's test favorites within 5 recommendations |
| **NDCG@5** | **0.4068** | High rank quality with relevant items prioritized at earlier positions |
| **Rating Prediction RMSE** | **0.8979** | Root Mean Squared Error under 0.90 on a 1.0–5.0 scale |
| **Genre Coherence@5** | **93.45%** | 93.45% categorical semantic alignment for content matches |
| **Intra-List Diversity@5** | **0.8895** | High serendipity preventing monochromatic recommendations |

---

## 🛠️ Technology Stack

- **Frontend:** React 19, TypeScript, Vite, Tailwind CSS, Lucide React, Recharts.
- **Backend:** Python 3.10+ (tested on Python 3.14 on macOS Apple Silicon), Flask, Flask-CORS, REST API architecture.
- **Machine Learning:** Scikit-learn, NumPy, Pandas, Scipy.
- **Database:** SQLite with SQLAlchemy ORM.
- **Testing:** Pytest 9.x.

---

## 🚀 Setup & Running Instructions (macOS MacBook Air M4 / Linux)

### Option A: One-Click Startup (Recommended)
From the project root:
```bash
chmod +x start.sh
./start.sh
```
This automatically initializes the Python virtual environment, verifies the dataset, installs dependencies, and boots both Flask (port 5000) and Vite (port 5173).

---

### Option B: Step-by-Step Manual Setup

#### 1. Backend Setup
```bash
# 1. Create and activate virtual environment
python3 -m venv backend/venv
source backend/venv/bin/activate

# 2. Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r backend/requirements.txt

# 3. Generate datasets and seed SQLite database
python scripts/seed_dataset.py

# 4. Run Pytest backend test suite
pytest backend/tests -v

# 5. Start Flask backend server
python backend/run.py
```
Backend will be live at: **`http://127.0.0.1:5000`**

#### 2. Frontend Setup (in a separate terminal)
```bash
cd frontend

# 1. Install npm packages
npm install

# 2. Verify TypeScript and production build
npm run build

# 3. Start development server
npm run dev
```
Frontend will be live at: **`http://localhost:5173`**

---

## 🧪 Running Academic Model Evaluation

To reproduce the offline evaluation metrics on the held-out test split:
```bash
source backend/venv/bin/activate
python scripts/evaluate_model.py
```
The results will be printed to terminal and saved in `docs/EVALUATION_RESULTS.json`.

---

## 📂 Project Structure

```
bookwise-ai/
├── backend/
│   ├── app/
│   │   ├── api/                 # Flask REST Blueprints
│   │   ├── models/              # SQLAlchemy Models (Book, LibraryEntry, Rating)
│   │   ├── recommender/         # ML Algorithms (Content, Collab, Popularity, Hybrid)
│   │   ├── data/                # Data loader and DB sync
│   │   ├── config.py            # App configurations
│   │   └── __init__.py          # Flask App Factory
│   ├── tests/                   # 13 Automated Pytest test cases
│   ├── requirements.txt
│   └── run.py
│
├── frontend/
│   ├── src/
│   │   ├── components/          # BookCard, Navbar, Footer, Skeletons, RatingDisplay
│   │   ├── pages/               # Discover, Explorer, BookDetails, Recommendations, Library, Dashboard
│   │   ├── services/            # Typed REST API service client
│   │   ├── types/               # TypeScript interfaces
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.ts
│
├── datasets/
│   ├── books.csv                # 165 Curated authentic books
│   ├── ratings.csv              # 3,868 Multi-user interactions
│   └── README.md
│
├── docs/
│   ├── PROJECT_REPORT.md        # Comprehensive 27-section NTCC B.Tech Report
│   ├── SYSTEM_ARCHITECTURE.md   # Architectural diagrams & module decomposition
│   ├── API_DOCUMENTATION.md     # REST endpoints & schema specifications
│   ├── ALGORITHM_EXPLANATION.md # Mathematical formulations & deep dive
│   ├── TESTING_REPORT.md        # QA test execution & coverage results
│   └── EVALUATION_RESULTS.json  # Raw evaluation metrics output
│
├── scripts/
│   ├── seed_dataset.py          # Dataset synthesizer & seeder
│   ├── evaluate_model.py        # Model evaluation pipeline (Precision/Recall/NDCG)
│   └── download_dataset.py      # Optional external scaling helper
│
├── start.sh                     # One-click launch script
├── .env.example
├── .gitignore
├── pytest.ini
└── README.md
```

---

## 📚 Academic Documentation
Full documentation ready for formatting into your university's prescribed NTCC project template is available in the [`docs/`](file:///Users/hsan2010/NTCC%20project%201/docs/) directory:
- [PROJECT_REPORT.md](file:///Users/hsan2010/NTCC%20project%201/docs/PROJECT_REPORT.md)
- [SYSTEM_ARCHITECTURE.md](file:///Users/hsan2010/NTCC%20project%201/docs/SYSTEM_ARCHITECTURE.md)
- [API_DOCUMENTATION.md](file:///Users/hsan2010/NTCC%20project%201/docs/API_DOCUMENTATION.md)
- [ALGORITHM_EXPLANATION.md](file:///Users/hsan2010/NTCC%20project%201/docs/ALGORITHM_EXPLANATION.md)
- [TESTING_REPORT.md](file:///Users/hsan2010/NTCC%20project%201/docs/TESTING_REPORT.md)
