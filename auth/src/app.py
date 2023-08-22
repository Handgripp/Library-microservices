from dotenv import load_dotenv
from flask import Flask
import os
from src.controllers.auth_controller import auth_blueprint


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

def create_app():
    app = Flask(__name__)
    app_key = os.getenv("APP_KEY")
    app.config['SECRET_KEY'] = app_key
    app.register_blueprint(auth_blueprint)

    return app
