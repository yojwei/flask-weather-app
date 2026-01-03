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
        "condition": data["weather"][0]["main"],  # 例如 'Clouds', 'Rain'
        "dt": datetime.fromtimestamp(data["dt"]).strftime("%Y-%m-%d %H:%M"),
    }


def get_weather_icon_class(icon_code):
    """
    將 OpenWeatherMap icon code 對應到 Remix Icon
    參考: https://remixicon.com/
    """
    mapping = {
        "01d": "ri-sun-fill text-yellow-500",  # 晴天 (日)
        "01n": "ri-moon-fill text-gray-200",  # 晴天 (夜)
        "02d": "ri-sun-cloudy-fill text-gray-500",  # 少雲 (日)
        "02n": "ri-moon-cloudy-fill text-gray-400",  # 少雲 (夜)
        "03d": "ri-cloudy-fill text-gray-500",  # 多雲
        "03n": "ri-cloudy-fill text-gray-400",
        "04d": "ri-cloudy-2-fill text-gray-600",  # 陰天
        "04n": "ri-cloudy-2-fill text-gray-500",
        "09d": "ri-showers-fill text-blue-400",  # 毛毛雨
        "09n": "ri-showers-fill text-blue-300",
        "10d": "ri-rain-fill text-blue-500",  # 雨天
        "10n": "ri-rain-fill text-blue-400",
        "11d": "ri-thunderstorms-fill text-purple-500",  # 雷雨
        "11n": "ri-thunderstorms-fill text-purple-400",
        "13d": "ri-snowy-fill text-blue-200",  # 雪
        "13n": "ri-snowy-fill text-blue-100",
        "50d": "ri-foggy-fill text-gray-400",  # 霧
        "50n": "ri-foggy-fill text-gray-300",
    }
    return mapping.get(icon_code, "ri-question-fill text-gray-500")


def get_weather_by_coords(lat, lon):
    """
    根據經緯度取得當前天氣
    :param lat: 緯度
    :param lon: 經度
    :return: 成功回傳天氣資料字典，失敗回傳 None
    """
    api_key = current_app.config["OPENWEATHER_API_KEY"]
    base_url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
        "units": "metric",
        "lang": "zh_tw",
    }

    try:
        print(f"正在呼叫 API 查詢經緯度 ({lat}, {lon}) 的天氣...")
        response = requests.get(base_url, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code if e.response is not None else 0
        if status_code == 404:
            current_app.logger.warning(
                f"找不到經緯度: ({lat}, {lon}) 的城市"
            )  # 改用 logger
        elif status_code == 401:
            current_app.logger.error("API Key 無效")
        else:
            current_app.logger.error(f"HTTP 錯誤: {e}")
    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"連線錯誤: {e}")
    except ValueError as e:
        current_app.logger.error(f"API 回傳資料格式錯誤: {e}")

    return None
