import pytest
from flask_weather import create_app


@pytest.fixture
def app():
    """建立測試用的應用程式"""
    app = create_app()
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    """建立測試用的客戶端"""
    return app.test_client()
