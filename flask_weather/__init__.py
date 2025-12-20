from flask import Flask
from flask_weather.config import get_config
from flask_weather.routes import register_routes


def create_app():
    """應用程式工廠函數"""
    app = Flask(__name__)

    # Load configuration
    config = get_config()
    app.config.from_object(config)

    # Register routes
    register_routes(app)

    return app
