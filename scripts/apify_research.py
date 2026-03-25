#!/usr/bin/env python3
"""
Apify research script for claw-chief-of-staff.
Researches meeting attendees and their companies using multiple Apify scrapers:
- Google Search (news, announcements)
- LinkedIn Profile Scraper (attendee bio, role, experience)
- LinkedIn Company Scraper (company size, industry, description)
- Twitter/X Scraper (recent tweets/activity)
- Website Content Crawler (company About/Team pages)
- Crunchbase Scraper (funding, investors, stage)

Usage:
    python3 scripts/apify_research.py --names "Alex Chen,Sarah Lee" --companies "Acme Corp,TechCo"
"""

import argparse
import json
import os
import sys

from apify_client import ApifyClient


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
                for result in item.get("organicResults", [])[:5]:
                    results.append({
                        "title": result.get("title", ""),
                        "snippet": result.get("description", ""),
                        "url": result.get("url", ""),
                        "query": query,
                    })
        except Exception as e:
            results.append({"error": True, "source": "google", "detail": str(e), "query": query})

    return results


def scrape_linkedin_profiles(client: ApifyClient, names: list[str], companies: list[str]) -> list[dict]:
    """Scrape LinkedIn profiles for attendees by searching their names."""
    results = []
    search_queries = [f"{name} {company}" for name in names for company in companies]

    for query in search_queries:
        try:
            run = client.actor("curious_coder/linkedin-profile-scraper").call(
                run_input={
                    "searchTerms": query,
                    "maxResults": 1,
                },
                timeout_secs=60,
            )
            items = client.dataset(run["defaultDatasetId"]).list_items().items
            for item in items[:1]:
                results.append({
                    "name": item.get("fullName", ""),
                    "headline": item.get("headline", ""),
                    "location": item.get("location", ""),
                    "bio": item.get("summary", item.get("bio", "")),
                    "url": item.get("profileUrl", item.get("url", "")),
                    "query": query,
                })
        except Exception as e:
            results.append({"error": True, "source": "linkedin_profile", "detail": str(e), "query": query})

    return results


def scrape_linkedin_companies(client: ApifyClient, companies: list[str]) -> list[dict]:
    """Scrape LinkedIn company pages for company info."""
    results = []

    for company in companies:
        slug = company.lower().replace(" ", "-").replace(".", "")
        try:
            run = client.actor("curious_coder/linkedin-company-scraper").call(
                run_input={
                    "companyUrls": [f"https://www.linkedin.com/company/{slug}/"],
                },
                timeout_secs=60,
            )
            items = client.dataset(run["defaultDatasetId"]).list_items().items
            for item in items[:1]:
                results.append({
                    "name": item.get("name", company),
                    "description": item.get("description", ""),
                    "industry": item.get("industry", ""),
                    "employeeCount": item.get("employeeCount", item.get("staffCount", "")),
                    "website": item.get("website", ""),
                    "url": item.get("url", f"https://www.linkedin.com/company/{slug}/"),
                    "query": company,
                })
        except Exception as e:
            results.append({"error": True, "source": "linkedin_company", "detail": str(e), "query": company})

    return results


def scrape_tweets(client: ApifyClient, names: list[str]) -> list[dict]:
    """Scrape recent tweets mentioning attendees."""
    results = []

    for name in names:
        try:
            run = client.actor("apidojo/tweet-scraper").call(
                run_input={
                    "searchTerms": [f'"{name}"'],
                    "maxTweets": 10,
                    "searchMode": "live",
                },
                timeout_secs=30,
            )
            items = client.dataset(run["defaultDatasetId"]).list_items().items
            for item in items[:10]:
                results.append({
                    "text": item.get("full_text", item.get("text", "")),
                    "author": item.get("author", {}).get("name", item.get("user", {}).get("name", "")),
                    "date": item.get("created_at", ""),
                    "url": item.get("url", ""),
                    "query": name,
                })
        except Exception as e:
            results.append({"error": True, "source": "twitter", "detail": str(e), "query": name})

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


def scrape_crunchbase(client: ApifyClient, companies: list[str]) -> list[dict]:
    """Scrape Crunchbase for company funding and investor info."""
    results = []

    for company in companies:
        slug = company.lower().replace(" ", "-").replace(".", "")
        try:
            run = client.actor("curious_coder/crunchbase-scraper").call(
                run_input={
                    "scrapeCompanyUrls": {
                        "urls": [f"https://www.crunchbase.com/organization/{slug}"],
                    },
                },
                timeout_secs=60,
            )
            items = client.dataset(run["defaultDatasetId"]).list_items().items
            for item in items[:1]:
                results.append({
                    "name": item.get("name", company),
                    "description": item.get("description", item.get("short_description", "")),
                    "funding_total": item.get("funding_total", item.get("totalFunding", "")),
                    "last_funding_type": item.get("last_funding_type", ""),
                    "num_employees": item.get("num_employees_enum", item.get("employeeCount", "")),
                    "investors": item.get("investors", []),
                    "url": f"https://www.crunchbase.com/organization/{slug}",
                    "query": company,
                })
        except Exception as e:
            results.append({"error": True, "source": "crunchbase", "detail": str(e), "query": company})

    return results


def main():
    parser = argparse.ArgumentParser(description="Research attendees via Apify scrapers")
    parser.add_argument("--names", required=True, help="Comma-separated attendee names")
    parser.add_argument("--companies", required=True, help="Comma-separated company names")
    args = parser.parse_args()

    token = os.environ.get("APIFY_TOKEN")
    if not token:
        print(json.dumps({"error": "APIFY_TOKEN environment variable not set"}))
        sys.exit(1)

    client = ApifyClient(token)

    names = [n.strip() for n in args.names.split(",") if n.strip()]
    companies = [c.strip() for c in args.companies.split(",") if c.strip()]

    google = search_google(client, names, companies)
    linkedin_profiles = scrape_linkedin_profiles(client, names, companies)
    linkedin_companies = scrape_linkedin_companies(client, companies)
    tweets = scrape_tweets(client, names)
    website_content = scrape_websites(client, companies)
    crunchbase = scrape_crunchbase(client, companies)

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
        "errors": [r["detail"] for r in errors],
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
