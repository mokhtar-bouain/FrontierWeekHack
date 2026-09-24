from pathlib import Path
import csv
from typing import Optional


DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "energy"

PRODUCTION_FILE = DATA_DIR / "production_output.csv"
ENERGY_FILE = DATA_DIR / "energy_consumption.csv"


def _read_csv(file_path: Path) -> list[dict]:
    with file_path.open("r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def get_energy_data(
    period: str,
    production_line: str
) -> Optional[dict]:
    """Combine production and energy data for one period/line."""

    production = next(
        (
            row for row in _read_csv(PRODUCTION_FILE)
            if row["period"] == period
            and row["production_line"] == production_line
        ),
        None,
    )

    energy = next(
        (
            row for row in _read_csv(ENERGY_FILE)
            if row["period"] == period
            and row["production_line"] == production_line
        ),
        None,
    )

    if production is None or energy is None:
        return None

    return {
        "production": production,
        "energy": energy,
    }


def calculate_kwh_per_unit(
    period: str,
    production_line: str
) -> Optional[float]:

    data = get_energy_data(period, production_line)

    if data is None:
        return None

    units = int(data["production"]["units_produced"])
    energy_kwh = float(data["energy"]["total_energy_kwh"])

    if units == 0:
        return None

    return round(energy_kwh / units, 2)


def detect_energy_deviation(
    period: str,
    production_line: str,
    baseline_kwh_per_unit: float = 10.0,
    threshold_percent: float = 20.0,
) -> dict:

    actual = calculate_kwh_per_unit(period, production_line)

    if actual is None:
        return {
            "candidate": False,
            "reason": "energy_data_not_found",
        }

    deviation_percent = (
        (actual - baseline_kwh_per_unit)
        / baseline_kwh_per_unit
    ) * 100

    return {
        "period": period,
        "production_line": production_line,
        "actual_kwh_per_unit": actual,
        "baseline_kwh_per_unit": baseline_kwh_per_unit,
        "deviation_percent": round(deviation_percent, 2),
        "candidate": deviation_percent > threshold_percent,
    }


def calculate_energy_impact(
    period: str,
    production_line: str,
    baseline_kwh_per_unit: float = 10.0,
) -> dict:

    data = get_energy_data(period, production_line)

    if data is None:
        return {
            "period": period,
            "potential_excess_kwh": None,
            "potential_cost_eur": None,
        }

    units = int(data["production"]["units_produced"])
    total_energy = float(data["energy"]["total_energy_kwh"])
    price = float(
        data["energy"]["electricity_cost_eur_per_kwh"]
    )

    expected_energy = units * baseline_kwh_per_unit
    excess_energy = max(0, total_energy - expected_energy)
    potential_cost = excess_energy * price

    return {
        "period": period,
        "production_line": production_line,
        "expected_energy_kwh": round(expected_energy, 2),
        "actual_energy_kwh": round(total_energy, 2),
        "potential_excess_kwh": round(excess_energy, 2),
        "potential_cost_eur": round(potential_cost, 2),
    }