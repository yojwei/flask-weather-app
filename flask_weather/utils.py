"""Utility functions for Flask Weather App"""

import requests
from flask import current_app
from datetime import datetime
from flask_weather import cache


@cache.memoize(timeout=600)  # 快取 10 分鐘
def get_current_weather(city):
    """
    取得指定城市的當前天氣
    :param city: 城市名稱
    :return: 成功回傳天氣資料字典，失敗回傳 None
    """
    api_key = current_app.config["OPENWEATHER_API_KEY"]
    base_url = "https://api.openweathermap.org/data/2.5/weather"

    params = {"q": city, "appid": api_key, "units": "metric", "lang": "zh_tw"}

    try:
        print(f"正在呼叫 API 查詢 {city}...")
        response = requests.get(base_url, params=params, timeout=5)
        response.raise_for_status()  # 如果狀態碼不是 200，會拋出 HTTPError
        return response.json()
    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code if e.response is not None else 0
        if status_code == 404:
            current_app.logger.warning(f"找不到城市: {city}")  # 改用 logger
        elif status_code == 401:
            current_app.logger.error("API Key 無效")
        else:
            current_app.logger.error(f"HTTP 錯誤: {e}")
    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"連線錯誤: {e}")
    except ValueError as e:  # 捕捉 JSON 解析錯誤
        current_app.logger.error(f"API 回傳資料格式錯誤: {e}")

    return None


def format_weather_data(data):
    """
    將 OpenWeatherMap 的原始資料轉換為前端易用的格式
    """
    if not data:
        return None

    return {
        "city": data["name"],
        "country": data["sys"]["country"],
        "temp": round(data["main"]["temp"], 1),
        "feels_like": round(data["main"]["feels_like"], 1),
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "pressure": data["main"]["pressure"],
        "description": data["weather"][0]["description"],
        "icon": data["weather"][0]["icon"],
        "dt": datetime.fromtimestamp(data["dt"]).strftime("%Y-%m-%d %H:%M"),
    }
