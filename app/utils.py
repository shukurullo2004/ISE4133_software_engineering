import requests
import time
import urllib.parse
import json
import time
import datetime

import config

# API configuration
gemini_api_url = "https://generativelanguage.googleapis.com/v1beta"
gemini_api_key =  config.GEMINI_API_KEY

# OpenStreetMap APIs (for geocoding and directions) - free alternatives
nominatim_url = "https://nominatim.openstreetmap.org/search"
osrm_url = "http://router.project-osrm.org/route/v1"

openweather_api_key = config.OPENWEATHER_API_KEY

# tries to connect to Google in order to check Internet connection
def check_connection()-> bool:
    # return True
    try:
        response = requests.get("https://8.8.8.8")
    except ConnectionError:
        config.logger.error("No internet connecton")
        return False
    config.logger.info("Internet connection succesfull")
    return response.status_code == 200

def check_osm() -> bool:
    try:
        response = requests.get(nominatim_url)
    except ConnectionError:
        config.logger.error("No internet connecton")
        return False
    if response.status_code == 200:
        config.logger.info("Internet connection succesfull")
        return True
    return False

def check_gemini() -> tuple:
    available_models = list_available_gemini_models(gemini_api_key)
    # Try to find a suitable model
    preferred_models = ["gemini-pro", "gemini-1.0-pro", "gemini-1.5-pro", "text-bison", "gemini-1.5-flash"]
    selected_model = None
    
    for preferred in preferred_models:
        if preferred in available_models:
            selected_model = preferred
            break
            
    if not selected_model and available_models:
        # Use the first available model if none of the preferred ones are available
        selected_model = available_models[0]
    
    if selected_model:
        return True, selected_model
    return False

def check_addr(location, key=None) -> tuple:
    data = geocoding(location, key)
    if (data[0] == 200) and (data[1] != "null"):
        return True, data
    else: return False, {}

def get_things_done(args):
    originWeather = ''
    destWeather = ''
    directions = ''
    route = ''
    geminiTips = ''

    if args['origin-addr'] and args['dest-addr']:
        # Get weather info
        originWeather = display_weather_info(args['origin-addr'][1], args['origin-addr'][2], openweather_api_key)
        destWeather = display_weather_info(args['dest-addr'][1], args['dest-addr'][2], openweather_api_key)
        
        config.logger.info("Wether info gathered")
        
        # Get directions get_directions(origin_lat, origin_lng, dest_lat, dest_lng, mode, key=None)
        directions = get_directions(args['origin-addr'][1], args['origin-addr'][2], 
                                    args['dest-addr'][1], args['dest-addr'][2], 
                                    mode=args['transport'])[1]
        
        config.logger.info("Direction info gathered")
        
        route = display_directions(directions, args['origin-addr'][3], args['dest-addr'][3], args['transport'])
      
        config.logger.info("Routes info gathered")

        if args['gemini'] != '':
            geminiTips = enhance_directions_with_gemini(args['origin-addr'], args['dest-addr'], 
                                                        args['transport'], 
                                                        directions, gemini_api_key, args['gemini'])
        
            config.logger.info("Gemini Tips are gathered")
        else:
            geminiTips = "No AI tips available."

        return {'weather-orig': originWeather, 
                'weather-dest': destWeather, 
                'route': route, 
                'gemini-tips': geminiTips}

# Below are the functions that dbasically are basicallay slightly modified slicees of the main.py
def geocoding(location, key=None):
    """
    Get geocoding information for a location using OpenStreetMap Nominatim API
    
    Args:
        location (str): The location to geocode
        key (str): Not needed for Nominatim
        
    Returns:
        tuple: (status_code, lat, lng, formatted_address)
    """
    # Don't send empty location
    # while location == "":
    #     location = input("Enter the location again: ")
        
    # Construct the URL - no API key required for Nominatim
    url = nominatim_url + "?" + urllib.parse.urlencode({
        "q": location,
        "format": "json",
        "limit": 1
    })
    
    # Add a user agent header as required by Nominatim
    headers = {
        "User-Agent": "DirectionsApp/1.0"
    }
    
    try:
        # Be polite and respect rate limits (max 1 request per second)
        time.sleep(1) 
        
        
        # Send the request to Nominatim
        response = requests.get(url, headers=headers)
        json_status = response.status_code
        
        # Check if the request was successful and results are not empty
        if json_status == 200:
            json_data = response.json()
            
            if len(json_data) > 0:
                # Extract latitude, longitude, and formatted address
                lat = float(json_data[0]["lat"])
                lng = float(json_data[0]["lon"])
                formatted_address = json_data[0]["display_name"]
                
                if "type" in json_data[0]:
                    location_type = json_data[0]["type"]
                else:
                    location_type = "place"
                
                config.logger.info(f"Geocoding API URL for {formatted_address} (Location Type: {location_type})")
                config.logger.info(url)
                
                return json_status, lat, lng, formatted_address
            else:
                config.logger.info(f"Geocoding API URL for {location} returned no results")
                config.logger.info(url)
                return json_status, "null", "null", location
        else:
            # Handle errors
            config.logger.info(f"Geocode API status: {json_status}\nError with request")
            return json_status, "null", "null", location
            
    except Exception as e:
        config.logger.error(f"An error occurred: {str(e)}")
        return 500, "null", "null", location

