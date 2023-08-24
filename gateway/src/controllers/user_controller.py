from flask import jsonify, Blueprint, request
import requests
import uuid
from src.controllers.auth_controller import token_required
from constans import USERS_MICROSERVICE_URL

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route("/users", methods=["POST"])
def create_user():
    data = request.json
    correlation_id = str(uuid.uuid4())

    print("gateway create user:", correlation_id)

    response = requests.post(f"{USERS_MICROSERVICE_URL}/users", json=data,
                             headers={'correlation_id': correlation_id})

    return jsonify(response.json()), response.status_code


@user_blueprint.route("/users/<user_id>", methods=["GET"])
@token_required
def get_user(current_user, user_id):
    correlation_id = str(uuid.uuid4())
    print("gateway get user:", correlation_id)

    if current_user['role'] == 'admin':
        response = requests.get(
            f"{USERS_MICROSERVICE_URL}/users/{user_id}",
            headers={'correlation_id': correlation_id}
        )
        return jsonify(response.json()), response.status_code
    return jsonify({'error': 'Forbidden'}), 403
