
import requests

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


def get_city():
    while True:
        city = input("Enter city name (or 'exit' to quit): ").strip()

        if city.lower() == "exit":
            print("Thank you for using Weather Data CLI!")
            raise SystemExit

        if not city or not any(c.isalpha() for c in city):
            print("Please enter a valid city name.\n")
            continue

        return city


def fetch_weather(city):
    try:
        location_response = requests.get(
            GEOCODING_URL,
            params={"name": city, "count": 1, "language": "en"},
            timeout=10,
        )
        location_response.raise_for_status()
        locations = location_response.json().get("results", [])

        if not locations:
            print(f"City '{city}' was not found.")
            return None

        location = locations[0]

        weather_response = requests.get(
            WEATHER_URL,
            params={
                "latitude": location["latitude"],
                "longitude": location["longitude"],
                "current": (
                    "temperature_2m,relative_humidity_2m,"
                    "apparent_temperature,is_day,precipitation,"
                    "weather_code,wind_speed_10m"
                ),
                "timezone": "auto",
            },
            timeout=10,
        )
        weather_response.raise_for_status()

        return location, weather_response.json()

    except requests.exceptions.Timeout:
        print("Error: Request timed out. Try again.")
    except requests.exceptions.ConnectionError:
        print("Error: Check your internet connection.")
    except requests.exceptions.HTTPError as error:
        print(f"Weather API error: {error}")
    except requests.exceptions.RequestException as error:
        print(f"Request failed: {error}")
    except (ValueError, KeyError, IndexError) as error:
        print(f"Invalid weather response: {error}")

    return None


def describe_weather(code):
    descriptions = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snowfall",
        73: "Moderate snowfall",
        75: "Heavy snowfall",
        80: "Rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        95: "Thunderstorm",
        96: "Thunderstorm with hail",
        99: "Thunderstorm with heavy hail",
    }
    return descriptions.get(code, "Other weather conditions")


def display_weather(result):
    if result is None:
        return

    location, data = result
    current = data.get("current", {})

    print("\n" + "=" * 44)
    print("             CURRENT WEATHER")
    print("=" * 44)
    print(
        f"Location      : {location['name']}, "
        f"{location.get('country', '')}"
    )
    print(f"Temperature   : {current.get('temperature_2m')} °C")
    print(f"Feels like    : {current.get('apparent_temperature')} °C")
    print(f"Humidity      : {current.get('relative_humidity_2m')}%")
    print(f"Condition     : {describe_weather(current.get('weather_code'))}")
    print(f"Wind speed    : {current.get('wind_speed_10m')} km/h")
    print(f"Precipitation : {current.get('precipitation')} mm")
    print(f"Local time    : {current.get('time', 'Unavailable')}")
    print("=" * 44)


def main():
    print("\n" + "=" * 44)
    print("          WEATHER DATA CLI")
    print("=" * 44)
    print("Real-time weather data using Open-Meteo.\n")

    while True:
        city = get_city()
        result = fetch_weather(city)
        display_weather(result)
        print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nApplication stopped by user.")
