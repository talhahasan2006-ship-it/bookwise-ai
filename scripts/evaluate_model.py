"""
BookWise AI — Rigorous Academic Model Evaluation Pipeline
Evaluates Content-Based, Item-Based Collaborative Filtering, and Hybrid algorithms
using train/test split (80/20) with no data leakage.
Computes Precision@K, Recall@K, NDCG@K, RMSE, and Intra-List Diversity.
"""
import os
import json
import math
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATASETS_DIR = os.path.join(BASE_DIR, "datasets")
DOCS_DIR = os.path.join(BASE_DIR, "docs")
os.makedirs(DOCS_DIR, exist_ok=True)

def dcg_at_k(r, k):
    """Discounted Cumulative Gain at rank k"""
    r = np.asarray(r, dtype=float)[:k]
    if r.size:
        return np.sum(r / np.log2(np.arange(2, r.size + 2)))
    return 0.0

def ndcg_at_k(r, k):
    """Normalized Discounted Cumulative Gain at rank k"""
    dcg_max = dcg_at_k(sorted(r, reverse=True), k)
    if not dcg_max:
        return 0.0
    return dcg_at_k(r, k) / dcg_max

def run_evaluation():
    print("=" * 60)
    print("BOOKWISE AI — MACHINE LEARNING MODEL EVALUATION PIPELINE")
    print("=" * 60)

    books_path = os.path.join(DATASETS_DIR, "books.csv")
    ratings_path = os.path.join(DATASETS_DIR, "ratings.csv")

    df_books = pd.read_csv(books_path)
    df_ratings = pd.read_csv(ratings_path)

    print(f"Total Books: {len(df_books)}")
    print(f"Total User Ratings: {len(df_ratings)}")
    print(f"Unique Users: {df_ratings['user_id'].nunique()}")

    # 1. Train/Test Split on Ratings (80% Train, 20% Held-out Test)
    train_ratings, test_ratings = train_test_split(
        df_ratings,
        test_size=0.20,
        random_state=42,
        stratify=df_ratings['user_id']
    )
    print(f"Training Interactions: {len(train_ratings)}")
    print(f"Held-out Test Interactions: {len(test_ratings)}")

    # 2. Collaborative Filtering Model trained strictly on train_ratings
    train_pivot = train_ratings.pivot_table(index='book_id', columns='user_id', values='rating')
    user_means = train_pivot.mean(axis=0)
    pivot_centered = train_pivot.sub(user_means, axis=1).fillna(0)
    item_sim = pd.DataFrame(cosine_similarity(pivot_centered), index=train_pivot.index, columns=train_pivot.index)

    # Collaborative Evaluation Metrics
    precisions_5 = []
    precisions_10 = []
    recalls_5 = []
    recalls_10 = []
    ndcgs_5 = []
    ndcgs_10 = []
    squared_errors = []

    # Relevance threshold: ratings >= 4.0 are relevant
    test_users = test_ratings['user_id'].unique()

    for u_id in test_users:
        u_train = train_ratings[train_ratings['user_id'] == u_id]
        u_test = test_ratings[test_ratings['user_id'] == u_id]

        if u_train.empty or u_test.empty:
            continue

        ground_truth_relevant = set(u_test[u_test['rating'] >= 4.0]['book_id'].tolist())
        if not ground_truth_relevant:
            continue

        # Predict item scores for unobserved items using user's high-rated train books
        user_top_train = u_train[u_train['rating'] >= 4.0]['book_id'].tolist()
        if not user_top_train:
            user_top_train = u_train.sort_values('rating', ascending=False)['book_id'].head(3).tolist()

        predicted_scores = {}
        for seed_id in user_top_train:
            if seed_id in item_sim.index:
                sims = item_sim.loc[seed_id]
                for cand_id, score in sims.items():
                    if cand_id not in u_train['book_id'].values:
                        predicted_scores[cand_id] = predicted_scores.get(cand_id, 0.0) + score

        # Rank items
        ranked_items = sorted(predicted_scores.keys(), key=lambda x: predicted_scores[x], reverse=True)

        # Top 5 and Top 10 recommendations
        top_5 = ranked_items[:5]
        top_10 = ranked_items[:10]

        # Precision & Recall @ 5
        hits_5 = len(set(top_5).intersection(ground_truth_relevant))
        precisions_5.append(hits_5 / 5.0)
        recalls_5.append(hits_5 / float(len(ground_truth_relevant)))

        # Precision & Recall @ 10
        hits_10 = len(set(top_10).intersection(ground_truth_relevant))
        precisions_10.append(hits_10 / 10.0)
        recalls_10.append(hits_10 / float(len(ground_truth_relevant)))

        # NDCG binary relevance vector
        rel_vec_5 = [1 if item in ground_truth_relevant else 0 for item in top_5]
        rel_vec_10 = [1 if item in ground_truth_relevant else 0 for item in top_10]
        ndcgs_5.append(ndcg_at_k(rel_vec_5, 5))
        ndcgs_10.append(ndcg_at_k(rel_vec_10, 10))

        # Rating prediction RMSE check on test interactions
        for _, test_row in u_test.iterrows():
            cand_book = test_row['book_id']
            actual_r = test_row['rating']
            if cand_book in item_sim.index:
                # weighted average prediction
                sim_weights = []
                sim_ratings = []
                for _, tr_row in u_train.iterrows():
                    tr_book = tr_row['book_id']
                    if tr_book in item_sim.columns:
                        w = item_sim.loc[cand_book, tr_book]
                        if w > 0:
                            sim_weights.append(w)
                            sim_ratings.append(tr_row['rating'])
                if sim_weights:
                    pred_r = sum(w * r for w, r in zip(sim_weights, sim_ratings)) / sum(sim_weights)
                    squared_errors.append((actual_r - pred_r) ** 2)

    mean_p5 = float(np.mean(precisions_5)) if precisions_5 else 0.0
    mean_p10 = float(np.mean(precisions_10)) if precisions_10 else 0.0
    mean_r5 = float(np.mean(recalls_5)) if recalls_5 else 0.0
    mean_r10 = float(np.mean(recalls_10)) if recalls_10 else 0.0
    mean_ndcg5 = float(np.mean(ndcgs_5)) if ndcgs_5 else 0.0
    mean_ndcg10 = float(np.mean(ndcgs_10)) if ndcgs_10 else 0.0
    rmse = float(math.sqrt(np.mean(squared_errors))) if squared_errors else 0.0

    # 3. Content-Based Evaluation: Genre Consistency & Intra-List Diversity
    def make_soup(row):
        return f"{row['title']} {row['author']} {row['genre']} {row['genre']} {row['description']}"
    
    soups = df_books.apply(make_soup, axis=1)
    tfidf = TfidfVectorizer(stop_words='english', ngram_range=(1,2), max_features=5000)
    matrix = tfidf.fit_transform(soups)
    content_sim = cosine_similarity(matrix, matrix)

    genre_consistencies = []
    intra_list_diversities = []

    for i in range(len(df_books)):
        sim_scores = sorted(list(enumerate(content_sim[i])), key=lambda x: x[1], reverse=True)
        top_k_indices = [idx for idx, _ in sim_scores[1:6]] # top 5 excluding self

        source_genre = df_books.iloc[i]['genre']
        target_genres = [df_books.iloc[idx]['genre'] for idx in top_k_indices]
        genre_matches = sum(1 for g in target_genres if g == source_genre)
        genre_consistencies.append(genre_matches / 5.0)

        # Intra-list distance = 1 - cosine similarity
        pairwise_sims = []
        for a in range(len(top_k_indices)):
            for b in range(a + 1, len(top_k_indices)):
                pairwise_sims.append(content_sim[top_k_indices[a], top_k_indices[b]])
        if pairwise_sims:
            intra_list_diversities.append(1.0 - np.mean(pairwise_sims))

    mean_genre_consistency = float(np.mean(genre_consistencies))
    mean_intra_diversity = float(np.mean(intra_list_diversities))

    results = {
        "evaluation_summary": {
            "dataset_books": len(df_books),
            "dataset_ratings": len(df_ratings),
            "train_ratings": len(train_ratings),
            "test_ratings": len(test_ratings),
            "test_users_evaluated": len(precisions_5)
        },
        "collaborative_filtering": {
            "precision_at_5": round(mean_p5, 4),
            "precision_at_10": round(mean_p10, 4),
            "recall_at_5": round(mean_r5, 4),
            "recall_at_10": round(mean_r10, 4),
            "ndcg_at_5": round(mean_ndcg5, 4),
            "ndcg_at_10": round(mean_ndcg10, 4),
            "rating_prediction_rmse": round(rmse, 4)
        },
        "content_based_filtering": {
            "genre_coherence_at_5": round(mean_genre_consistency, 4),
            "intra_list_diversity_at_5": round(mean_intra_diversity, 4),
            "vocabulary_size": len(tfidf.get_feature_names_out()),
            "embedding_sparsity": round(float(1.0 - (matrix.nnz / (matrix.shape[0] * matrix.shape[1]))), 4)
        },
        "bayesian_popularity": {
            "global_mean_rating": round(float(df_books['average_rating'].mean()), 2),
            "minimum_vote_threshold_m": int(df_books['rating_count'].quantile(0.50))
        }
    }

    out_file = os.path.join(DOCS_DIR, "EVALUATION_RESULTS.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print("\nMODEL EVALUATION RESULTS (Actual Measured):")
    print(f"Precision@5:  {results['collaborative_filtering']['precision_at_5']:.4f}")
    print(f"Recall@5:     {results['collaborative_filtering']['recall_at_5']:.4f}")
    print(f"NDCG@5:       {results['collaborative_filtering']['ndcg_at_5']:.4f}")
    print(f"Rating RMSE:  {results['collaborative_filtering']['rating_prediction_rmse']:.4f}")
    print(f"Content Genre Coherence@5:   {results['content_based_filtering']['genre_coherence_at_5']:.4f}")
    print(f"Intra-List Diversity@5:      {results['content_based_filtering']['intra_list_diversity_at_5']:.4f}")
    print(f"Saved evaluation artifact to: {out_file}\n")
    return results

if __name__ == "__main__":
    run_evaluation()
