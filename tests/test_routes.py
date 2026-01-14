from unittest.mock import patch


def test_index_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Weather App" in response.data  # 檢查頁面內容是否包含標題


def test_login_logout(client, app):
    # 測試登入成功（使用 conftest 中已建立的使用者）
    response = client.post(
        "/auth/login",
        data={"username": "testuser", "password": "password123"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Hi, testuser" in response.data  # 確認導航列顯示使用者名稱

    # 測試登出
    response = client.get("/auth/logout", follow_redirects=True)
    assert response.status_code == 200
    assert b"Hi, testuser" not in response.data


def test_weather_search(client):
    # 模擬的 API 回傳資料
    mock_weather_data = {
        "coord": {"lon": 120.6839, "lat": 24.1469},
        "weather": [
            {"id": 801, "main": "Clouds", "description": "few clouds", "icon": "02d"}
        ],
        "base": "stations",
        "main": {
            "temp": 22.84,
            "feels_like": 22.17,
            "temp_min": 22.84,
            "temp_max": 24.7,
            "pressure": 1019,
            "humidity": 38,
            "sea_level": 1019,
            "grnd_level": 1000,
        },
        "visibility": 10000,
        "wind": {"speed": 2.57, "deg": 270},
        "clouds": {"all": 20},
        "dt": 1768361391,
        "sys": {
            "type": 2,
            "id": 86663,
            "country": "TW",
            "sunrise": 1768344142,
            "sunset": 1768382967,
        },
        "timezone": 28800,
        "id": 1668399,
        "name": "Taichung",
        "cod": 200,
    }

    mock_forecast_data = {
        "cod": "200",
        "list": [
            {
                "dt": 1768361391,
                "main": {
                    "temp": 23.5,
                    "feels_like": 22.8,
                    "temp_min": 22.0,
                    "temp_max": 25.0,
                    "pressure": 1020,
                    "humidity": 40,
                },
                "weather": [
                    {
                        "id": 801,
                        "main": "Clouds",
                        "description": "few clouds",
                        "icon": "02d",
                    }
                ],
                "wind": {"speed": 2.5, "deg": 270},
            }
        ],
    }

    mock_pollution_data = {
        "coord": {"lon": 120.6839, "lat": 24.1469},
        "list": [
            {
                "main": {"aqi": 2},
                "components": {
                    "pm2_5": 15.5,
                    "pm10": 20.0,
                    "no2": 10.0,
                    "o3": 50.0,
                },
                "dt": 1768361391,
            }
        ],
    }

    # 使用 patch 替換 utils 中的函數
    with patch(
        "flask_weather.weather.routes.get_current_weather"
    ) as mock_weather, patch(
        "flask_weather.weather.routes.get_forecast"
    ) as mock_forecast, patch(
        "flask_weather.weather.routes.get_air_pollution"
    ) as mock_pollution:

        # 設定 mock 物件的回傳值
        mock_weather.return_value = mock_weather_data
        mock_forecast.return_value = mock_forecast_data
        mock_pollution.return_value = mock_pollution_data

        # 發送搜尋請求
        response = client.post(
            "/weather/search", data={"city": "Taichung"}, follow_redirects=True
        )

        assert response.status_code == 200
        assert b"Taichung" in response.data
        assert b"22.8" in response.data  # 溫度會被 round 到 1 位小數
