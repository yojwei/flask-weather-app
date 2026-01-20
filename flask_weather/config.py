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

    # Security: Flask-Talisman (HTTPS enforcement)
    # Default to True, set to 'False' in environment to disable (e.g. for local Docker)
    TALISMAN_ENABLED = os.environ.get("TALISMAN_ENABLED", "True").lower() == "true"

    # OpenWeatherMap API settings
    OPENWEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY")

    # ...
    # Zeabur 等平台會提供 DATABASE_URL 環境變數
    # 如果沒有，則退回使用 SQLite (本地開發)
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "app.db")

    # 修正某些平台的 Postgres URL 開頭 (postgres:// -> postgresql://)
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace(
            "postgres://", "postgresql://", 1
        )

        # 設定 Limiter 的儲存後端
    # 如果有設定環境變數就用 Redis，沒有就退回記憶體 (開發用)
    RATELIMIT_STORAGE_URI = os.environ.get("RATELIMIT_STORAGE_URI", "memory://")


class DevelopmentConfig(Config):
    """Development configuration"""

    DEBUG = True
    ENV = "development"
    WTF_CSRF_ENABLED = False  # 測試時關閉 CSRF 驗證方便測試
    TALISMAN_ENABLED = False  # 測試時禁用 Talisman 以避免 HTTPS 重定向


class TestingConfig(Config):
    """Testing configuration"""

    TESTING = True
    ENV = "testing"
    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///:memory:"  # 使用記憶體資料庫，速度快且不影響硬碟
    )
    WTF_CSRF_ENABLED = False  # 測試時關閉 CSRF 驗證方便測試
    TALISMAN_ENABLED = False  # 測試時禁用 Talisman 以避免 HTTPS 重定向


class ProductionConfig(Config):
    """Production configuration"""

    DEBUG = False
    ENV = "production"
    CACHE_TYPE = "redis"
    CACHE_REDIS_URL = os.environ.get("REDIS_CONNECTION_STRING")


def get_config():
    """Get appropriate config based on environment"""
    env = os.getenv("FLASK_ENV", "development")

    if env == "testing":
        return TestingConfig()
    elif env == "production":
        return ProductionConfig()
    else:
        return DevelopmentConfig()
