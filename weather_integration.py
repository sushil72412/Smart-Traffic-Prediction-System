import requests
import pandas as pd

# API Configuration
API_KEY = "67b45447151fec1bbf362f93dc621c80"

city = "Delhi"

# API URL
url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

# Fetch Data
response = requests.get(url)

data = response.json()

# Weather Mapping
weather_map = {
    'Clear': 0,
    'Clouds': 1,
    'Rain': 2,
    'Haze': 3,
    'Mist': 4,
    'Fog': 5
}

# Check API Success
if response.status_code == 200:

    temperature = data['main']['temp']

    humidity = data['main']['humidity']

    weather = data['weather'][0]['main']

    weather_value = weather_map.get(weather, 0)

    print("Temperature:", temperature)

    print("Humidity:", humidity)

    print("Weather:", weather)

    print("Weather Encoded:", weather_value)

    # Create ML Input Sample
    sample = pd.DataFrame({

        'hour': [18],

        'day': [15],

        'month': [5],

        'year': [2017],

        'Junction': [1],

        'temperature': [temperature],

        'humidity': [humidity],

        'weather_condition': [weather_value]

    })

    print("\nAI Input Sample:")

    print(sample)

else:

    print("API Error:", data)