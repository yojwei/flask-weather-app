from flask import Flask
from flask_weather.config import get_config


def create_app():
    """應用程式工廠函數"""
    app = Flask(__name__)

    # Load configuration
    config = get_config()
    app.config.from_object(config)

    # 從子模組導入並註冊藍圖
    from .main import main_bp
    from .weather import weather_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(weather_bp, url_prefix="/weather")

    @app.template_filter("datetimeformat")
    def datetimeformat(value, format="%Y-%m-%d %H:%M:%S"):
        from datetime import datetime

        if not value:
            return ""
        try:
            # 確保 value 是數字
            value = float(value) if isinstance(value, str) else value
            return datetime.fromtimestamp(value).strftime(format)
        except (ValueError, TypeError, OSError) as e:
            return f"<無效時間戳: {value}>"

    # 錯誤處理
    @app.errorhandler(404)
    def page_not_found(e):
        return "<h1>404 - 找不到頁面</h1><p>請檢查您的網址是否正確。</p>", 404

    return app
