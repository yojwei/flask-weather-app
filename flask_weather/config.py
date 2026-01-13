"""Flask Weather App Configuration"""

import os
from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base configuration"""

    DEBUG = False
    TESTING = False

    # CSRF settings
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-scret-key"

    # OpenWeatherMap API settings
    OPENWEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY")

    # SQLite settings
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "app.db")


class DevelopmentConfig(Config):
    """Development configuration"""

    DEBUG = True
    ENV = "development"


class TestingConfig(Config):
    """Testing configuration"""

    TESTING = True
    ENV = "testing"
    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///:memory:"  # 使用記憶體資料庫，速度快且不影響硬碟
    )
    WTF_CSRF_ENABLED = False  # 測試時關閉 CSRF 驗證方便測試


class ProductionConfig(Config):
    """Production configuration"""

    DEBUG = False
    ENV = "production"


def get_config():
    """Get appropriate config based on environment"""
    env = os.getenv("FLASK_ENV", "development")

    if env == "testing":
        return TestingConfig()
    elif env == "production":
        return ProductionConfig()
    else:
        return DevelopmentConfig()
