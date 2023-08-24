import uuid

from flask import jsonify, Blueprint, request
from src.models.user_model import Users
from src.repositories.user_repository import UserRepository

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route("/users", methods=["POST"])
def create_owner():
    data = request.json
    user = UserRepository.get_user_by_email(data["email"])

    correlation_id = request.headers.get('correlation_id')

    if user:
        return jsonify({'error': 'User with that email already exists'}), 409

    UserRepository.create_user(
        data['email'],
        data['password'],
        data['role']
    )

    print("microservice users create user:", correlation_id)

    return jsonify({'message': 'New user created'}), 201


@user_blueprint.route('/users/<user_id>', methods=['GET'])
def get_one_user(user_id):
    try:
        uuid.UUID(user_id, version=4)
    except ValueError:
        return jsonify({'error': 'Invalid uuid format'}), 400

    correlation_id = request.headers.get('correlation_id')

    user_data = UserRepository.get_user_by_id(user_id)
    print("microservice users get one:", correlation_id)
    if not user_data:
        return jsonify({'error': 'No user found!'}), 404

    return jsonify(user_data), 200


@user_blueprint.route("/users/login", methods=["POST"])
def check_user():
    data = request.json
    user = None
    if data.get('email'):
        email = data.get('email')
        user = UserRepository.get_user_by_email(email)
    if data.get('id'):
        user_id = data.get('id')
        user = UserRepository.get_user_by_id(user_id)

    if user:
        return jsonify(user), 200
    else:
        return jsonify({'error': 'Bad request'}), 400
