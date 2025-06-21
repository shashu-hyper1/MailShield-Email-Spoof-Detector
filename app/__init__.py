from flask import Flask
from .routes import main

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_strong_secret_key_here'
    app.config['UPLOAD_FOLDER'] = 'uploads/'
    app.register_blueprint(main)
    return app
