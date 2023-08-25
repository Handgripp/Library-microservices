import uuid
from src.models.rent_model import Rents
from src.extensions import db


class RentRepository:

    @staticmethod
    def rent(user_id, book_id, rent_from, rent_to):
        new_rent = Rents(id=str(uuid.uuid4()), user_id=user_id, book_id=book_id, rent_from=rent_from, rent_to=rent_to)
        db.session.add(new_rent)
        db.session.commit()

    @staticmethod
    def get_one_by_id(rent_id):
        rent = Rents.query.filter_by(id=rent_id).first()
        if not rent:
            return None

        rent_data = {
            'id': rent.id,
            'user_id': rent.user_id,
            'book_id': rent.book_id,
            'rent_from': rent.rent_from,
            'rent_to': rent.rent_to,
            'returned': rent.returned
        }

        return rent_data

    @staticmethod
    def return_book(rent_id):
        rent = Rents.query.filter_by(id=rent_id).first()
        rent.returned = True
        db.session.commit()
