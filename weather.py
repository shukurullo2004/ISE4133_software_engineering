import requests
import datetime
import pytz
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def display_weather_info(lat, lng, key):
    """
    Fetches and prints the current weather beautifully for the given latitude and longitude using OpenWeatherMap API.
    
    Args:
        lat (float): Latitude of the location.
        lng (float): Longitude of the location.
        key (str): OpenWeatherMap API key.
    """
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={key}&units=metric"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()

            # Basic Weather Information
            city_name = weather_data["name"]
            description = weather_data["weather"][0]["description"].capitalize()
            temp = weather_data["main"]["temp"]
            feels_like = weather_data["main"]["feels_like"]
            humidity = weather_data["main"]["humidity"]
            pressure = weather_data["main"]["pressure"]
            wind_speed = weather_data["wind"]["speed"]
            wind_deg = weather_data["wind"]["deg"]
            sea_level = weather_data["main"].get("sea_level", "N/A")
            grnd_level = weather_data["main"].get("grnd_level", "N/A")

            # Sunrise and Sunset
            sunrise_ts = weather_data["sys"]["sunrise"]
            sunset_ts = weather_data["sys"]["sunset"]
            local_timezone = pytz.timezone('Asia/Seoul')  # Change this if needed

            sunrise_time = datetime.datetime.utcfromtimestamp(sunrise_ts).replace(tzinfo=pytz.utc).astimezone(local_timezone)
            sunset_time = datetime.datetime.utcfromtimestamp(sunset_ts).replace(tzinfo=pytz.utc).astimezone(local_timezone)

            # Display Weather
            print(Fore.GREEN + Style.BRIGHT + f"\n📍 Weather Report for {city_name}\n" + Style.RESET_ALL)
            print(Fore.GREEN + f"🌤 Weather: {description}")
            print(Fore.GREEN + f"🌡 Temperature: {temp}°C (Feels like {feels_like}°C)")
            print(Fore.GREEN + f"💧 Humidity: {humidity}%")
            print(Fore.GREEN + f"📈 Pressure: {pressure} hPa")
            print(Fore.GREEN + f"🌊 Sea Level: {sea_level} hPa")
            print(Fore.GREEN + f"🏔 Ground Level: {grnd_level} hPa\n")

            print(Fore.RED + f"💨 Wind Speed: {wind_speed} m/s")
            print(Fore.RED + f"🧭 Wind Direction: {wind_deg}°\n")

            print(Fore.GREEN + f"🌅 Sunrise: {sunrise_time.strftime('%H:%M:%S')}")
            print(Fore.RED + f"🌇 Sunset: {sunset_time.strftime('%H:%M:%S')}\n")

        else:
            print(Fore.RED + f"❌ Error: Unable to fetch weather data. Status code: {response.status_code}")
    except Exception as e:
        print(Fore.RED + f"⚠️ An error occurred: {e}")
