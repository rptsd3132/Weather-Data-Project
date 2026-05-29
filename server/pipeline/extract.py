import os
import requests
from dotenv import load_dotenv

# Load secrets from the .env file
load_dotenv()

# Read the API key from .env
API_KEY = os.getenv("WEATHER_API_KEY")

# The base web address of the weather API
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def extract_weather(city):
    """Fetch raw weather data for one city from the API."""
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()  # stop if the request failed
    return response.json()       # return the data as a Python dictionary


# This block runs only when we run this file directly (for testing)
if __name__ == "__main__":
    data = extract_weather("London")
    print(data)
    