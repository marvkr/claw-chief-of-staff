#!/usr/bin/env python3
"""
Apify web research script for claw-chief-of-staff.
Searches Google for recent news about meeting attendees and their companies.

Usage:
    python3 scripts/apify_research.py --names "Alex Chen,Sarah Lee" --companies "Acme Corp,TechCo"
"""

import argparse
import json
import os
import sys

from apify_client import ApifyClient


def search_google(client: ApifyClient, queries: list[str]) -> list[dict]:
    """Run Google search via Apify actor and return results."""
    results = []

    for query in queries:
        try:
            run = client.actor("apify/google-search-scraper").call(
                run_input={
                    "queries": query,
                    "maxPagesPerQuery": 1,
                    "resultsPerPage": 5,
                    "languageCode": "en",
                    "mobileResults": False,
                },
                timeout_secs=30,
            )
            items = client.dataset(run["defaultDatasetId"]).list_items().items

            for item in items:
                organic = item.get("organicResults", [])
                for result in organic[:5]:
                    results.append({
                        "title": result.get("title", ""),
                        "snippet": result.get("description", ""),
                        "url": result.get("url", ""),
                        "query": query,
                    })
        except Exception as e:
            results.append({
                "title": f"Search failed for: {query}",
                "snippet": str(e),
                "url": "",
                "query": query,
                "error": True,
            })

    return results


def main():
    parser = argparse.ArgumentParser(description="Research attendees via Apify")
    parser.add_argument("--names", required=True, help="Comma-separated attendee names")
    parser.add_argument("--companies", required=True, help="Comma-separated company names")
    args = parser.parse_args()

    token = os.environ.get("APIFY_TOKEN")
    if not token:
        print(json.dumps({"error": "APIFY_TOKEN environment variable not set", "search_results": []}))
        sys.exit(1)

    client = ApifyClient(token)

    names = [n.strip() for n in args.names.split(",") if n.strip()]
    companies = [c.strip() for c in args.companies.split(",") if c.strip()]

    queries = []
    for name in names:
        for company in companies:
            queries.append(f'"{name}" "{company}" recent news')
    for company in companies:
        queries.append(f'"{company}" funding OR launch OR announcement 2026')

    search_results = search_google(client, queries)

    output = {
        "search_results": [r for r in search_results if not r.get("error")],
        "errors": [r["snippet"] for r in search_results if r.get("error")],
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
