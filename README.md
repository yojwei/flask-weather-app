# Flask Weather App

簡單的 Flask 範例：一個可在本機啟動的天氣應用程式骨架。

## 專案結構

```text
flask_weather/
├── flask_weather/          # 應用程式主程式碼 (Package)
│   ├── __init__.py         # 應用工廠函數 (create_app)
│   ├── config.py           # 配置管理
│   ├── utils.py            # 工具函數
│   ├── routes/             # 路由模組
│   │   └── __init__.py
│   ├── static/             # 靜態檔案 (CSS, JS, Images)
│   │   └── style.css
│   └── templates/          # Jinja2 模板
│       └── base.html
├── tests/                  # 測試程式碼
│   ├── __init__.py
│   └── test_app.py
├── app.py                  # 應用啟動入點
├── .env.example            # 環境變數範本
├── .gitignore              # Git 忽略清單
├── pyproject.toml          # 專案設定 (uv)
└── README.md
```

## 快速開始

### 安裝依賴

```bash
uv sync
```

### 環境設定

1. 複製 `.env.example` 為 `.env`
2. 編輯 `.env` 填入必要的環境變數

### 執行應用

```bash
python app.py
```

應用將在 `http://localhost:5000` 啟動

## 開發

### 執行測試

```bash
python -m pytest
```

### 專案依賴

- Flask >= 3.1.2
- python-dotenv >= 1.2.1
