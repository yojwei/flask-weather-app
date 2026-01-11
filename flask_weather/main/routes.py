from flask import (
    render_template,
    session,
    flash,
    redirect,
    request,
    url_for,
)
from flask_weather.weather.forms import SearchForm
from . import main_bp
from flask_weather.utils import (
    clear_weather_cache,
    get_current_weather,
    format_weather_data,
)
from flask_login import login_required, current_user


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
        clear_weather_cache()
    return redirect(request.referrer or url_for("main.index"))


@main_bp.route("/dashboard")
@login_required
def dashboard():
    page = request.args.get("page", 1, type=int)
    per_page = 6

    pagination = current_user.saved_cities.paginate(
        page=page, per_page=per_page, error_out=False
    )
    saved_cities = pagination.items

    weather_reports = []
    for saved in saved_cities:
        # 逐一查詢天氣 (注意：這可能會很慢，後續需優化)
        raw_data = get_current_weather(saved.city_name)
        if raw_data:
            data = format_weather_data(raw_data)
            weather_reports.append(data)

    return render_template(
        "dashboard.html", reports=weather_reports, pagination=pagination
    )
