import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENWEATHER_API_KEY")
city = "Taipei"
url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=zh_tw"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print(f"城市: {data['name']}")
    print(f"天氣: {data['weather'][0]['description']}")
    print(f"溫度: {data['main']['temp']}°C")
else:
    print(f"錯誤: {response.status_code}")
