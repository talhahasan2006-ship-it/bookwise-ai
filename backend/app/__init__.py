import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from backend.app.config import Config
from backend.app.models import db
from backend.app.data.loader import load_data
from backend.app.recommender import engine
from backend.app.api import (
    books_bp,
    recs_bp,
    genres_bp,
    stats_bp,
    library_bp,
    health_bp
)

def create_app(config_class=Config):
    possible_dist_dirs = [
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "dist")),
        os.path.abspath(os.path.join(os.getcwd(), "frontend", "dist")),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")),
        os.path.abspath("frontend/dist"),
    ]
    dist_folder = next((d for d in possible_dist_dirs if os.path.exists(d)), possible_dist_dirs[0])
    app = Flask(__name__, static_folder=dist_folder, static_url_path="/")
    app.config.from_object(config_class)

    # Enable CORS for frontend Vite development server and production
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Initialize Database
    db.init_app(app)

    # Wrap DB table creation and warmup in try/except so app always boots on serverless
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print(f"DB init failed (expected on Vercel if no env): {e}")

        # Load datasets and sync DB / warmup engine
        try:
            df_books, df_ratings = load_data(app)
            engine.initialize(df_books, df_ratings)
        except Exception as e:
            print(f"Warning during data loading / engine warmup: {e}")

    # Register API Blueprints
    app.register_blueprint(health_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(recs_bp)
    app.register_blueprint(genres_bp)
    app.register_blueprint(stats_bp)
    app.register_blueprint(library_bp)

    # Serve built React Single Page Application (SPA)
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_frontend(path):
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        elif os.path.exists(os.path.join(app.static_folder, 'index.html')):
            return send_from_directory(app.static_folder, 'index.html')
        else:
            return jsonify({
                'application': 'BookWise AI Backend',
                'status': 'online',
                'note': 'Frontend dist not built. Run npm run build in frontend/.'
            })

    # Error Handlers
    @app.errorhandler(404)
    def not_found(error):
        if os.path.exists(os.path.join(app.static_folder, 'index.html')):
            return send_from_directory(app.static_folder, 'index.html')
        return jsonify({'error': 'Resource not found', 'status': 404}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error', 'status': 500}), 500

    return app
