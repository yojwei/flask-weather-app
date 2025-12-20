"""Routes module for Flask Weather App"""

from flask import request


def register_routes(app):
    """Register routes with the Flask app"""

    @app.route("/")
    def index():
        """Home page"""
        return "這是首頁"

    @app.route("/search", methods=["GET", "POST"])
    def search():
        if request.method == "POST":
            # 處理表單提交
            city = request.form.get("city")
            return f"您正在搜尋：{city}"
        # GET 請求則顯示搜尋頁面
        return "請輸入城市名稱進行搜尋"

    @app.route("/weather", methods=["GET"])
    def get_weather():
        """Weather API endpoint with query parameter"""
        city = request.args.get("city", "未指定")
        return {"status": "ok", "city": city, "message": f"{city} 的天氣資訊"}

    @app.route("/api/weather/<city>", methods=["GET"])
    def weather_api(city):
        """Weather API endpoint"""
        return {"status": "ok", "city": city, "message": f"{city} 的天氣資訊"}

    @app.errorhandler(404)
    def page_not_found(e):
        # 返回自定義內容與 404 狀態碼
        return "<h1>404 - 找不到頁面</h1><p>請檢查您的網址是否正確。</p>", 404
