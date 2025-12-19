from flask import Flask
from flask_weather.config import get_config
from flask_weather.routes import main_bp


def create_app():
    """應用程式工廠函數"""
    app = Flask(__name__)

    # Load configuration
    config = get_config()
    app.config.from_object(config)

    # Register blueprints
    app.register_blueprint(main_bp)

    return app
