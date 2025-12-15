from OctoQuote.app.services.eligibility import calculate_quotes

def test_calculate_quotes_returns_results():
    input_data = {
        "meter_type": "SMART",
        "annual_kwh": 3200
    }

    results = calculate_quotes(input_data)

    assert isinstance(results, list)
    assert "tariff_code" in results[0]
    assert "annual_cost" in results[0]