def list_available_gemini_models(key):
    """
    List all available Gemini models for the given API key
    
    Args:
        key (str): API key for Gemini
        
    Returns:
        list: List of available model names
    """
    url = f"{gemini_api_url}/models"
    headers = {
        "x-goog-api-key": key
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            models_data = response.json()
            available_models = []
            if "models" in models_data:
                for model in models_data["models"]:
                    if "name" in model:
                        model_name = model["name"].split("/")[-1]  # Extract just the model name
                        # Check if model supports generateContent
                        if "supportedGenerationMethods" in model and "generateContent" in model["supportedGenerationMethods"]:
                            available_models.append(model_name)
            return available_models
        else:
            config.logger.error(f"Error listing models: {response.status_code}")
            try:
                error_data = response.json()
                config.logger.error(f"Error details: {json.dumps(error_data, indent=2)}")
            except:
                pass
            return []
    except Exception as e:
        config.logger.error(f"Exception listing models: {str(e)}")
        return []
    
import requests
import datetime
import pytz

def display_weather_info(lat, lng, key) -> str:
   
    
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

            return f"""
# 📍 Weather Report for **{city_name}**

### 🌤 Weather
- **Description:** {description}
- **Temperature:** {temp}°C _(Feels like {feels_like}°C)_
- **Humidity:** {humidity}%
- **Pressure:** {pressure} hPa  
- **Sea Level:** {sea_level} hPa  
- **Ground Level:** {grnd_level} hPa  

### 💨 Wind
- **Speed:** {wind_speed} m/s  
- **Direction:** {wind_deg}°

### 🌅 Sun Times
- **Sunrise:** {sunrise_time.strftime('%H:%M:%S')}
- **Sunset:** {sunset_time.strftime('%H:%M:%S')}
"""

        else:
            config.logger.error(f"Error: Unable to fetch weather data. Status code: {response.status_code}")
            return ""
    except Exception as e:
        config.logger.error(f"⚠️ An error occurred: {e}")
        return ""

def get_directions(origin_lat, origin_lng, dest_lat, dest_lng, mode, key=None):
    """
    Get directions between two points using OpenStreetMap OSRM API
    
    Args:
        origin_lat (float): Latitude of origin
        origin_lng (float): Longitude of origin
        dest_lat (float): Latitude of destination
        dest_lng (float): Longitude of destination
        mode (str): Mode of transportation (driving, walking, bicycling)
        key (str): Not needed for OSRM
        
    Returns:
        tuple: (status_code, directions_data)
    """
    # Convert transportation mode to OSRM profile
    if mode.lower() == "driving" or mode.lower() == "car":
        osrm_profile = "car"
    elif mode.lower() == "walking" or mode.lower() == "foot":
        osrm_profile = "foot"
    elif mode.lower() == "bicycling" or mode.lower() == "bike":
        osrm_profile = "bike"
    else:
        # Default to car if mode not recognized
        osrm_profile = "car"
    
    # Construct the URL
    url = f"{osrm_url}/{osrm_profile}/{origin_lng},{origin_lat};{dest_lng},{dest_lat}?overview=full&steps=true&annotations=true"
    
    try:
        # Be polite and respect rate limits
        time.sleep(1)
        
        # Send the request to OSRM
        response = requests.get(url)
        json_status = response.status_code
        
        print(f"Routing API Status: {json_status}")
        print(f"Routing API URL:\n{url}")
        
        if json_status == 200:
            json_data = response.json()
            return json_status, json_data
        else:
            return json_status, {"code": "Error", "message": f"Status code: {json_status}"}
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return 500, {"code": "Error", "message": str(e)}

def display_directions(directions_data, origin, destination, mode, enhanced_info=None) -> str:
    """
    Prepare formatted directions from OSRM data.
    
    Args:
        directions_data (dict): Directions data from OSRM
        origin (str): Origin location
        destination (str): Destination location
        mode (str): Mode of transportation
        enhanced_info (str): Optional enhanced explanation
    
    Returns:
        str: Formatted step-by-step direction summary
    """

    if directions_data.get("code") != "Ok" or "routes" not in directions_data or not directions_data["routes"]:
        config.logger.error(f"Failed to get directions from {origin} to {destination}: {directions_data.get('code')}")
        if "message" in directions_data:
            config.logger.error(f"Message: {directions_data['message']}")
        return f"❌ Error retrieving directions: {directions_data.get('code', 'Unknown error')}\n" \
               f"{directions_data.get('message', '')}"
    # get
    route = directions_data["routes"][0]

    distance_meters = route["distance"]
    km = distance_meters / 1000
    miles = km / 1.61

    duration_seconds = route["duration"]
    hr = int(duration_seconds / 3600)
    min = int((duration_seconds % 3600) / 60)

    summary = (
        f"📍 **Directions from {origin} to {destination} by {mode}**\n"
        f"📏 Distance: **{km:.1f} km** / **{miles:.1f} miles**\n"
        f"⏱ Duration: **{hr}h {min}m**\n"
    )

    config.logger.info(f"Directions loaded: {km:.1f} km, {hr}h {min}m")

    directions = []

    legs = route.get("legs", [])
    if legs and "steps" in legs[0]:
        for i, step in enumerate(legs[0]["steps"], 1):
            maneuver = step.get("maneuver", {})
            type_ = maneuver.get("type", "").capitalize()
            modifier = maneuver.get("modifier", "")
            name = step.get("name", "")

            direction = f"{type_} {modifier}".strip()
            if name:
                direction += f" onto **{name}**"

            if not direction.strip():
                direction = "Continue straight"

            step_km = step["distance"] / 1000
            step_mi = step_km / 1.61

            directions.append(f"{i}. {direction} ({step_km:.1f} km / {step_mi:.1f} miles)")

    else:
        directions.append(f"Follow the route for {km:.1f} km / {miles:.1f} miles.")
        directions.append("Arrive at your destination.")

    return summary + "\n" + "\n".join(directions)

# I changed the prompt to AI to make it better
def enhance_directions_with_gemini(origin, destination, mode, directions_data, key, model=None) -> str:
    """
    Enhance directions with travel tips and local insights via Gemini API.

    Args:
        origin (str): Origin location
        destination (str): Destination location
        mode (str): Mode of transportation
        directions_data (dict): OSRM directions
        key (str): Gemini API key
        model (str, optional): Specific Gemini model to use

    Returns:
        str: Enhanced travel guidance, or error message
    """
    if directions_data.get("code") != "Ok" or not directions_data.get("routes"):
        config.logger.warning("Invalid or missing directions data.")
        return "⚠️ Unable to enhance directions due to missing or invalid data."

    route = directions_data["routes"][0]

    # Prepare distance and duration
    distance_km = route["distance"] / 1000
    distance_mi = distance_km / 1.61
    duration_sec = route["duration"]
    duration_str = str(datetime.timedelta(seconds=int(duration_sec)))

    # Prompt
    prompt = (
        f"""You are enhancing a directions app for end users.

They are traveling from {origin} to {destination} by {mode}.  
The total route is approximately {distance_km:.1f} km ({distance_mi:.1f} miles) and will take about {duration_str}.

Your response will be shown in a user interface using Markdown formatting. Please provide:

1. Notable landmarks or points of interest along the way (if any)
2. One or two interesting historical or cultural facts about {origin} and {destination}
3. Travel tips or cautions specific to the journey (if relevant)

Be concise, informative, and user-friendly. Use Markdown headings or bullet points where appropriate. Avoid generic or filler text.
"""
    )

    url = f"{gemini_api_url}/models/{model}:generateContent"
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": key
    }

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 1024
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        config.logger.info(f"Gemini API response status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            candidates = data.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts:
                    return parts[0].get("text", "⚠️ Gemini returned empty response.")
            config.logger.warning("Empty response parts from Gemini.")
            return "⚠️ Gemini returned no enhancement content."

        # If not 200, try to get detailed error
        try:
            error_data = response.json()
            message = error_data.get("error", {}).get("message", "Unknown error")
            config.logger.error(f"Gemini API error: {message}")
            return f"❌ Gemini Error: {message}"
        except Exception as parse_err:
            config.logger.exception("Failed to parse Gemini error response.")
            return f"❌ Gemini Error: {response.status_code}"

    except Exception as e:
        config.logger.exception("Exception while calling Gemini API")
        return f"❌ Error communicating with Gemini: {str(e)}"
    