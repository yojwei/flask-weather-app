from flask import request
from . import weather_bp


@weather_bp.route("/search", methods=["GET", "POST"])
def search():
    """天氣搜尋"""
    if request.method == "POST":
        city = request.form.get("city")
        return f"您正在搜尋：{city}"
    return "請輸入城市名稱進行搜尋"


@weather_bp.route("", methods=["GET"])
def get_weather():
    """天氣查詢（查詢參數）"""
    city = request.args.get("city", "未指定")
    return {"status": "ok", "city": city, "message": f"{city} 的天氣資訊"}


@weather_bp.route("/<city>", methods=["GET"])
def weather_api(city):
    """天氣查詢（路徑參數）"""
    return {"status": "ok", "city": city, "message": f"{city} 的天氣資訊"}
