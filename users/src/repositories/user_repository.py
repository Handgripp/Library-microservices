import uuid
from werkzeug.security import generate_password_hash
from src.models.user_model import Users
from src.extensions import db


class UserRepository:

    @staticmethod
    def create_user(email, password, role):
        hashed_password = generate_password_hash(password, method='sha256')

        new_user = Users(id=str(uuid.uuid4()), email=email, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()

    @staticmethod
    def get_one_by_id(user_id):
        user = Users.query.filter_by(id=user_id).first()
        if not user:
            return None

        user_data = {
            'id': user.id,
            'email': user.email,
            'role': user.role
        }

        return user_data

