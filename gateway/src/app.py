from flask import Flask
import os

SERVICE1_URL = "http://localhost:5001"


def create_app():
    app = Flask(__name__)
    app_key = os.getenv("APP_KEY")
    app.config['SECRET_KEY'] = app_key

    return app
