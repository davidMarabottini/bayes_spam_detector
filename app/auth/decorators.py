from functools import wraps
from flask import request, abort
from .jwt_validator import verify_token

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get("Authorization")
        if not auth or not auth.startswith("Bearer "):
            abort(401, "Authorization header mancante")

        token = auth.split(" ")[1]
        request.user = verify_token(token)

        return f(*args, **kwargs)
    return decorated
