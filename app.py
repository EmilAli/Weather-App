from flask import Flask, render_template, request
import requests
import datetime

app = Flask(__name__)

api_key = "a4362eb5d4fc4c553ed864c2f8842b75"

# Mapping weather descriptions to background images
weather_backgrounds = {
    "clear sky": "clear-sky.png",
    "few clouds": "few-clouds.png",
    "scattered clouds": "scattered-clouds.png",
    "broken clouds": "broken-clouds.png",
    "shower rain": "shower-rain.png",
    "rain": "rain.png",
    "thunderstorm": "thunderstorm.png",
    "snow": "snow.png",
    "mist": "mist.png"
}

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    error = None
    background_image = "default.png"  # Default background image

    if request.method == 'POST':
        city_request = request.form['city']
        results = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city_request}&units=metric&appid={api_key}")
        
        if results.json()["cod"] == "404":
            error = f"I'm afraid we do not have weather information for {city_request}."
        else:
            description = results.json()["weather"][0]["description"]
            temperature = round(results.json()["main"]["temp"])
            humidity = results.json()["main"]["humidity"]
            wind_speed = round(results.json()["wind"]["speed"])
            weather_data = {
                'city': city_request.capitalize(),
                'description': description,
                'temperature': temperature,
                'humidity': humidity,
                'wind_speed': wind_speed
            }
            background_image = weather_backgrounds.get(description, "default.png")

    current_time = datetime.datetime.now()
    hour = current_time.hour
    if 4 <= hour < 7:
        greeting = "Good morning early riser,"
    elif 7 <= hour < 12:
        greeting = "Good morning,"
    elif 12 <= hour < 18:
        greeting = "Good afternoon,"
    elif 18 <= hour < 23:
        greeting = "Good evening"
    else:
        greeting = "Good evening night owl,"

    return render_template('index.html', greeting=greeting, weather_data=weather_data, error=error, background_image=background_image)

if __name__ == '__main__':
    app.run()
