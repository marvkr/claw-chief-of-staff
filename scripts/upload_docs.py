#!/usr/bin/env python3
"""Upload documents from demo/sample-docs/ to the Contextual AI datastore."""

import os
import sys

from contextual import ContextualAI
from dotenv import load_dotenv

load_dotenv()


def main():
    api_key = os.environ.get("CONTEXTUAL_API_KEY")
    datastore_id = os.environ.get("CONTEXTUAL_DATASTORE_ID")

    if not api_key:
        print("Error: CONTEXTUAL_API_KEY not set")
        sys.exit(1)
    if not datastore_id:
        print("Error: CONTEXTUAL_DATASTORE_ID not set")
        sys.exit(1)

    client = ContextualAI(api_key=api_key)

    docs_dir = os.path.join(os.path.dirname(__file__), "..", "demo", "sample-docs")
    if not os.path.exists(docs_dir):
        print(f"Error: {docs_dir} not found")
        sys.exit(1)

    files = sorted(f for f in os.listdir(docs_dir) if os.path.isfile(os.path.join(docs_dir, f)))
    if not files:
        print("No files found in demo/sample-docs/")
        sys.exit(1)

    print(f"Uploading {len(files)} documents to datastore {datastore_id}...\n")

    for filename in files:
        filepath = os.path.join(docs_dir, filename)
        print(f"  Uploading {filename}...")
        with open(filepath, "rb") as f:
            result = client.datastores.documents.ingest(
                datastore_id=datastore_id,
                file=f,
            )
        doc_id = getattr(result, "id", getattr(result, "document_id", "unknown"))
        print(f"  ✓ {filename} (id: {doc_id})")

    print(f"\nDone. {len(files)} documents uploaded.")


if __name__ == "__main__":
    main()
