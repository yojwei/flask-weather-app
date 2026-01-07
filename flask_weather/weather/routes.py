from flask import request, render_template, flash, redirect, url_for
from . import weather_bp
from .forms import SearchForm
from flask_login import login_required, current_user
from flask_weather import db
from flask_weather.models import SavedCity
from flask_weather.utils import (
    get_current_weather,
    format_weather_data,
    get_weather_by_coords,
    get_forecast,
    get_forecast_by_coords,
    format_forecast_data,
    prepare_chart_data,
)


def _check_if_city_saved(city_name):
    """檢查城市是否已被當前使用者收藏"""
    if not current_user.is_authenticated:
        return False
    return (
        SavedCity.query.filter_by(
            user_id=current_user.id,
            city_name=city_name,
        ).first()
        is not None
    )


def _render_weather_result(weather_data, forecast, city=None):
    """渲染天氣結果頁面的共用函數"""
    if not weather_data or not forecast:
        return None

    formatted_weather = format_weather_data(weather_data)
    formatted_forecast = format_forecast_data(forecast)
    chart_data = prepare_chart_data(formatted_forecast)
    is_saved = _check_if_city_saved(formatted_weather["city"])

    return render_template(
        "weather.html",
        city=city,
        data=formatted_weather,
        forecast=formatted_forecast,
        chart_data=chart_data,
        is_saved=is_saved,
    )


def _validate_coordinates(lat, lon):
    """驗證經緯度座標

    Returns:
        tuple: (lat_float, lon_float) 如果有效
        None: 如果無效
    """
    try:
        lat_float = float(lat)
        lon_float = float(lon)

        if not (-90 <= lat_float <= 90) or not (-180 <= lon_float <= 180):
            return None

        return lat_float, lon_float
    except (ValueError, TypeError):
        return None


def _search_city_weather(city):
    """搜尋指定城市的天氣資訊

    Args:
        city: 城市名稱

    Returns:
        Flask response 或 None
    """
    weather_data = get_current_weather(city)
    forecast = get_forecast(city)

    result = _render_weather_result(weather_data, forecast, city=city)
    if result:
        return result

    flash(f"無法取得 {city} 的天氣資訊，請確認城市名稱是否正確。", "danger")
    return None


@weather_bp.route("/search", methods=["GET", "POST"])
def search():
    """天氣搜尋"""
    form = SearchForm()

    # 支持 GET 請求的 city 查詢參數
    city_param = request.args.get("city")
    if city_param and request.method == "GET":
        result = _search_city_weather(city_param)
        if result:
            return result
        return redirect(url_for("weather.search"))

    if form.validate_on_submit():
        result = _search_city_weather(form.city.data)
        if result:
            return result
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
    """根據地理座標搜尋天氣"""
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if not lat or not lon:
        flash("座標資訊錯誤", "danger")
        return redirect(url_for("main.index"))

    coords = _validate_coordinates(lat, lon)
    if not coords:
        flash("座標格式或範圍錯誤", "danger")
        return redirect(url_for("main.index"))

    lat, lon = coords
    weather_data = get_weather_by_coords(lat, lon)
    forecast = get_forecast_by_coords(lat, lon)

    result = _render_weather_result(weather_data, forecast)
    if result:
        return result

    flash("無法取得該位置的天氣資訊", "danger")
    return redirect(url_for("main.index"))


def _get_user_saved_city(city_name):
    """取得使用者收藏的特定城市

    Args:
        city_name: 城市名稱

    Returns:
        SavedCity 物件或 None
    """
    return SavedCity.query.filter_by(
        user_id=current_user.id, city_name=city_name
    ).first()


@weather_bp.route("/save/<city>")
@login_required
def save_city(city):
    """儲存使用者喜愛的城市"""
    if _get_user_saved_city(city):
        flash(f"{city} 已經在您的收藏清單中了。", "info")
    else:
        db.session.add(SavedCity(city_name=city, user=current_user))
        db.session.commit()
        flash(f"已將 {city} 加入收藏！", "success")

    return redirect(request.referrer or url_for("main.index"))


@weather_bp.route("/unsave/<city>")
@login_required
def unsave_city(city):
    """移除使用者喜愛的城市"""
    saved_city = _get_user_saved_city(city)

    if saved_city:
        db.session.delete(saved_city)
        db.session.commit()
        flash(f"已移除 {city}。", "success")
    else:
        flash(f"找不到收藏紀錄。", "warning")

    return redirect(request.referrer or url_for("main.index"))
