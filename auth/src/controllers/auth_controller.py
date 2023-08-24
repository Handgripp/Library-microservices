import datetime
import jwt
from flask import jsonify, Blueprint, request, current_app, app
from werkzeug.security import check_password_hash
import requests
from constans import USERS_MICROSERVICE_URL

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/login', methods=['POST'])
def login():
    secret_key = current_app.config['SECRET_KEY']
    data = request.get_json()
    correlation_id = data.get('correlation_id')
    if not data or not data['email'] or not data['password']:
        return jsonify({'error': 'Invalid credentials'}), 401

    response = requests.post(f"{USERS_MICROSERVICE_URL}/users/login", json={'email': data['email']})
    user_exists = response.json()
    print("auth correlation_id: ", correlation_id)
    print(user_exists)

    if user_exists["role"] == "admin":
        if user_exists and 'password' in user_exists and check_password_hash(user_exists['password'], data['password']):
            token = jwt.encode(
                {'id': str(user_exists['id']), 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
                 'role': 'admin'},
                secret_key,
                algorithm='HS256')
            return jsonify({'token': token}), 200
    elif user_exists["role"] == "guest":
        if user_exists and 'password' in user_exists and check_password_hash(user_exists['password'], data['password']):
            token = jwt.encode(
                {'id': str(user_exists['id']), 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
                 'role': 'guest'},
                secret_key,
                algorithm='HS256')
            return jsonify({'token': token}), 200

    return jsonify({'error': 'Invalid credentials'}), 401

