import serpapi, os, json

params = {
    "api_key": "674ca958dc3c7c4afccacee096d4cb026e12ab6e882dda693516d975987d71f5",  # your serpapi api
    "engine": "google_maps",  # SerpApi search engine
    "q": "Restaurant",
    "ll": "@-33.8651304,151.1939402,15z",
}

results = serpapi.Client().search(params)["local_results"]

print(results)
