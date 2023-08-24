import uuid

from flask import jsonify
from src.models.book_model import Books
from src.extensions import db


class BookRepository:

    @staticmethod
    def add_book(book_name, number_of_books):
        new_book = Books(id=str(uuid.uuid4()), book_name=book_name, number_of_books=number_of_books)
        db.session.add(new_book)
        db.session.commit()

    @staticmethod
    def get_one_by_id(book_id):
        book = Books.query.filter_by(id=book_id).first()

        if not book:
            return None

        book_data = {
            'id': book.id,
            'book_name': book.book_name,
            'number_of_books': book.number_of_books,
            'created_at': book.added_at,
            'updated_at': book.updated_at
        }

        return book_data

