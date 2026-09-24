from tools.it_tools import (
    get_cloud_resource,
    get_resource_evidence,
    check_low_utilization,
    calculate_annual_cost,
)


def test_get_cloud_resource():
    resource = get_cloud_resource("VM-002")

    assert resource is not None
    assert resource["resource_name"] == "VM-TEST-03"
    assert resource["environment"] == "test"


def test_resource_evidence():
    evidence = get_resource_evidence("VM-002")

    assert evidence["resource"] is not None
    assert evidence["usage"] is not None
    assert evidence["cost"] is not None


def test_vm_test_is_low_utilization_candidate():
    result = check_low_utilization("VM-002")

    assert result["candidate"] is True
    assert result["avg_cpu_percent"] == 0.8
    assert result["monthly_requests"] == 12


def test_vm_test_annual_cost():
    result = calculate_annual_cost("VM-002")

    assert result["monthly_cost_eur"] == 500.00
    assert result["potential_annual_value_eur"] == 6000.00


def test_backup_vm_is_also_technical_candidate():
    result = check_low_utilization("VM-003")

    # Important: metrics alone make it look unused.
    # The future Policy Agent must discover the DR exception.
    assert result["candidate"] is True