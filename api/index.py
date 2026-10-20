import sys
import os

# Ensure Vercel serverless functions write SQLite to writable /tmp
os.environ.setdefault('DATABASE_URL', 'sqlite:////tmp/test.db')

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from backend.run import app

app = app
