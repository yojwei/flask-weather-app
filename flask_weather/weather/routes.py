import requests
from flask import request, render_template, flash, current_app
from . import weather_bp
from .forms import SearchForm


@weather_bp.route("/search", methods=["GET", "POST"])
def search():
    """天氣搜尋"""
    form = SearchForm()
    weather_data = None

    if form.validate_on_submit():
        city = form.city.data
        api_key = current_app.config.get("OPENWEATHER_API_KEY")

        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=zh_tw"
        response = requests.get(url)

        if response.status_code == 200:
            weather_data = response.json()
            return render_template("weather.html", city=city, data=weather_data)

        flash(f"無法取得 {city} 的天氣資訊，請確認城市名稱是否正確。", "danger")

    return render_template("index.html", form=form)


@weather_bp.route("", methods=["GET"])
def get_weather():
    """天氣查詢（查詢參數）"""
    city = request.args.get("city", "未指定")
    return {"status": "ok", "city": city, "message": f"{city} 的天氣資訊"}


@weather_bp.route("/<city>", methods=["GET"])
def weather_api(city):
    """天氣查詢（路徑參數）"""
    return {"status": "ok", "city": city, "message": f"{city} 的天氣資訊"}
