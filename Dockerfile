# 使用官方 Python 輕量版映像檔
FROM python:3.11-slim

# 設定工作目錄
WORKDIR /app

# 設定環境變數
# PYTHONDONTWRITEBYTECODE: 防止 Python 產生 .pyc 檔案
# PYTHONUNBUFFERED: 確保 log 即時輸出
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 安裝系統依賴 (如果需要編譯某些 Python 套件)
# RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# 複製依賴清單並安裝
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn  # 生產環境 Server

# 複製專案程式碼
COPY . .

# 暴露 Port
EXPOSE 5000

# 啟動指令
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "flask_weather:create_app()"]