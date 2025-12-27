from flask import request, render_template, flash, redirect, url_for
from . import weather_bp
from .forms import SearchForm
from flask_weather.utils import get_current_weather, format_weather_data


@weather_bp.route("/search", methods=["GET", "POST"])
def search():
    """天氣搜尋"""
    form = SearchForm()
    weather_data = None

    if form.validate_on_submit():
        city = form.city.data

        raw_data = get_current_weather(city)

        if raw_data:
            weather_data = format_weather_data(raw_data)
            return render_template("weather.html", city=city, data=weather_data)
        else:
            flash(f"無法取得 {city} 的天氣資訊，請確認城市名稱是否正確。", "danger")
            return redirect(url_for("weather.search"))

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
