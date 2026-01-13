import os
import pytest
from flask_login import login_user
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

        # 創建測試用戶
        test_user = User(username="testuser", email="test@example.com")
        test_user.set_password("password123")
        db.session.add(test_user)
        db.session.commit()

        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """建立已認證的測試客戶端"""
    with app.test_client() as client:
        with client.session_transaction() as sess:
            user = User.query.filter_by(username="testuser").first()
            login_user(user)
        yield client


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
