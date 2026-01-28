from flask import Blueprint

taiwan_weather_bp = Blueprint("taiwan_weather", __name__)

from . import routes  # noqa: E402,F401
