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



