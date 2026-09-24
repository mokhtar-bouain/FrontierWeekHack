from tools.energy_tools import (
    get_energy_data,
    calculate_kwh_per_unit,
    detect_energy_deviation,
    calculate_energy_impact,
)


def test_get_energy_data():
    data = get_energy_data("2026-04", "LINE-01")

    assert data is not None
    assert data["production"]["product_id"] == "PRODUCT-A"


def test_calculate_kwh_per_unit():
    result = calculate_kwh_per_unit(
        "2026-04",
        "LINE-01",
    )

    assert result == 13.0


def test_detect_energy_deviation():
    result = detect_energy_deviation(
        "2026-04",
        "LINE-01",
    )

    assert result["candidate"] is True
    assert result["deviation_percent"] == 30.0


def test_calculate_energy_impact():
    result = calculate_energy_impact(
        "2026-04",
        "LINE-01",
    )

    assert result["potential_excess_kwh"] == 3000.0
    assert result["potential_cost_eur"] == 600.0


def test_certification_is_technical_candidate():
    result = detect_energy_deviation(
        "2026-05",
        "LINE-01",
    )

    # Metrics alone look anomalous.
    # Policy/RAG will later identify certification mode.
    assert result["candidate"] is True