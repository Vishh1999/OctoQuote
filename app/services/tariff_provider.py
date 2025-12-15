import json

TARIFF_PATH = "app/data/tariff_config.json"

def load_tariffs_from_config():
    with open(TARIFF_PATH) as f:
        return json.load(f)
