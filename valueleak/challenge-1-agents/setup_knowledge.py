import os
from pathlib import Path

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchableField,
    SearchFieldDataType,
)


VALUELEAK_DIR = Path(__file__).resolve().parents[1]
load_dotenv(VALUELEAK_DIR / ".env")

KNOWLEDGE_DIR = VALUELEAK_DIR / "data" / "knowledge"

SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
INDEX_NAME = os.getenv(
    "AZURE_SEARCH_INDEX_NAME",
    "valueleak-knowledge"
)

if not SEARCH_ENDPOINT:
    raise ValueError(
        "AZURE_SEARCH_ENDPOINT is missing from valueleak/.env"
    )


credential = DefaultAzureCredential()


def create_index():
    index_client = SearchIndexClient(
        endpoint=SEARCH_ENDPOINT,
        credential=credential,
    )

    fields = [
        SimpleField(
            name="id",
            type=SearchFieldDataType.String,
            key=True,
        ),
        SearchableField(
            name="title",
            type=SearchFieldDataType.String,
        ),
        SearchableField(
            name="content",
            type=SearchFieldDataType.String,
        ),
        SimpleField(
            name="domain",
            type=SearchFieldDataType.String,
            filterable=True,
        ),
        SimpleField(
            name="source",
            type=SearchFieldDataType.String,
            filterable=True,
        ),
    ]

    index = SearchIndex(
        name=INDEX_NAME,
        fields=fields,
    )

    index_client.create_or_update_index(index)

    print(f"Index ready: {INDEX_NAME}")


def load_documents():
    mapping = {
        "supplier_contracts.md": "procurement",
        "finops_policy.md": "it",
        "energy_guidelines.md": "energy",
    }

    documents = []

    for filename, domain in mapping.items():
        path = KNOWLEDGE_DIR / filename

        content = path.read_text(encoding="utf-8")

        documents.append(
            {
                "id": path.stem.replace("_", "-"),
                "title": path.stem.replace("_", " ").title(),
                "content": content,
                "domain": domain,
                "source": filename,
            }
        )

    search_client = SearchClient(
        endpoint=SEARCH_ENDPOINT,
        index_name=INDEX_NAME,
        credential=credential,
    )

    results = search_client.merge_or_upload_documents(
        documents=documents
    )

    for result in results:
        print(
            f"{result.key}: "
            f"{'OK' if result.succeeded else 'FAILED'}"
        )


if __name__ == "__main__":
    create_index()
    load_documents()

    print("Knowledge indexing completed.")