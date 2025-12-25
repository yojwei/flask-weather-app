"""Flask Weather App Configuration"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration"""

    DEBUG = False
    TESTING = False

    # CSRF settings
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-scret-key"


class DevelopmentConfig(Config):
    """Development configuration"""

    DEBUG = True
    ENV = "development"


class TestingConfig(Config):
    """Testing configuration"""

    TESTING = True
    ENV = "testing"


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
