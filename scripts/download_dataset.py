"""
BookWise AI — Optional External Dataset Downloader
Provides instructions and helper utilities to ingest larger public book datasets
such as the Book-Crossing dataset or Goodreads 10k dataset.
"""
import os
import urllib.request

DATASETS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "datasets"))

def info():
    print("=" * 60)
    print("BOOKWISE AI — EXTERNAL DATASET INGESTION UTILITY")
    print("=" * 60)
    print("The current project already runs out-of-the-box with a high quality,")
    print("curated dataset of 165 real books and 3,868 user ratings.")
    print("\nTo scale to massive external datasets:")
    print("1. Goodreads 10k: https://github.com/zygmuntz/goodbooks-10k")
    print("2. Book-Crossing: http://www2.informatik.uni-freiburg.de/~cziegler/BX/")
    print("\nDownload books.csv and ratings.csv and place them in the datasets/ directory.")
    print("Then re-run: python scripts/evaluate_model.py")
    print("=" * 60)

if __name__ == '__main__':
    info()
