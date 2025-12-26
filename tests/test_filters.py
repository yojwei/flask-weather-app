def test_datetimeformat_filter(app):
    """測試 datetimeformat 模板過濾器"""
    timestamp = 1704067200  # 2024-01-01 00:00:00 UTC (approx)

    # 獲取過濾器函數
    datetimeformat = app.jinja_env.filters["datetimeformat"]

    # 驗證默認格式
    from datetime import datetime

    expected = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
    assert datetimeformat(timestamp) == expected

    # 驗證自定義格式
    custom_format = "%Y/%m/%d"
    expected_custom = datetime.fromtimestamp(timestamp).strftime(custom_format)
    assert datetimeformat(timestamp, custom_format) == expected_custom
