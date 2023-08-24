from flask import jsonify, Blueprint, request
import requests
import uuid
from src.controllers.auth_controller import token_required

from constans import BOOKS_MICROSERVICE_URL

book_blueprint = Blueprint('book', __name__)


@book_blueprint.route("/books", methods=["POST"])
@token_required
def create_user(current_user):
    data = request.json
    correlation_id = str(uuid.uuid4())

    print("gateway add book:", correlation_id)
    if current_user['role'] == 'admin':
        response = requests.post(f"{BOOKS_MICROSERVICE_URL}/books", json=data,
                                 headers={'correlation_id': correlation_id})
        return jsonify(response.json()), response.status_code
    return jsonify({'error': 'Forbidden'}), 403


@book_blueprint.route("/books/<book_id>", methods=["GET"])
@token_required
def get_book(current_user, book_id):
    correlation_id = str(uuid.uuid4())
    print("gateway get book:", correlation_id)
    if current_user['role']:
        response = requests.get(
            f"{BOOKS_MICROSERVICE_URL}/books/{book_id}",
            headers={'correlation_id': correlation_id}
        )
        return jsonify(response.json()), response.status_code
    return jsonify({'error': 'Forbidden'}), 403
