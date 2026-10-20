import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from backend.run import app as application
    app = application
except Exception as e:
    # fallback if app is in backend/app.py or backend/__init__.py
    try:
        from backend.app import app
    except:
        from backend import app

# Vercel needs 'app' variable
# def handler(event, context): return app(event, context)
