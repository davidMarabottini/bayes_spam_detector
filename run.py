import os
import logging
from app import create_app
from flask_cors import CORS

app = create_app()

CORS(app, resources={
        r"/predict/*": {
            "origins": ["http://localhost:5173"],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "X-Origin-Site"]
        }
    })

def configure_logging():
    level = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(
        level=getattr(logging, level, logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

def attach_app_components(app):
    try:
        from app.routes import register_routes
        from app.exception import register_error_handlers
        from app.services.model_registry import ModelRegistry
    except Exception as e:
        logging.getLogger(__name__).exception("Errore importando componenti dell'app: %s", e)
        return

    try:
        register_error_handlers(app)
    except Exception:
        logging.getLogger(__name__).exception("Impossibile registrare error handlers")

    try:
        register_routes(app)
    except Exception:
        logging.getLogger(__name__).exception("Impossibile registrare routes")

    if not hasattr(app, "model_registry") or app.model_registry is None:
        try:
            app.model_registry = ModelRegistry(app.root_path)
            logging.getLogger(__name__).info("ModelRegistry inizializzato su app.")
        except Exception:
            logging.getLogger(__name__).exception("Impossibile inizializzare ModelRegistry; le richieste di predict possono fallire.")

def main():
    configure_logging()
    attach_app_components(app)

    host = os.getenv("FLASK_RUN_HOST", "127.0.0.1")
    port = int(os.getenv("FLASK_RUN_PORT", "5000"))
    debug = os.getenv("FLASK_DEBUG", "0").lower() in ("1", "true", "yes")
    logging.getLogger(__name__).info("Starting app (debug=%s) on %s:%s", debug, host, port)
    app.run(host=host, port=port, debug=debug)

if __name__ == "__main__":
    main()