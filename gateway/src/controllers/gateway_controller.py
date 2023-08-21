import time

from flask import jsonify, Blueprint, request
import requests
import uuid

gateway_blueprint = Blueprint('user', __name__)

USERS_MICROSERVICE_URL = "http://localhost:5001"
AUTH_MICROSERVICE_URL = "http://localhost:5002"


@gateway_blueprint.route("/users", methods=["POST"])
def create_user():
    data = request.json
    correlation_id = str(uuid.uuid4())

    print("gateway create user:", correlation_id)

    data['correlation_id'] = correlation_id

    response = requests.post(f"{USERS_MICROSERVICE_URL}/users", json=data)

    return jsonify(response.json()), response.status_code


@gateway_blueprint.route("/login", methods=["POST"])
def auth():
    data = request.json
    correlation_id = str(uuid.uuid4())

    print("gateway auth:", correlation_id)
    st = time.time()
    requests.get("https://www.google.com")
    end = time.time()
    finish = end - st
    print(finish)
    data['correlation_id'] = correlation_id

    response = requests.post(f"{AUTH_MICROSERVICE_URL}/login", json=data)
    if response.status_code == 200:
        return jsonify(response.json()), response.status_code
    return response.json(), response.status_code

