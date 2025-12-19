import requests
from jose import jwt
from flask import abort

AUTH0_DOMAIN = "TUO_DOMINIO.auth0.com"
API_AUDIENCE = "https://spam-api"
ALGORITHMS = ["RS256"]

jwks = requests.get(
    f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
).json()

def verify_token(token: str):
    try:
        unverified_header = jwt.get_unverified_header(token)

        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"],
                }

        if not rsa_key:
            abort(401, "Chiave di firma non trovata")

        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=ALGORITHMS,
            audience=API_AUDIENCE,
            issuer=f"https://{AUTH0_DOMAIN}/"
        )
        return payload

    except Exception:
        abort(401, "Token non valido")
