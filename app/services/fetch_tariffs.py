import requests
import json

# ---------- CONFIG ----------
BASE_URL = "https://api.octopus.energy/v1"
OUTPUT_PATH = "app/data/tariff_config.json"
# ----------------------------

def fetch_electricity_tariffs(product_code, REGION_CODE):
    url = (
        f"{BASE_URL}/products/{product_code}/"
        f"electricity-tariffs/E-1R-{product_code}-{REGION_CODE}/standard-unit-rates/"
    )
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        return None
    return response.json()["results"]


def fetch_standing_charges(product_code, REGION_CODE):
    url = (
        f"{BASE_URL}/products/{product_code}/"
        f"electricity-tariffs/E-1R-{product_code}-{REGION_CODE}/standing-charges/"
    )
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        return None
    return response.json()["results"]


def normalize_tariff(product, unit_rates, standing_charges):
    if not unit_rates or not standing_charges:
        return None

    latest_unit_rate = unit_rates[0]
    latest_standing_charge = standing_charges[0]

    return {
        "tariff_code": product["code"],
        "name": product["display_name"],
        "fuel": "ELECTRICITY",
        "pricing": {
            "unit_rate_pence_per_kwh": round(
                latest_unit_rate["value_inc_vat"] * 100, 2
            ),
            "standing_charge_pence_per_day": round(
                latest_standing_charge["value_inc_vat"] * 100, 2
            ),
        },
        "meter_requirements": {
            "smart_meter_required": "SMART" in product["display_name"].upper()
        },
        "validity": {
            "from": latest_unit_rate["valid_from"],
            "to": latest_unit_rate["valid_to"],
        },
    }


def fetch_tariffs(region_code, max_tariffs):
    url = f"{BASE_URL}/products/"
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    products = response.json()["results"]
    frozen_tariffs = []

    for product in products:
        if len(frozen_tariffs) >= max_tariffs:
            break

        unit_rates = fetch_electricity_tariffs(product["code"], region_code)
        standing_charges = fetch_standing_charges(product["code"], region_code)

        tariff = normalize_tariff(product, unit_rates, standing_charges)
        if tariff:
            frozen_tariffs.append(tariff)

    output = {
        "region_code": region_code,
        "tariffs": frozen_tariffs,
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2)

    return output

    # response = requests.get(f"{BASE_URL}/industry/grid-supply-points",
    #                         timeout=10)
    # response.raise_for_status()
    # regions = response.json()["results"]
    # GSP_REGIONS = {
    #     "A": "Eastern England",
    #     "B": "East Midlands",
    #     "C": "London",
    #     "D": "South East England",
    #     "E": "South Wales",
    #     "F": "West Midlands",
    #     "G": "North West England",
    #     "H": "Southern England",
    #     "J": "South Eastern England",
    #     "K": "North Wales & Merseyside",
    #     "L": "South West England",
    #     "M": "Yorkshire",
    #     "N": "North East England",
    #     "P": "North Scotland",
    # }
    # for region in GSP_REGIONS.items():
    #     print(region)
    #
    #
    # region_code = input("Please enter the desired region code: ")
    # max_tariffs = int(input("Please enter the maximum number of tariffs to fetch: "))
    # main(region_code, max_tariffs)
