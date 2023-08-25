from flask import jsonify, Blueprint, request
import requests
import uuid
from src.controllers.auth_controller import token_required
from constans import RENTS_MICROSERVICE_URL

rent_blueprint = Blueprint('rent', __name__)


@rent_blueprint.route("/books/<book_id>/rent", methods=["POST"])
@token_required
def rent(current_user, book_id):
    data = request.json
    correlation_id = str(uuid.uuid4())

    print("gateway made rent:", correlation_id)

    response = requests.post(f"{RENTS_MICROSERVICE_URL}/books/{book_id}/rent", json=data,
                             headers={'correlation_id': correlation_id, 'user_id': current_user['id']})

    return jsonify(response.json()), response.status_code


@rent_blueprint.route("/books/<rent_id>/return", methods=["POST"])
@token_required
def return_book(current_user, rent_id):
    correlation_id = str(uuid.uuid4())

    print("gateway made rent:", correlation_id)

    response = requests.post(f"{RENTS_MICROSERVICE_URL}/books/{rent_id}/return",
                             headers={'correlation_id': correlation_id, 'user_id': current_user['id']})

    return jsonify(response.json()), response.status_code


@rent_blueprint.route("/rents/<rent_id>", methods=["GET"])
@token_required
def get_rent(current_user, rent_id):
    correlation_id = str(uuid.uuid4())
    print("gateway get rent:", correlation_id)

    if current_user['role'] == 'admin':
        response = requests.get(
            f"{RENTS_MICROSERVICE_URL}/rents/{rent_id}",
            headers={'correlation_id': correlation_id}
        )
        return jsonify(response.json()), response.status_code
    return jsonify({'error': 'Forbidden'}), 403
