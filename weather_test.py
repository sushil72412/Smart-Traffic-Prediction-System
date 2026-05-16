import requests

API_KEY = "67b45447151fec1bbf362f93dc621c80"

city = "Delhi"

url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

response = requests.get(url)

data = response.json()

# Check API success
if response.status_code == 200:

    temperature = data['main']['temp']

    humidity = data['main']['humidity']

    weather = data['weather'][0]['main']

    print("Temperature:", temperature)

    print("Humidity:", humidity)

    print("Weather:", weather)

else:

    print("API Error:", data)