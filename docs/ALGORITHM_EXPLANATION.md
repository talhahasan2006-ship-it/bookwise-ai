# BookWise AI — Machine Learning Algorithm Deep-Dive

## 1. Content-Based Filtering (NLP)

### The Semantic Soup
To build an information-dense representation of each book, multiple textual features are concatenated with specific weights:
```python
soup = f"{title} {author} {author} {genre} {genre} {genre} {description}"
```
- **Author duplication (2x):** Ensures books by the same author gain significant relevance boost without overwhelming description keywords.
- **Genre duplication (3x):** Guarantees high categorical affinity.

### Vectorization
Using Scikit-learn's `TfidfVectorizer`:
- `ngram_range=(1, 2)`: Captures single keywords and bigrams (e.g., "artificial intelligence", "deep learning", "space opera").
- `sublinear_tf=True`: Employs log-frequency scaling $1 + \ln(TF)$ to dampen the distortive effect of long descriptions.
- `stop_words='english'`: Eliminates non-discriminatory function words.

### Explainability Extraction
To explain *why* Book B was recommended for Book A:
$$\mathbf{W}_{shared} = \mathbf{V}_A \odot \mathbf{V}_B$$
The element-wise Hadamard product identifies top vocabulary indices with the highest mutual TF-IDF weights, converting math into human-understandable explanation tags (e.g., "shares themes: 'cyberpunk', 'neural', 'matrix'").

---

## 2. Item-Based Collaborative Filtering

### User-Item Pivot Matrix
Given user interactions across 150 simulated user taste profiles:
$$R \in \mathbb{R}^{B \times U}$$
where $B = 165$ books and $U = 150$ users.

### Mean-Centering & Zero-Norm Fallback
Different readers possess distinct rating thresholds: some give 5 stars generously, while others rarely give above 3. User mean-centering neutralizes this subjectivity:
$$s_{u, i} = r_{u, i} - \bar{r}_u$$
If an item vector has zero variance under mean-centering, the model smoothly falls back to raw interaction cosine similarity to preserve item continuity.

---

## 3. Bayesian Weighted Rating (Popularity)
The IMDb / Goodreads formulation prevents outlier distortion:
$$WR = \left(\frac{v}{v + m}\right) R + \left(\frac{m}{v + m}\right) C$$
Where:
- $v$ = count of votes for this book
- $m$ = 50th percentile threshold across the catalog
- $R$ = average rating of this book
- $C$ = global catalog mean rating (~4.22)

---

## 4. Cold-Start Handling Strategy
| Scenario | Algorithm Triggered | Fallback Behavior |
| :--- | :--- | :--- |
| **New User, No Seed Book** | Bayesian Genre Affinity | Recommends top Bayesian-rated books filtered by selected genres |
| **New Book, Zero User Ratings** | Content-Based Model | Computes TF-IDF similarity purely from synopsis, author, and genre |
| **Sparse Interaction Book** | Dynamic Weight Re-balancing | Shifts weights from collaborative ($0\%$) to content ($75\%$) + popularity ($25\%$) |
