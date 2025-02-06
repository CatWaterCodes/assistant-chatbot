import requests
WEATHER_API_KEY = "0949fe0c12ab9a7e26846909e8514891"

def weather_at_location(latitude, longitude):
    return requests.get(f"https://api.openweathermap.org/data/2.5/weather?&lat={ latitude }&lon={ longitude }&units=imperial&appid={ WEATHER_API_KEY }").json() 

definitions = [{
    "type": "function",
    "function": {
        "name": "weather_at_location",
        "description": "Returns the weather at the location of the given longitude and latitude",
        "parameters": {
            "type": "object",
            "properties": {
                "longitude": {
                    "type": "string",
                    "description": "The longitude of the palce",
                },
                "latitude": {
                    "type": "string",
                    "description": "The latitude of the palce",
                },
            },
            "required": ["longitude", "latitude"],
        },
    },
}]