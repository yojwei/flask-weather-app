from flask import jsonify, render_template
from . import taiwan_weather_bp
from flask_weather.utils import get_cwa_cities, get_cwa_weather


@taiwan_weather_bp.route("/taiwan")
def page():
    return render_template("taiwan_weather.html")


@taiwan_weather_bp.route("/taiwan/cities")
def cities():
    return jsonify({"success": True, "data": get_cwa_cities()})


@taiwan_weather_bp.route("/taiwan/weather/<city_code>")
def weather(city_code):
    data = get_cwa_weather(city_code)
    if not data:
        return (
            jsonify(
                {
                    "success": False,
                    "error": "查無資料",
                    "message": "無法取得該縣市天氣資料",
                }
            ),
            404,
        )

    return jsonify({"success": True, "data": data})
