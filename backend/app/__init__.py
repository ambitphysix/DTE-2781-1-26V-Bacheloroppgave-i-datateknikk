from flask import Flask
import os

def create_app():
    """
    Initialiserer Flask app og registrerer alle blueprints.
    """
    app = Flask(__name__)
    
    # Get secret key from environment variable
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') 

    if not os.getenv('SECRET_KEY'):
        print("No SECRET_KEY found in environment variables. Please set it in the .env file.")

    from app.main import main as main_bp
    from app.api import api as api_bp

    app.register_blueprint(main_bp, url_prefix='/')
    app.register_blueprint(api_bp, url_prefix='/api')

    return app