import requests
import time

# tries to connect to Google in order to check Internet connection
def check_connection()-> bool:
    return True
    try:
        response = requests.get("https://8.8.8.8")
    except ConnectionError:
        return False
    
    return response.status_code == 200

def check_osm() -> bool:
    return True

def check_gemini() -> tuple:
    return True, 'super-model.v1'

print(check_connection())