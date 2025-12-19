"""Flask Weather App Entry Point"""

from flask_weather import create_app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
