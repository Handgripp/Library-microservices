from flask import jsonify, Blueprint, request
import requests
import uuid

user_blueprint = Blueprint('user', __name__)

USERS_MICROSERVICE_URL = "http://localhost:5001"


@user_blueprint.route("/users", methods=["POST"])
def create_user():
    data = request.json
    correlation_id = str(uuid.uuid4())

    print("gateway create user:", correlation_id)

    data['correlation_id'] = correlation_id

    response = requests.post(f"{USERS_MICROSERVICE_URL}/users", json=data)

    return jsonify(response.json()), response.status_code

