# Enhanced Directions App

A command-line application that provides enhanced directions using free mapping APIs and Google's Gemini AI.

## 🌟 Features

- **Free Mapping Services**: Uses OpenStreetMap's Nominatim for geocoding and OSRM for routing
- **AI-Enhanced Directions**: Leverages Google's Gemini AI to provide additional information about your journey
- **Multiple Transportation Modes**: Support for car, bike, and walking directions
- **Detailed Turn-by-Turn Guidance**: Step-by-step directions with distance information
- **Cross-platform**: Works on any system with Python 3.6+

## 📋 Prerequisites

- Python 3.6 or higher
- Internet connection
- Google Gemini API key (for AI-enhanced directions)

## 🔧 Installation

1. Clone this repository:
   ```
   git clone ...
   cd ...
   ```

2. Install the required dependencies:
   ```
   pip install requests
   ```

3. Set up your API key:
   - Get a Google Gemini API key from https://makersuite.google.com/app/apikey
   - Replace the placeholder API key in the code with your own key

## 🚀 Usage

Run the application:
```
python directions_app.py
```

Follow the prompts to:
1. Choose a transportation mode (car, bike, foot)
2. Enter your starting location
3. Enter your destination
4. Review the directions and AI-enhanced information

To exit the application, type `q` or `quit` at any prompt.

## 📝 Example

```
===================================================
Welcome to the Enhanced Directions App!
This app uses OpenStreetMap for directions and
Google's Gemini AI to provide additional information.
===================================================

+++++++++++++++++++++++++++++++++++++++++++++
Transportation modes available:
+++++++++++++++++++++++++++++++++++++++++++++
car, bike, foot, driving, bicycling, walking
Note: 'driving' and 'bicycling' are Google Maps terms.
They will be converted to 'car' and 'bike' respectively.
To quit the program, type 'q' at any prompt.
+++++++++++++++++++++++++++++++++++++++++++++

Enter a transportation mode from the list above: car
Starting Location: New York

📍 Weather Report for New York

🌤 Weather: Clear sky
🌡 Temperature: 14.49°C (Feels like 13.22°C)
💧 Humidity: 47%
📈 Pressure: 1023 hPa
🌊 Sea Level: 1023 hPa
🏔 Ground Level: 1023 hPa

💨 Wind Speed: 3.09 m/s
🧭 Wind Direction: 190°

🌅 Sunrise: 18:56:49
🌇 Sunset: 08:49:38


Destination: Boston

📍 Weather Report for Boston

🌤 Weather: Broken clouds
🌡 Temperature: 11.75°C (Feels like 10.52°C)
💧 Humidity: 59%
📈 Pressure: 1023 hPa
🌊 Sea Level: 1023 hPa
🏔 Ground Level: 1019 hPa

💨 Wind Speed: 1.34 m/s
🧭 Wind Direction: 233°

🌅 Sunrise: 18:41:44
🌇 Sunset: 08:41:06

=================================================
Directions from New York to Boston by car
=================================================
Distance Traveled: 215.7 miles / 347.1 km
Trip Duration: 03:42:15
=================================================
1. Depart onto I-95 N (5.2 km / 3.2 miles)
2. Continue onto I-278 E (6.8 km / 4.2 miles)
...

Additional Information from Gemini AI:
=================================================
Here's some information to enhance your journey from New York to Boston by car:

Landmarks along the route:
- Yale University in New Haven, Connecticut
- Mystic Seaport, a maritime museum in Mystic, Connecticut
- Providence, Rhode Island (capital city)
- The Big Dig tunnels as you enter Boston

Historical facts:
New York:
- Originally called New Amsterdam when founded by Dutch settlers in 1624
- Became the first capital of the United States in 1789

Boston:
- Founded in 1630, making it one of America's oldest cities
- Site of the Boston Tea Party (1773) and the start of the American Revolution
- Home to the first public park (Boston Common, 1634) and public school (Boston Latin, 1635)

Travel tips:
- The I-95 corridor can get congested, especially during rush hours (7-9am, 4-7pm)
- Consider a rest stop in Mystic, CT or Providence, RI to break up the journey
- Watch for tolls along the route - have cash or electronic payment ready
- For the best skyline view of Boston, approach via the Tobin Bridge if possible
=================================================
```

## 🗺️ API Information

This application uses:

1. **OpenStreetMap Nominatim API**
   - For geocoding (converting addresses to coordinates)
   - Free to use with appropriate rate limiting
   - Documentation: https://nominatim.org/release-docs/latest/

2. **OSRM (Open Source Routing Machine)**
   - For calculating routes and directions
   - Free to use with appropriate rate limiting
   - Documentation: http://project-osrm.org/docs/

3. **Google Gemini API**
   - For AI-generated information about the journey
   - Requires an API key
   - Documentation: https://ai.google.dev/docs

4. **OpenWeather API**  
   - For providing real-time weather conditions along the route  
   - Useful for travel planning and safety alerts  
   - Requires a free API key from [OpenWeather](https://openweathermap.org/api)  
   - [Documentation](https://openweathermap.org/current)

## ⚠️ Limitations

- OSRM may not be able to calculate routes between very distant locations or across water bodies
- The quality of AI-enhanced information depends on the Gemini API's knowledge about the locations
- API rate limits may apply (the code implements proper delays to avoid hitting these limits)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenStreetMap contributors for the free mapping data
- OSRM team for the routing engine
- Google for the Gemini AI API
