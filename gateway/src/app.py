from flask import Flask
import os
from src.controllers.user_controller import user_blueprint
from src.controllers.auth_controller import auth_blueprint


def create_app():
    app = Flask(__name__)
    app_key = os.getenv("APP_KEY")
    app.config['SECRET_KEY'] = app_key

    app.register_blueprint(user_blueprint)
    app.register_blueprint(auth_blueprint)

    return app
