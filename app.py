from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# Load environment variables
API_KEY = os.getenv("X_RAPIDAPI_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        location = request.form.get("location")
        date = request.form.get("date")
        
        # Call weather forecast API
        forecast_data = fetch_weather_forecast(location, date)
        
        return render_template("index.html", forecast_data=forecast_data)
    
    return render_template("index.html")

def fetch_weather_forecast(location, date):
    # Make API request to fetch weather forecast data
    url = "https://api.weather.com/forecast"
    params = {
        "apiKey": API_KEY,
        "location": location,
        "date": date
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

if __name__ == "__main__":
    app.run(debug=True)
