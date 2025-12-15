from OctoQuote.app.services.tariff_provider import load_tariffs_from_config

def validate_input(data):
    if data["annual_kwh"] <= 0:
        raise ValueError("annual_kwh must be > 0")

    if data["meter_type"] not in {"SMART", "STANDARD"}:
        raise ValueError("invalid meter_type")

def is_eligible(input_data, tariff):
    requires_smart = tariff["meter_requirements"]["smart_meter_required"]

    if requires_smart and input_data["meter_type"] != "SMART":
        return False

    return True

def calculate_annual_cost(annual_kwh, tariff):
    unit_rate = tariff["pricing"]["unit_rate_pence_per_kwh"]
    standing_charge = tariff["pricing"]["standing_charge_pence_per_day"]

    energy_cost = (annual_kwh * unit_rate) / 100
    standing_cost = (standing_charge * 365) / 100

    return round(energy_cost + standing_cost, 2)

def calculate_quotes(input_data):
    validate_input(input_data)

    tariffs = load_tariffs_from_config()
    results = []

    for tariff in tariffs:
        if not is_eligible(input_data, tariff):
            continue

        annual_cost = calculate_annual_cost(
            input_data["annual_kwh"],
            tariff
        )

        results.append({
            "tariff_code": tariff["tariff_code"],
            "annual_cost": annual_cost
        })

    return results