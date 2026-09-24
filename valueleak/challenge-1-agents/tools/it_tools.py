from pathlib import Path
import csv
from typing import Optional


DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "it"

RESOURCES_FILE = DATA_DIR / "cloud_resources.csv"
USAGE_FILE = DATA_DIR / "cloud_usage.csv"
COSTS_FILE = DATA_DIR / "cloud_costs.csv"


def _read_csv(file_path: Path) -> list[dict]:
    with file_path.open("r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def get_cloud_resource(resource_id: str) -> Optional[dict]:
    """Return cloud resource metadata."""
    for resource in _read_csv(RESOURCES_FILE):
        if resource["resource_id"] == resource_id:
            return resource
    return None


def get_cloud_usage(resource_id: str) -> Optional[dict]:
    """Return utilization metrics for a cloud resource."""
    for usage in _read_csv(USAGE_FILE):
        if usage["resource_id"] == resource_id:
            return usage
    return None


def get_cloud_cost(resource_id: str) -> Optional[dict]:
    """Return cost information for a cloud resource."""
    for cost in _read_csv(COSTS_FILE):
        if cost["resource_id"] == resource_id:
            return cost
    return None


def get_resource_evidence(resource_id: str) -> dict:
    """Gather resource, usage and cost evidence."""
    return {
        "resource": get_cloud_resource(resource_id),
        "usage": get_cloud_usage(resource_id),
        "cost": get_cloud_cost(resource_id),
    }


def check_low_utilization(
    resource_id: str,
    cpu_threshold: float = 5.0,
    request_threshold: int = 100,
) -> dict:
    """
    Deterministically check utilization metrics.

    This only identifies a technical candidate.
    It does NOT decide whether the resource is a value leak.
    """
    usage = get_cloud_usage(resource_id)

    if usage is None:
        return {
            "resource_id": resource_id,
            "candidate": False,
            "reason": "usage_data_not_found",
        }

    cpu = float(usage["avg_cpu_percent"])
    requests = int(usage["monthly_requests"])

    candidate = (
        cpu < cpu_threshold
        and requests < request_threshold
    )

    return {
        "resource_id": resource_id,
        "candidate": candidate,
        "avg_cpu_percent": cpu,
        "monthly_requests": requests,
        "cpu_threshold": cpu_threshold,
        "request_threshold": request_threshold,
    }


def calculate_annual_cost(resource_id: str) -> dict:
    """
    Calculate potential annual cost from the current monthly cost.

    This is potential future value, not already-realized savings.
    """
    cost = get_cloud_cost(resource_id)

    if cost is None:
        return {
            "resource_id": resource_id,
            "monthly_cost_eur": None,
            "potential_annual_value_eur": None,
        }

    monthly_cost = float(cost["monthly_cost_eur"])
    annual_cost = monthly_cost * 12

    return {
        "resource_id": resource_id,
        "monthly_cost_eur": round(monthly_cost, 2),
        "potential_annual_value_eur": round(annual_cost, 2),
    }