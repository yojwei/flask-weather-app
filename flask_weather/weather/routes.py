from flask import request, render_template, flash, redirect, url_for
from . import weather_bp
from .forms import SearchForm
from flask_weather.utils import (
    get_current_weather,
    format_weather_data,
    get_weather_by_coords,
    get_forecast,
    get_forecast_by_coords,
    format_forecast_data,
    prepare_chart_data,
)


@weather_bp.route("/search", methods=["GET", "POST"])
def search():
    """天氣搜尋"""
    form = SearchForm()
    weather_data = None

    if form.validate_on_submit():
        city = form.city.data

        raw_data = get_current_weather(city)
        forecast = get_forecast(city)  # 新增的預報呼叫

        if raw_data and forecast:
            weather_data = format_weather_data(raw_data)
            forecast = format_forecast_data(forecast)  # 格式化預報資料
            chart_data = prepare_chart_data(forecast)  # 準備圖表資料（如果需要）
            return render_template(
                "weather.html",
                city=city,
                data=weather_data,
                forecast=forecast,
                chart_data=chart_data,
            )
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


@weather_bp.route("/search/geo")
def search_by_geo():
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if not lat or not lon:
        flash("座標資訊錯誤", "danger")
        return redirect(url_for("main.index"))

    try:
        # 驗證座標格式
        lat = float(lat)
        lon = float(lon)

        # 基本範圍檢查
        if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
            flash("座標範圍錯誤", "danger")
            return redirect(url_for("main.index"))

    except ValueError:
        flash("座標格式錯誤", "danger")
        return redirect(url_for("main.index"))

    # 呼叫 Service
    raw_data = get_weather_by_coords(lat, lon)
    forecast = get_forecast_by_coords(lat, lon)

    if raw_data:
        weather_data = format_weather_data(raw_data)
        forecast = format_forecast_data(forecast)
        return render_template("weather.html", data=weather_data, forecast=forecast)
    else:
        flash("無法取得該位置的天氣資訊", "danger")
        return redirect(url_for("main.index"))
