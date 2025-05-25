from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required,
    get_jwt_identity, get_jwt, unset_jwt_cookies
)
from datetime import timedelta

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

jwt = JWTManager(app)

users = {
    "user1": {"password": "parola1", "role": "admin"},
    "user2": {"password": "parola2", "role": "owner"},
    "user3": {"password": "parolaX", "role": "owner"},
}

token_blacklist = set()

#---------------------1--------
@app.route('/auth', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = users.get(username)
    if not user or user["password"] != password:
        return jsonify({"msg": "Invalid credentials"}), 401

    token = create_access_token(
        identity=username,
        additional_claims={"role": user["role"]}
    )
    return jsonify({"token": token}), 200

#---------------------2--------
@app.route('/auth/jwtStore', methods=['GET'])
@jwt_required()
def verify_token():
    jwt_data = get_jwt()
    if jwt_data["jti"] in token_blacklist:
        return jsonify({"msg": "Token invalid"}), 404
    return jsonify({
        "username": get_jwt_identity(),
        "role": jwt_data["role"]
    }), 200

#---------------------3--------
@app.route('/auth/jwtStore', methods=['DELETE'])
@jwt_required()
def logout():
    jwt_data = get_jwt()
    token_blacklist.add(jwt_data["jti"])
    response = jsonify({"msg": "Logout"})
    unset_jwt_cookies(response)
    return response, 200


if __name__ == '__main__':
    app.run()

