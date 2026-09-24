from pathlib import Path
import csv
from typing import Optional


DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "procurement"

PO_FILE = DATA_DIR / "purchase_orders.csv"
INVOICE_FILE = DATA_DIR / "invoices.csv"


def _read_csv(file_path: Path) -> list[dict]:
    with file_path.open("r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def get_purchase_order(po_id: str) -> Optional[dict]:
    """Return a purchase order by its ID."""
    for po in _read_csv(PO_FILE):
        if po["po_id"] == po_id:
            return po
    return None


def get_invoice(invoice_id: str) -> Optional[dict]:
    """Return an invoice by its ID."""
    for invoice in _read_csv(INVOICE_FILE):
        if invoice["invoice_id"] == invoice_id:
            return invoice
    return None


def get_supplier_purchase_orders(
    supplier_id: str,
    item_id: Optional[str] = None,
) -> list[dict]:
    """Return purchase orders for a supplier and optionally an item."""
    results = []

    for po in _read_csv(PO_FILE):
        if po["supplier_id"] != supplier_id:
            continue

        if item_id and po["item_id"] != item_id:
            continue

        results.append(po)

    return results


def calculate_cumulative_quantity(
    supplier_id: str,
    item_id: str,
) -> int:
    """Calculate cumulative ordered quantity for supplier/item."""
    orders = get_supplier_purchase_orders(supplier_id, item_id)

    return sum(int(po["quantity"]) for po in orders)


def calculate_discount_value(
    supplier_id: str,
    item_id: str,
    discount_percent: float,
) -> dict:
    """
    Calculate the deterministic financial value of a retroactive
    percentage discount across matching purchase orders.
    """
    orders = get_supplier_purchase_orders(supplier_id, item_id)

    total_quantity = sum(int(po["quantity"]) for po in orders)

    gross_value = sum(
        int(po["quantity"]) * float(po["unit_price"])
        for po in orders
    )

    discount_value = gross_value * (discount_percent / 100)

    return {
        "supplier_id": supplier_id,
        "item_id": item_id,
        "total_quantity": total_quantity,
        "gross_value_eur": round(gross_value, 2),
        "discount_percent": discount_percent,
        "potential_value_eur": round(discount_value, 2),
    }