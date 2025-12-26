def test_index(client):
    """測試主頁路由"""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Flask \xe5\xa4\xa9\xe6\xb0\xa3\xe6\x87\x89\xe7\x94\xa8" in response.data


def test_weather_api(client):
    """測試天氣 API 端點"""
    response = client.get("/api/weather")
    assert response.status_code == 200
    assert response.json == {"status": "ok", "message": "天氣 API 端點"}
