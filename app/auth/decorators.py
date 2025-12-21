from functools import wraps
from flask import request, jsonify

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('authToken')
        
        if not token:
            return jsonify({"error": "Sessione mancante o scaduta"}), 401
        return f(*args, **kwargs)
    return decorated
