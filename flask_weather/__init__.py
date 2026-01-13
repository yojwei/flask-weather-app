from flask import Flask
from flask_weather.config import get_config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = "auth.login"
login.login_message = "請先登入以存取此頁面。"
cache = Cache()
limiter = Limiter(key_func=get_remote_address)


def create_app():
    """應用程式工廠函數"""
    app = Flask(__name__)

    # Load configuration
    config = get_config()
    app.config.from_object(config)

    # Initial db
    db.init_app(app)

    # Initialize migration
    migrate.init_app(app, db)

    # 重要：確保 models 被導入，Flask-Migrate 才能偵測到資料表變化
    with app.app_context():
        from flask_weather import models

    # 初始化登入管理
    login.init_app(app)

    # 初始化快取
    # 設定快取類型為 SimpleCache (開發用，存在記憶體中)
    # 生產環境建議使用 RedisCache
    app.config["CACHE_TYPE"] = "SimpleCache"
    app.config["CACHE_DEFAULT_TIMEOUT"] = 300  # 預設快取 5 分鐘
    cache.init_app(app)

    # 自訂 Jinja2 過濾器 icon 和 datetimeformat
    from .utils import get_weather_icon_class
    from datetime import datetime

    app.jinja_env.filters["weather_icon"] = get_weather_icon_class

    def datetimeformat(timestamp, fmt="%Y-%m-%d %H:%M:%S"):
        """將 timestamp 轉換為格式化的日期時間字符串"""
        return datetime.fromtimestamp(timestamp).strftime(fmt)

    app.jinja_env.filters["datetimeformat"] = datetimeformat

    # content_security_policy 設為 None 是因為我們用了 CDN (Tailwind, Alpine)
    # 生產環境建議嚴格設定 CSP
    limiter.init_app(app)

    # 安全性設置
    if app.config.get("TALISMAN_ENABLED", True):
        Talisman(app, content_security_policy=None)

    # 從子模組導入並註冊藍圖
    from .main import main_bp
    from .weather import weather_bp
    from .auth import auth_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(weather_bp, url_prefix="/weather")
    app.register_blueprint(auth_bp, url_prefix="/auth")

    # 錯誤處理
    @app.errorhandler(404)
    def page_not_found(e):
        return "<h1>404 - 找不到頁面</h1><p>請檢查您的網址是否正確。</p>", 404

    return app
