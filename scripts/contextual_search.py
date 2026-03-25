#!/usr/bin/env python3
"""
Query Contextual AI agent for relevant documents.

Usage:
    python3 scripts/contextual_search.py --query "contract terms with Acme Corp"
"""

import argparse
import json
import os
import sys

from contextual import ContextualAI
from dotenv import load_dotenv

load_dotenv()


def main():
    parser = argparse.ArgumentParser(description="Search documents via Contextual AI")
    parser.add_argument("--query", required=True, help="Search query")
    args = parser.parse_args()

    api_key = os.environ.get("CONTEXTUAL_API_KEY")
    agent_id = os.environ.get("CONTEXTUAL_AGENT_ID")

    if not api_key:
        print(json.dumps({"error": "CONTEXTUAL_API_KEY not set", "response": ""}))
        sys.exit(1)

    if not agent_id:
        print(json.dumps({"error": "CONTEXTUAL_AGENT_ID not set. Run setup_contextual.py first.", "response": ""}))
        sys.exit(1)

    client = ContextualAI(api_key=api_key)

    try:
        response = client.agents.query.create(
            agent_id=agent_id,
            messages=[{"role": "user", "content": args.query}],
        )

        output = {
            "response": response.message.content,
            "retrieval_contents": [],
        }

        if hasattr(response, "retrieval_contents") and response.retrieval_contents:
            for item in response.retrieval_contents[:5]:
                output["retrieval_contents"].append({
                    "text": getattr(item, "text", ""),
                    "doc_name": getattr(item, "doc_name", ""),
                    "score": getattr(item, "score", 0),
                })

        print(json.dumps(output, indent=2))

    except Exception as e:
        print(json.dumps({"error": str(e), "response": ""}))
        sys.exit(1)


if __name__ == "__main__":
    main()
