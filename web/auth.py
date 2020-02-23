from flask import request, jsonify
from web import jwt, bcrypt, app
from web.model import User, RevokedToken, Raspberry
from flask_jwt_extended import create_access_token,  jwt_required, get_raw_jwt


"""
The authentication script, allowing the user to login, logout and adding additional variables to the token
"""


@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400

    email = request.json.get('email', None)
    password = request.json.get('password', None)
    raspberry_id = request.json.get('raspberry_id', None)
    if raspberry_id:
        raspberry = Raspberry.query.filter_by(id=raspberry_id).first()
        if not raspberry:
            return jsonify({"message": "Bad raspberry pi id"}), 401
        ret = {
            'access_token': create_access_token(identity=raspberry.id),
        }
        return jsonify(ret), 200
    else:
        if not email:
            return jsonify({"message": "Missing email parameter"}), 400
        if not password:
            return jsonify({"message": "Missing password parameter"}), 400

        user = User.query.filter_by(email=email).first()
        if not user or not bcrypt.check_password_hash(user.password, password):
            return jsonify({"message": "Bad email or password"}), 401

        # Identity can be any data that is json serializable
        ret = {
            'access_token': create_access_token(identity=user.id),
            'user': user
        }
        return jsonify(ret), 200


# logout


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedToken.is_jti_blacklisted(jti)


@app.route('/logout', methods=['POST'])
@jwt_required
def logout():
    jti = get_raw_jwt()['jti']
    revoked_token = RevokedToken(jti=jti)
    revoked_token.add()
    return jsonify({"message": "Successfully logged out"}), 200