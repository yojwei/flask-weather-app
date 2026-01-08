"""Utility functions for Flask Weather App"""

import requests
from flask import current_app, session
from datetime import datetime
from flask_weather import cache
from collections import defaultdict


def _fetch_weather_data(params, timeout=5):
    """
    私有函式：統一處理 OpenWeather API 請求與錯誤處理，成功回傳 JSON，失敗回傳 None
    """
    base_url = "https://api.openweathermap.org/data/2.5/weather"

    try:
        current_app.logger.debug(f"呼叫 OpenWeather API：{params}")
        response = requests.get(base_url, params=params, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        current_app.logger.warning("OpenWeather API 請求逾時")
        return None
    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code if e.response is not None else 0
        if status_code == 404:
            current_app.logger.warning(f"找不到城市或經緯度：{params}")
        elif status_code == 401:
            current_app.logger.error("OpenWeather API Key 無效")
        else:
            current_app.logger.error(f"HTTP 錯誤: {e}")
        return None
    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"連線錯誤: {e}")
        return None
    except ValueError as e:
        current_app.logger.error(f"API 回傳資料格式錯誤: {e}")
        return None


@cache.memoize(timeout=600)  # 快取 10 分鐘
def get_current_weather(city):
    """
    取得指定城市的當前天氣
    :param city: 城市名稱
    :return: 成功回傳天氣資料字典，失敗回傳 None
    """
    api_key = current_app.config.get("OPENWEATHER_API_KEY")
    units = session.get("units", "metric")

    params = {"q": city, "appid": api_key, "units": units, "lang": "zh_tw"}
    return _fetch_weather_data(params)


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
        "sunrise": datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M"),
        "sunset": datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M"),
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
        "10d": "ri-rainy-fill text-blue-500",  # 雨天
        "10n": "ri-rainy-fill text-blue-400",
        "11d": "ri-thunderstorms-fill text-purple-500",  # 雷雨
        "11n": "ri-thunderstorms-fill text-purple-400",
        "13d": "ri-snowy-fill text-blue-200",  # 雪
        "13n": "ri-snowy-fill text-blue-100",
        "50d": "ri-foggy-fill text-gray-400",  # 霧
        "50n": "ri-foggy-fill text-gray-300",
    }
    return mapping.get(icon_code, "ri-question-fill text-gray-500")


@cache.memoize(timeout=600)  # 快取 10 分鐘
def get_weather_by_coords(lat, lon):
    """
    根據經緯度取得當前天氣
    :param lat: 緯度
    :param lon: 經度
    :return: 成功回傳天氣資料字典，失敗回傳 None
    """
    api_key = current_app.config.get("OPENWEATHER_API_KEY")
    units = session.get("units", "metric")

    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
        "units": units,
        "lang": "zh_tw",
    }

    return _fetch_weather_data(params)


def clear_weather_cache():
    """清除所有天氣相關的快取，並記錄成功或失敗的日誌。回傳 True 表示成功，False 表示失敗。"""
    try:
        cache.delete_memoized(get_current_weather)
        cache.delete_memoized(get_weather_by_coords)
        current_app.logger.debug("已清除天氣快取")
        return True
    except Exception as e:
        current_app.logger.error(f"清除天氣快取失敗: {e}")
        return False


@cache.memoize(timeout=600)  # 快取 10 分鐘
def get_forecast(city):
    """
    取得指定城市的天氣預報
    :param city: 城市名稱
    :return: 成功回傳天氣預報資料字典，失敗回傳 None
    """
    api_key = current_app.config.get("OPENWEATHER_API_KEY")
    units = session.get("units", "metric")

    params = {"q": city, "appid": api_key, "units": units, "lang": "zh_tw"}
    base_url = "https://api.openweathermap.org/data/2.5/forecast"

    try:
        current_app.logger.debug(f"呼叫 OpenWeather Forecast API：{params}")
        response = requests.get(base_url, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"取得天氣預報失敗: {e}")
        return None


def format_forecast_data(data):
    """
    將 OpenWeatherMap 的預報資料轉換為前端易用的格式
    """
    if not data:
        return None

    daily_forecasts = defaultdict(list)

    for item in data.get("list", []):
        # item['dt'] 是 timestamp
        dt = datetime.fromtimestamp(item["dt"])
        date_str = dt.strftime("%Y-%m-%d")
        weekday = dt.strftime("%A")  # 星期幾的英文名稱

        # 將英文星期轉換為中文
        weekday_map = {
            "Monday": "(一)",
            "Tuesday": "(二)",
            "Wednesday": "(三)",
            "Thursday": "(四)",
            "Friday": "(五)",
            "Saturday": "(六)",
            "Sunday": "(日)",
        }
        weekday_zh = weekday_map.get(weekday, weekday)

        # 整理單筆資料
        forecast_item = {
            "time": dt.strftime("%H:%M"),
            "temp": round(item["main"]["temp"], 1),
            "description": item["weather"][0]["description"],
            "icon": item["weather"][0]["icon"],
            "pop": int(
                item.get("pop", 0) * 100
            ),  # 降雨機率 (Probability of Precipitation)
            "weekday": weekday_zh,  # 星期幾
        }

        daily_forecasts[date_str].append(forecast_item)

    return dict(daily_forecasts)


def get_forecast_by_coords(lat, lon):
    """
    根據經緯度取得天氣預報
    :param lat: 緯度
    :param lon: 經度
    :return: 成功回傳天氣預報資料字典，失敗回傳 None
    """
    api_key = current_app.config.get("OPENWEATHER_API_KEY")
    units = session.get("units", "metric")

    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
        "units": units,
        "lang": "zh_tw",
    }
    base_url = "https://api.openweathermap.org/data/2.5/forecast"
    try:
        current_app.logger.debug(f"呼叫 OpenWeather Forecast API：{params}")
        response = requests.get(base_url, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"取得天氣預報失敗: {e}")
        return None


def prepare_chart_data(forecast_data):
    """
    將預報資料整理為圖表所需格式
    :param forecast_data: 經過 format_forecast_data 處理的預報資料
    :return: 包含時間軸與溫度資料的字典
    """
    if not forecast_data:
        return None

    labels = []
    temps = []
    pops = []  # 降雨機率

    # 限制為未來 12 筆（3 小時間隔，共 36 小時）
    count = 0
    for date, items in forecast_data.items():
        for item in items:
            if count >= 12:
                break

            # 格式化標籤: "05 (一) 12:00" -> 日 + 中文星期 + 時間
            labels.append(f"{date[8:]} {item['weekday']} {item['time']}")
            temps.append(item["temp"])
            pops.append(item["pop"])
            count += 1

        # 若已達上限則跳出外層迴圈以避免不必要的迭代
        if count >= 12:
            break

    return {"labels": labels, "temps": temps, "pops": pops}


@cache.memoize(timeout=3600)
def get_air_pollution(lat, lon):
    """
    根據經緯度取得空氣污染資料
    :param lat: 緯度
    :param lon: 經度
    :return: 成功回傳空氣污染資料字典，失敗回傳 None
    """
    api_key = current_app.config.get("OPENWEATHER_API_KEY")
    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
    }
    base_url = "http://api.openweathermap.org/data/2.5/air_pollution"

    try:
        current_app.logger.debug(f"呼叫 OpenWeather Air Pollution API：{params}")
        response = requests.get(base_url, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"取得空氣污染資料失敗: {e}")
        return None
