from flask import request, render_template
from . import weather_bp


@weather_bp.route("/search", methods=["GET", "POST"])
def search():
    """天氣搜尋"""
    if request.method == "POST":
        city = request.form.get("city")
        return render_template("weather.html", city=city)
    return render_template("index.html")


@weather_bp.route("", methods=["GET"])
def get_weather():
    """天氣查詢（查詢參數）"""
    city = request.args.get("city", "未指定")
    return {"status": "ok", "city": city, "message": f"{city} 的天氣資訊"}


@weather_bp.route("/<city>", methods=["GET"])
def weather_api(city):
    """天氣查詢（路徑參數）"""
    return {"status": "ok", "city": city, "message": f"{city} 的天氣資訊"}
