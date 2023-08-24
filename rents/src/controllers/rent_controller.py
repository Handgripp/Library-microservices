import uuid

import requests
from flask import jsonify, Blueprint, request
from src.repositories.rent_repository import RentRepository
from constans import BOOKS_MICROSERVICE_URL

rent_blueprint = Blueprint('rent', __name__)


@rent_blueprint.route("/rents/books/<book_id>", methods=["POST"])
def rent(book_id):
    data = request.json
    correlation_id = request.headers.get('correlation_id')
    user_id = request.headers.get('user_id')

    response = requests.get(f"{BOOKS_MICROSERVICE_URL}/books/{book_id}")
    print(response)
    if response.status_code != 200:
        return jsonify(response.json()), 404

    RentRepository.rent(
        user_id,
        book_id,
        data['rent_from'],
        data['rent_to']
    )

    print("microservice rents, rent made:", correlation_id)

    return jsonify({'message': 'New rent made'}), 201


@rent_blueprint.route('/rents/<rent_id>', methods=['GET'])
def get_one_user(rent_id):
    try:
        uuid.UUID(rent_id, version=4)
    except ValueError:
        return jsonify({'error': 'Invalid uuid format'}), 400

    correlation_id = request.headers.get('correlation_id')

    rent_data = RentRepository.get_one_by_id(rent_id)
    print("microservice rents get one:", correlation_id)
    if not rent_data:
        return jsonify({'error': 'No rent found!'}), 404

    return jsonify(rent_data), 200


