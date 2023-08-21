import datetime
import time
import jwt
from flask import jsonify, Blueprint, request, current_app
from werkzeug.security import check_password_hash
import requests
auth_blueprint = Blueprint('auth', __name__)

USERS_MICROSERVICE_URL = "http://localhost:5001"


@auth_blueprint.route('/login', methods=['POST'])
def login():
    secret_key = current_app.config['SECRET_KEY']
    data = request.get_json()
    correlation_id = data.get('correlation_id')
    if not data or not data['email'] or not data['password']:
        return jsonify({'error': 'Invalid credentials'}), 401

    email = data['email']
    st = time.time()
    response = requests.post(f"{USERS_MICROSERVICE_URL}/users/login", json={'email': email})
    end = time.time()
    finish = end - st
    print(finish)
    user_exists = response.json()

    print("auth correlation_id: ", correlation_id)
    if user_exists and 'password' in user_exists and check_password_hash(user_exists['password'], data['password']):
        token = jwt.encode(
            {'id': str(user_exists['id']), 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
             'role': 'admin'},
            secret_key,
            algorithm='HS256')
        return jsonify({'token': token}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

