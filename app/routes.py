from flask import request, jsonify, make_response
from .auth.decorators import requires_auth
import logging
from .exception import APIError

logger = logging.getLogger(__name__)

def register_routes(app):
    @app.route('/login', methods=['POST'])
    def login():
        user_data = {"user": "user-mock", "role": "admin"}
        token = "mock-jwt-token" 

        response = make_response(jsonify({"status": "success", "user": user_data}))
        
        response.set_cookie(
            'authToken',
            token,
            httponly=True,
            secure=False,
            samesite='Lax',
            max_age=3600
        )
        return response

    @app.route('/api/me', methods=['GET'])
    @requires_auth
    def me():
        token = request.cookies.get('authToken')
        
        return jsonify({"user": {"user": "user-mock", "role": "admin"}})

    @app.route('/logout', methods=['POST'])
    def logout():
        response = make_response(jsonify({"status": "success"}))
        response.set_cookie('authToken', '', expires=0)
        return response

    @app.route('/predict/<model_type>', methods=['POST'])
    @requires_auth
    def predict_dynamic(model_type):
        raw_text = request.values.get('text')
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
