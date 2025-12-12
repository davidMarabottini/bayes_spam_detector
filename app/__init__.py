# app/__init__.py
import os
import sys
from flask import Flask
from .routes import register_routes
from .services.model_registry import ModelRegistry

def create_app():
    app = Flask(__name__)

    app_root = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(app_root)

    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    try:
        app.model_registry = ModelRegistry(root_dir=app_root)
    except Exception as e:
        sys.stderr.write(f"FATAL: Errore durante l'inizializzazione del Registro Modelli: {e}\n")
        sys.exit(1)

    register_routes(app)
    return app
