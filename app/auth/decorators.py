from functools import wraps
from flask import request, jsonify, g
from ..services.auth_service import AuthService
from ..models import User

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('authToken')
        if not token:
            return jsonify({"message": "Token mancante"}), 401
        
        user_id = AuthService.decode_token(token)
        if not user_id:
            return jsonify({"message": "Token invalido o scaduto"}), 401
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "Utente non trovato"}), 401
            
        g.current_user = user
        
        return f(*args, **kwargs)
    return decorated

# from functools import wraps
# from flask import request, jsonify

# def requires_auth(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = request.cookies.get('authToken')
        
#         if not token:
#             return jsonify({"error": "Sessione mancante o scaduta"}), 401
#         return f(*args, **kwargs)
#     return decorated
