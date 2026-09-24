import os
from pathlib import Path

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient


VALUELEAK_DIR = Path(__file__).resolve().parents[1]
load_dotenv(VALUELEAK_DIR / ".env")

SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
INDEX_NAME = os.getenv(
    "AZURE_SEARCH_INDEX_NAME",
    "valueleak-knowledge"
)

if not SEARCH_ENDPOINT:
    raise ValueError("AZURE_SEARCH_ENDPOINT missing from .env")


client = SearchClient(
    endpoint=SEARCH_ENDPOINT,
    index_name=INDEX_NAME,
    credential=DefaultAzureCredential(),
)


def search_knowledge(query: str, domain: str):
    results = client.search(
        search_text=query,
        filter=f"domain eq '{domain}'",
        top=1,
    )

    return list(results)


def test_procurement_contract_retrieval():
    results = search_knowledge(
        "volume discount 5000 units 10 percent",
        "procurement",
    )

    assert len(results) > 0

    document = results[0]

    assert document["source"] == "supplier_contracts.md"
    assert "5,000" in document["content"]
    assert "10%" in document["content"]


def test_it_disaster_recovery_retrieval():
    results = search_knowledge(
        "low utilization disaster recovery resource",
        "it",
    )

    assert len(results) > 0

    document = results[0]

    assert document["source"] == "finops_policy.md"
    assert "disaster recovery" in document["content"].lower()


def test_energy_certification_retrieval():
    results = search_knowledge(
        "certification mode high energy consumption",
        "energy",
    )

    assert len(results) > 0

    document = results[0]

    assert document["source"] == "energy_guidelines.md"
    assert "certification" in document["content"].lower()