from functools import wraps
import jwt
from flask import jsonify, Blueprint, request, current_app
import requests
import uuid
from constans import USERS_MICROSERVICE_URL, AUTH_MICROSERVICE_URL

auth_blueprint = Blueprint('auth', __name__)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        secret_key = current_app.config['SECRET_KEY']

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return jsonify({'error': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, 'thisissecret', algorithms=['HS256'])
            response = requests.post(f"{USERS_MICROSERVICE_URL}/users/login", json={'id': data['id']})
            current_user = response.json()

            if not current_user:
                return jsonify({'error': 'User not found'}), 401
            kwargs['current_user'] = current_user
            return f(*args, **kwargs)
        except jwt.exceptions.DecodeError:
            return jsonify({'error': 'Token is invalid!'}), 401

    return decorated


@auth_blueprint.route("/login", methods=["POST"])
def auth():
    data = request.json
    correlation_id = str(uuid.uuid4())

    print("gateway auth:", correlation_id)

    data['correlation_id'] = correlation_id

    response = requests.post(f"{AUTH_MICROSERVICE_URL}/login", json=data)
    if response.status_code == 200:
        return jsonify(response.json()), response.status_code
    return response.json(), response.status_code
