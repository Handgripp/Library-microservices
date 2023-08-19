from flask import Flask
import os
from src.controllers.user_controller import user_blueprint


SERVICE1_URL = "http://localhost:5001"


def create_app():
    app = Flask(__name__)
    app_key = os.getenv("APP_KEY")
    app.config['SECRET_KEY'] = app_key

    app.register_blueprint(user_blueprint)

    return app
