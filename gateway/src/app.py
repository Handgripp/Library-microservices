from flask import Flask
import os
from src.controllers.gateway_controller import gateway_blueprint


SERVICE1_URL = "http://localhost:5001"
SERVICE2_URL = "http://localhost:5002"

def create_app():
    app = Flask(__name__)
    app_key = os.getenv("APP_KEY")
    app.config['SECRET_KEY'] = app_key

    app.register_blueprint(gateway_blueprint)

    return app
