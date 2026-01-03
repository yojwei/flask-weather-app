from flask import render_template, session, flash, redirect, request, url_for, current_app
from flask_weather.weather.forms import SearchForm
from . import main_bp
from flask_weather import cache
from flask_weather.utils import get_current_weather, get_weather_by_coords


@main_bp.route("/")
def index():
    """Home page"""
    form = SearchForm()
    return render_template("index.html", form=form)


@main_bp.route("/api/weather", methods=["GET"])
def weather_api_root():
    """天氣 API 端點"""
    return {"status": "ok", "message": "天氣 API 端點"}


@main_bp.route("/set_units/<unit>")
def set_units(unit):
    if unit in ["metric", "imperial"]:
        session["units"] = unit
        flash(f"已切換至 {'攝氏 (°C)' if unit == 'metric' else '華氏 (°F)'}", "success")
        # 切換單位後清除與城市/經緯度相關的天氣快取
        try:
            cache.delete_memoized(get_current_weather)
            cache.delete_memoized(get_weather_by_coords)
        except Exception as e:
            current_app.logger.error(f"清除天氣快取失敗: {e}")
    return redirect(request.referrer or url_for("main.index"))
