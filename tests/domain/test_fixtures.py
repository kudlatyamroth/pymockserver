from pathlib import Path

import pytest

from pymockserver.domain import fixture

fixture.FIXTURES_DIR = Path(__file__).parent.resolve()


@pytest.mark.usefixtures("cleanup")
def test_if_fixtures_are_loaded(client):
    fixture.load_fixtures()

    http_response = {
        "data": {
            "currencyRates": [
                {
                    "currencyCode": "PLN",
                    "currencyRate": "4.194753000000",
                    "roundingPolicy": "ROUND_HALF_UP",
                }
            ],
            "allowedCurrencies": ["EUR", "GBP", "JPY", "PLN", "USD"],
            "sellerAllowedCurrencies": ["EUR", "GBP", "PLN"],
            "sellerNotAllowedCurrencies": ["JPY", "USD"],
            "currencyConversionFee": "1.0249",
        }
    }

    mock_response = client.get("/api/v2/currency-policies")
    assert mock_response.status_code == 200
    assert mock_response.json() == http_response
