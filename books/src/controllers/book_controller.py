import uuid
from flask import jsonify, Blueprint, request
from src.models.book_model import Books
from src.repositories.book_repository import BookRepository

book_blueprint = Blueprint('book', __name__)


@book_blueprint.route("/books", methods=["POST"])
def create_owner():
    data = request.json
    book_name = Books.query.filter_by(book_name=data['book_name']).first()

    correlation_id = request.headers.get('correlation_id')

    if book_name:
        return jsonify({'error': 'Book with that name already exists'}), 409

    BookRepository.add_book(
        data['book_name'],
        data['number_of_books']
    )

    print("microservice books create book:", correlation_id)

    return jsonify({'message': 'New book added'}), 201


@book_blueprint.route('/books/<book_id>', methods=['GET'])
def get_one_book(book_id):
    try:
        uuid.UUID(book_id, version=4)
    except ValueError:
        return jsonify({'error': 'Invalid uuid format'}), 400

    correlation_id = request.headers.get('correlation_id')

    book_data = BookRepository.get_one_by_id(book_id)

    print("microservice books get one:", correlation_id)
    if not book_data:
        return jsonify({'error': 'No book found!'}), 404

    return jsonify(book_data), 200


