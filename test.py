from data.clients.openweather_client import fetch_current_weather
from data.loaders.cities_loader import load_active_cities
from data.storage.raw_saver import save_raw_payload

sample = {"test": 123}
path = save_raw_payload("ljubljana", sample)
print(path)


# cities = load_active_cities("data/metadata/cities.csv")
# print(cities)

# data = fetch_current_weather(46.0569, 14.5058)
# print(data)