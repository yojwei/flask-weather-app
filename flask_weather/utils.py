"""Utility functions for Flask Weather App"""


def format_temperature(celsius):
    """Convert Celsius to Fahrenheit"""
    return (celsius * 9 / 5) + 32


def get_weather_condition(condition_code):
    """Map weather condition code to description"""
    conditions = {
        "01d": "晴天",
        "02d": "多雲",
        "03d": "陰天",
        "04d": "陰天",
        "09d": "小雨",
        "10d": "下雨",
        "11d": "雷雨",
        "13d": "下雪",
    }
    return conditions.get(condition_code, "未知")
