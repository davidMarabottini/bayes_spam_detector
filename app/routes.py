from flask import request, jsonify, make_response, g
from .auth.decorators import requires_auth
import logging
from .exception import APIError
from .services.auth_service import AuthService
from .services.user_service import UserService

logger = logging.getLogger(__name__)

def register_routes(app):
    @app.route('/login', methods=['POST'])
    
    def login():
        data = request.get_json()
        response, error = AuthService.login_user(data.get('username'), data.get('password'))
        
        if error:
            return jsonify({"status": "error", "message": error}), 401
        return response

    @app.route('/logout', methods=['POST'])
    def logout():
        return AuthService.logout_user()

    @app.route('/api/me', methods=['GET'])
    @requires_auth
    def me():
        user = g.current_user
        return jsonify({
            "id": user.id,
            "user": user.username,
            "role": [r.name for r in user.roles]
        })

    @app.route('/api/users/me', methods=['GET'])
    @requires_auth
    def get_me():
        user = g.current_user
        return jsonify({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "gender": user.gender,
            "name": user.name,
            "surname": user.surname,
            "roles": [r.name for r in user.roles]
        })
    
    @app.route('/api/users/me', methods=['PUT'])
    @requires_auth
    def update_me():
        user = g.current_user
        data = request.get_json()

        updated_user, error = UserService.update_user(user.id, data)

        if error:
            return jsonify({"status": "error", "message": error}), 400

        return jsonify({
            "status": "success",
            "user": {
                "id": updated_user.id,
                "username": updated_user.username,
                "email": updated_user.email,
                "gender": user.gender,
                "name": updated_user.name,
                "surname": updated_user.surname,
                "roles": [r.name for r in updated_user.roles]
            }
        })

        
    @app.route('/api/users', methods=['GET'])
    @requires_auth
    def list_users():
        users = UserService.get_all_users()
        return jsonify([{
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "name": u.name,
            "surname": u.surname,
            "roles": [r.name for r in u.roles]
        } for u in users])

    @app.route('/api/users', methods=['POST'])
    def add_user():
        data = request.get_json()
        data['roles'] = ['user'] 
        user, error = UserService.create_user(data)
        
        if error:
            return jsonify({"status": "error", "message": error}), 400
        
        return jsonify({"status": "success", "id": user.id, "message": "OK"}), 201

    @app.route('/api/users/<int:user_id>', methods=['GET'])
    @requires_auth
    def get_single_user(user_id):
        user, error = UserService.get_single_user(user_id)
        if error:
            return jsonify({"status": "error", "message": error}), 400
        return jsonify(user)
    

    @app.route('/api/users/<int:user_id>', methods=['PUT'])
    @requires_auth
    def update_user(user_id):
        data = request.get_json()
        user, error = UserService.update_user(user_id, data)
        if error:
            return jsonify({"status": "error", "message": error}), 400
        return jsonify({"status": "success", "message": "Utente aggiornato"})

    @app.route('/api/users/<int:user_id>', methods=['DELETE'])
    @requires_auth
    def delete_user(user_id):
        success = UserService.delete_user(user_id)
        if not success:
            return jsonify({"status": "error", "message": "Utente non trovato"}), 404
        return jsonify({"status": "success", "message": "Utente eliminato"})

    # @app.route('/logout', methods=['POST'])
    # def logout():
    #     response = make_response(jsonify({"status": "success"}))
    #     response.set_cookie('authToken', '', expires=0)
    #     return response

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
