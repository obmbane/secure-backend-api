from flask import Flask, request, jsonify
from flask_cors import CORS
from jose import jwt
import requests

app = Flask(__name__)
CORS(app)

TENANT_ID = "738134d3-44fa-4fe0-9efa-e4310ffb2bea"
CLIENT_ID = "d44509c3-58b3-4885-a9f2-df1508a8cd4f"
API_AUDIENCE = f"api://{CLIENT_ID}"
JWKS_URL = f"https://login.microsoftonline.com/{TENANT_ID}/discovery/v2.0/keys"
ISSUER = f"https://sts.windows.net/{TENANT_ID}/"

# Cache JWKS
jwks = requests.get(JWKS_URL).json()["keys"]

def get_token_auth_header():
    auth = request.headers.get("Authorization", None)
    if not auth or not auth.startswith("Bearer "):
        raise Exception("Missing or invalid Authorization header")
    return auth.split(" ")[1]

def verify_jwt(token):
    try:
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if not rsa_key:
            raise Exception("Unable to find appropriate key")

        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=["RS256"],
            audience=API_AUDIENCE,
            issuer=ISSUER
        )
        return payload
    except Exception as e:
        raise Exception(f"Token verification failed: {str(e)}")

@app.route("/api/inventory", methods=["GET"])
def get_inventory():
    username = (
    payload.get("preferred_username")
    or payload.get("unique_name")
    or payload.get("email")
    or payload.get("name")
    or "unknown")
    try:
        token = get_token_auth_header()
        payload = verify_jwt(token)
        return jsonify({"message": "Access granted", "user": username})
    except Exception as e:
        return jsonify({"error": str(e)}), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
