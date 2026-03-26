#!/usr/bin/env python3
"""
Apify research script for claw-chief-of-staff.
Researches meeting attendees and their companies using Apify scrapers:
- Google Search (news, announcements)
- LinkedIn Profile search (via Google site: search)
- LinkedIn Company search (via Google site: search)
- Twitter/X search (via Google site: search)
- Website Content Crawler (company About/Team pages)
- Crunchbase search (via Google site: search)

Usage:
    python3 scripts/apify_research.py --names "Alex Chen,Sarah Lee" --companies "Acme Corp,TechCo"
    python3 scripts/apify_research.py --names "Alex Chen" --companies "ColdIQ" --urls "https://linkedin.com/in/alex-vacca"
"""

import argparse
import json
import os
import sys

from dotenv import load_dotenv

load_dotenv()

from apify_client import ApifyClient


def _google_search(client: ApifyClient, query: str, max_results: int = 5, timeout: int = 30) -> list[dict]:
    """Run a single Google search query via Apify and return organic results."""
    try:
        run = client.actor("apify/google-search-scraper").call(
            run_input={
                "queries": query,
                "maxPagesPerQuery": 1,
                "resultsPerPage": max_results,
                "languageCode": "en",
                "mobileResults": False,
            },
            timeout_secs=timeout,
        )
        items = client.dataset(run["defaultDatasetId"]).list_items().items
        results = []
        for item in items:
            for result in item.get("organicResults", [])[:max_results]:
                results.append({
                    "title": result.get("title", ""),
                    "snippet": result.get("description", ""),
                    "url": result.get("url", ""),
                    "query": query,
                })
        return results
    except Exception as e:
        return [{"error": True, "source": "google", "detail": str(e), "query": query}]


def search_google(client: ApifyClient, names: list[str], companies: list[str]) -> list[dict]:
    """Search Google for recent news about attendees and companies."""
    results = []
    queries = []
    for name in names:
        for company in companies:
            queries.append(f'"{name}" "{company}" recent news')
    for company in companies:
        queries.append(f'"{company}" funding OR launch OR announcement 2026')

    for query in queries:
        results.extend(_google_search(client, query))
    return results


def search_linkedin_profiles(client: ApifyClient, names: list[str], companies: list[str], urls: list[str] | None = None) -> list[dict]:
    """Find LinkedIn profiles via Google site: search. Also scrapes direct URLs if provided."""
    results = []

    # Search by name + company
    for name in names:
        for company in companies:
            query = f'site:linkedin.com/in "{name}" "{company}"'
            hits = _google_search(client, query, max_results=3)
            for hit in hits:
                if not hit.get("error"):
                    results.append({
                        "name": name,
                        "headline": hit.get("snippet", ""),
                        "url": hit.get("url", ""),
                        "source": "linkedin_profile_search",
                        "query": f"{name} {company}",
                    })

    # Also scrape direct LinkedIn URLs if provided
    if urls:
        for url in urls:
            if "linkedin.com/in/" in url:
                try:
                    run = client.actor("apify/website-content-crawler").call(
                        run_input={
                            "startUrls": [{"url": url}],
                            "maxCrawlPages": 1,
                            "crawlerType": "cheerio",
                        },
                        timeout_secs=30,
                    )
                    items = client.dataset(run["defaultDatasetId"]).list_items().items
                    for item in items[:1]:
                        text = item.get("text", "")
                        results.append({
                            "name": item.get("title", "").replace(" | LinkedIn", ""),
                            "headline": text[:500] if text else "",
                            "url": url,
                            "source": "linkedin_profile_direct",
                            "query": url,
                        })
                except Exception as e:
                    results.append({"error": True, "source": "linkedin_profile_direct", "detail": str(e), "query": url})

    return results


def search_linkedin_companies(client: ApifyClient, companies: list[str]) -> list[dict]:
    """Find LinkedIn company pages via Google site: search."""
    results = []
    for company in companies:
        query = f'site:linkedin.com/company "{company}"'
        hits = _google_search(client, query, max_results=3)
        for hit in hits:
            if not hit.get("error"):
                results.append({
                    "name": company,
                    "description": hit.get("snippet", ""),
                    "url": hit.get("url", ""),
                    "source": "linkedin_company_search",
                    "query": company,
                })
    return results


