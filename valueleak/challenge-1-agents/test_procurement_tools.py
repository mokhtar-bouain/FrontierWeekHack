from tools.procurement_tools import (
    get_purchase_order,
    get_invoice,
    calculate_cumulative_quantity,
    calculate_discount_value,
)


def test_get_purchase_order():
    po = get_purchase_order("PO-001")

    assert po is not None
    assert po["supplier_id"] == "SUP-001"
    assert po["item_id"] == "COMP-A"


def test_get_invoice():
    invoice = get_invoice("INV-003")

    assert invoice is not None
    assert float(invoice["unit_price"]) == 12.00


def test_cumulative_quantity():
    quantity = calculate_cumulative_quantity(
        "SUP-001",
        "COMP-A",
    )

    assert quantity == 6000


def test_discount_calculation():
    result = calculate_discount_value(
        "SUP-001",
        "COMP-A",
        10,
    )

    assert result["total_quantity"] == 6000
    assert result["gross_value_eur"] == 72000.00
    assert result["potential_value_eur"] == 7200.00