from flask import Flask

def create_app():
    """
    Initialiserer Flask app og registrerer alle blueprints.
    """
    app = Flask(__name__)

    from app.main.routes import main
    from app.api.routes import api

    app.register_blueprint(main)
    app.register_blueprint(api)

    return app