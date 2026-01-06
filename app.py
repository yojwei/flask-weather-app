"""Flask Weather App Entry Point"""

import os
from dotenv import load_dotenv
from flask_weather import create_app

load_dotenv()

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=int(os.getenv("PORT", "5000")), host="0.0.0.0")
