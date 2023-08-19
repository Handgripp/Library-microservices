from flask import Flask
import os
from src.extensions import db
from src.controllers.user_controller import user_blueprint

SERVICE1_URL = "http://localhost:5001"


def create_app():
    app = Flask(__name__)
    app_key = os.getenv("APP_KEY")
    app.config['SECRET_KEY'] = app_key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@localhost:5432/dbname'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(user_blueprint)

    return app
