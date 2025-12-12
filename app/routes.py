from flask import request, jsonify
import logging
from .exception import APIError

logger = logging.getLogger(__name__)

def register_routes(app):

    @app.route('/predict/<model_type>', methods=['GET'])
    def predict_dynamic(model_type):
        # legge 'text' da query string/form prima, poi da JSON body se necessario
        raw_text = request.values.get('text')  # handles query string and form data
        if raw_text is None:
            json_body = request.get_json(silent=True) or {}
            raw_text = json_body.get('text')

        input_text = raw_text.strip() if isinstance(raw_text, str) else None
        logger.info("Received prediction request for model '%s' with text: %s", model_type, input_text)

        if not input_text:
            raise APIError('Parametro "text" mancante nella query string o body.', status_code=400)

        try:
            prediction_service = app.model_registry.get_model(model_type)
        except ValueError as e:
            raise APIError(str(e), status_code=404)

        try:
            results = prediction_service.predict(input_text)
        except Exception as exc:
            logger.exception("Errore durante la previsione")
            raise APIError("Errore interno durante la previsione.", status_code=500) from exc

        return jsonify({
            'status': 'success',
            'model_used': model_type,
            'input_text': input_text,
            **results
        })

    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({'status': 'ok'}), 200
