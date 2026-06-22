# Replace the weather function
import tools
import importlib

# Redefine get_weather
def get_weather(city):
    import requests
    try:
        url = f"https://wttr.in/{city}?format=%C+%t+%w"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return f"Weather in {city}: {response.text.strip()}"
        else:
            return f"Weather error: Could not fetch data for {city}"
    except Exception as e:
        return f"Weather error: {e}"

# Replace the function in tools module
tools.get_weather = get_weather
print(" Weather function fixed!")
