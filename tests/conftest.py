import os
import pytest
from flask_weather import create_app, db
from flask_weather.config import TestingConfig
from flask_weather.models import User


@pytest.fixture
def app():
    """建立測試用的應用程式"""
    # 設定 FLASK_ENV 環境變數，確保使用測試配置
    os.environ["FLASK_ENV"] = "testing"

    app = create_app()
    app.config.from_object(TestingConfig)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """建立測試用的客戶端"""
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
