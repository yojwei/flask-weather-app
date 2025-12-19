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


def test_hello(client):
    """測試根路由"""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Hello, World!" in response.data
