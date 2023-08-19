from flask import jsonify, Blueprint, request
from src.models.user_model import Users
from src.repositories.user_repository import UserRepository

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route("/users", methods=["POST"])
def create_owner():
    data = request.json
    email = Users.query.filter_by(email=data['email']).first()

    correlation_id = data.get('correlation_id')

    if email:
        return jsonify({'error': 'User with that email already exists'}), 409

    UserRepository.create_user(
        data['email'],
        data['password'],
        data['role']
    )

    print("microservice users create user:", correlation_id)

    return jsonify({'message': 'New user created'}), 201