def search_tweets(client: ApifyClient, names: list[str]) -> list[dict]:
    """Find recent tweets/X posts via Google site: search."""
    results = []
    for name in names:
        query = f'site:twitter.com OR site:x.com "{name}"'
        hits = _google_search(client, query, max_results=5)
        for hit in hits:
            if not hit.get("error"):
                results.append({
                    "text": hit.get("snippet", ""),
                    "url": hit.get("url", ""),
                    "source": "twitter_search",
                    "query": name,
                })
    return results


def scrape_websites(client: ApifyClient, companies: list[str]) -> list[dict]:
    """Scrape company websites for About/Team page content."""
    results = []
    for company in companies:
        domain = company.lower().replace(" ", "").replace(".", "") + ".com"
        try:
            run = client.actor("apify/website-content-crawler").call(
                run_input={
                    "startUrls": [{"url": f"https://{domain}"}],
                    "maxCrawlPages": 3,
                    "crawlerType": "cheerio",
                },
                timeout_secs=60,
            )
            items = client.dataset(run["defaultDatasetId"]).list_items().items
            for item in items[:3]:
                text = item.get("text", "")
                results.append({
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "text": text[:1000] if text else "",
                    "query": company,
                })
        except Exception as e:
            results.append({"error": True, "source": "website", "detail": str(e), "query": company})
    return results


def search_crunchbase(client: ApifyClient, companies: list[str]) -> list[dict]:
    """Find Crunchbase info via Google site: search."""
    results = []
    for company in companies:
        query = f'site:crunchbase.com/organization "{company}"'
        hits = _google_search(client, query, max_results=3)
        for hit in hits:
            if not hit.get("error"):
                results.append({
                    "name": company,
                    "description": hit.get("snippet", ""),
                    "url": hit.get("url", ""),
                    "source": "crunchbase_search",
                    "query": company,
                })
    return results


def main():
    parser = argparse.ArgumentParser(description="Research attendees via Apify scrapers")
    parser.add_argument("--names", required=True, help="Comma-separated attendee names")
    parser.add_argument("--companies", required=True, help="Comma-separated company names")
    parser.add_argument("--urls", default="", help="Comma-separated LinkedIn profile URLs (optional)")
    args = parser.parse_args()

    token = os.environ.get("APIFY_TOKEN")
    if not token:
        print(json.dumps({"error": "APIFY_TOKEN environment variable not set"}))
        sys.exit(1)

    client = ApifyClient(token)

    names = [n.strip() for n in args.names.split(",") if n.strip()]
    companies = [c.strip() for c in args.companies.split(",") if c.strip()]
    urls = [u.strip() for u in args.urls.split(",") if u.strip()] if args.urls else []

    print(f"Researching: {names} at {companies}...", file=sys.stderr)

    google = search_google(client, names, companies)
    print(f"  Google Search: {len([r for r in google if not r.get('error')])} results", file=sys.stderr)

    linkedin_profiles = search_linkedin_profiles(client, names, companies, urls)
    print(f"  LinkedIn Profiles: {len([r for r in linkedin_profiles if not r.get('error')])} results", file=sys.stderr)

    linkedin_companies = search_linkedin_companies(client, companies)
    print(f"  LinkedIn Companies: {len([r for r in linkedin_companies if not r.get('error')])} results", file=sys.stderr)

    tweets = search_tweets(client, names)
    print(f"  Twitter/X: {len([r for r in tweets if not r.get('error')])} results", file=sys.stderr)

    website_content = scrape_websites(client, companies)
    print(f"  Websites: {len([r for r in website_content if not r.get('error')])} results", file=sys.stderr)

    crunchbase = search_crunchbase(client, companies)
    print(f"  Crunchbase: {len([r for r in crunchbase if not r.get('error')])} results", file=sys.stderr)

    all_results = google + linkedin_profiles + linkedin_companies + tweets + website_content + crunchbase
    errors = [r for r in all_results if r.get("error")]

    clean = lambda items: [r for r in items if not r.get("error")]

    output = {
        "search_results": clean(google),
        "linkedin_profiles": clean(linkedin_profiles),
        "linkedin_companies": clean(linkedin_companies),
        "tweets": clean(tweets),
        "website_content": clean(website_content),
        "crunchbase": clean(crunchbase),
        "errors": [r["detail"] for r in errors] if errors else [],
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
