#!/usr/bin/env python3
"""
One-time setup for Contextual AI: creates a datastore, uploads sample documents,
and creates an agent for the Chief of Staff skill.

Usage:
    python3 scripts/setup_contextual.py

After running, copy the printed CONTEXTUAL_AGENT_ID into your .env file.
"""

import os
import sys
import time

from contextual import ContextualAI
from dotenv import load_dotenv

load_dotenv()


def main():
    api_key = os.environ.get("CONTEXTUAL_API_KEY")
    if not api_key:
        print("Error: CONTEXTUAL_API_KEY not set in environment")
        sys.exit(1)

    client = ContextualAI(api_key=api_key)

    # Step 1: Create datastore
    print("Creating datastore...")
    datastore = client.datastores.create(name="chief-of-staff-docs")
    datastore_id = datastore.id
    print(f"Datastore created: {datastore_id}")

    # Step 2: Upload documents
    docs_dir = os.path.join(os.path.dirname(__file__), "..", "sample-docs")
    if os.path.exists(docs_dir):
        for filename in os.listdir(docs_dir):
            filepath = os.path.join(docs_dir, filename)
            if os.path.isfile(filepath) and filename.endswith(".pdf"):
                print(f"Uploading {filename}...")
                with open(filepath, "rb") as f:
                    client.datastores.documents.create(
                        datastore_id=datastore_id,
                        file=f,
                        metadata={"title": filename, "source": "chief-of-staff-setup"},
                    )
                print(f"  Uploaded {filename}")
    else:
        print(f"No sample-docs/ directory found at {docs_dir}")
        print("You can upload documents later via the Contextual AI dashboard.")

    # Step 3: Wait briefly for processing to start
    print("Waiting for document processing to begin...")
    time.sleep(5)

    # Step 4: Create agent
    print("Creating agent...")
    agent = client.agents.create(
        name="Chief of Staff RAG",
        description=(
            "Searches over uploaded business documents (contracts, proposals, specs, "
            "meeting notes) to find relevant context for meeting preparation. "
            "Returns specific excerpts with source citations."
        ),
        datastore_ids=[datastore_id],
    )
    agent_id = agent.id
    print(f"Agent created: {agent_id}")

    # Step 5: Output for .env
    print("\n" + "=" * 60)
    print("Setup complete! Add these to your .env file:")
    print(f"CONTEXTUAL_AGENT_ID={agent_id}")
    print(f"CONTEXTUAL_DATASTORE_ID={datastore_id}")
    print("=" * 60)


if __name__ == "__main__":
    main()
