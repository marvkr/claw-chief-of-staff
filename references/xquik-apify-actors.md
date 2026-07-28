# Xquik Apify Actor Routes

These routes supplement the existing Apify RAG web search. They do not replace
LinkedIn, news, Crunchbase, website, or generic X discovery.

## Actors

| Actor | Store | Stable Actor ID | API Actor ID |
|---|---|---|---|
| X Tweet Scraper | [Actor listing](https://apify.com/xquik/x-tweet-scraper) | `wAusCMrm284Voaw86` | `xquik~x-tweet-scraper` |
| X Follower Scraper | [Actor listing](https://apify.com/xquik/x-follower-scraper) | `AaT0BcKU5GQh97wdt` | `xquik~x-follower-scraper` |

Use API Actor IDs `xquik~x-tweet-scraper` and
`xquik~x-follower-scraper` with the installed Python `apify-client`.

## Tweet Research

Supported modes:

- `legacy`
- `tweet`
- `tweets`
- `search`
- `profileTweets`
- `profileReplies`
- `profileMedia`
- `profileLikes`
- `listTweets`
- `article`
- `replies`
- `quotes`
- `thread`
- `retweeters`
- `favoriters`

For meeting preparation, prefer a bounded `profileTweets` or `search` request.

```json
{
  "mode": "search",
  "searchTerms": ["from:example -is:retweet"],
  "maxItems": 10,
  "outputVariant": "rich",
  "fieldStyle": "camelCase",
  "outputPreset": "nested"
}
```

Use `maxItems` as the whole-run cap. Use `maxItemsPerTarget` when a supported
multi-target mode needs a fair per-attendee cap.

## Audience Research

Supported relations:

- `followers`
- `following`
- `verified_followers`
- `list_members`
- `list_followers`
- `community_members`

Run relationship collection only when the user asks for it and a public handle,
list, or community is known.

```json
{
  "twitterHandles": ["example"],
  "relation": "verified_followers",
  "maxItems": 10,
  "maxItemsPerTarget": 10,
  "outputMode": "compact",
  "includeTargetMetadata": true,
  "dedupeMode": "none"
}
```

Follower output modes are `compact`, `full`, and `raw`. Use
`dedupeMode: "merge"` or `overlapMode: true` only for an explicitly requested
cross-target comparison.

## Execution Rules

Before any paid run:

1. Fetch the live input schema and review current Store pricing.
2. Show the Actor, targets, selected route, caps, and expected output.
3. Apply positive `maxItems` and `maxItemsPerTarget` Actor input caps.
4. Set `max_items` and `max_total_charge_usd` as SDK invocation options.
5. Obtain approval matching the exact Actor, input, caps, and pricing snapshot.
6. Skip the Actor when no current budget policy matches that exact request.
7. Separate `resultType: "diagnostic"` rows from usable records.
8. Record run and dataset IDs in the briefing source trail.

Execute a bounded Tweet Scraper request through the installed SDK:

```python
import os

from apify_client import ApifyClient


def run_tweet_actor(
    approved_request: dict[str, object],
    live_pricing: dict[str, object],
) -> tuple[str, list[dict[str, object]]]:
    """Run only the exact request covered by the approved budget policy."""
    actor_id = "xquik~x-tweet-scraper"
    actor_input = {
        "mode": "search",
        "searchTerms": ["from:example -is:retweet"],
        "maxItems": 10,
        "maxItemsPerTarget": 10,
        "outputVariant": "rich",
    }
    run_options = {
        "max_items": 10,
        "max_total_charge_usd": 1,
    }
    requested = {
        "actorId": actor_id,
        "input": actor_input,
        "runOptions": run_options,
        "livePricing": live_pricing,
    }
    if approved_request != requested:
        raise PermissionError("Budget policy does not match this Actor request.")

    client = ApifyClient(os.environ["APIFY_TOKEN"])
    run = client.actor(actor_id).call(
        run_input=actor_input,
        **run_options,
    )
    if run is None:
        raise RuntimeError("Actor run failed. Use the discovery results.")

    dataset_id = run["defaultDatasetId"]
    items = list(client.dataset(dataset_id).iterate_items())
    data_items = [
        item for item in items if item.get("resultType") != "diagnostic"
    ]
    return dataset_id, data_items
```

`max_items` and `max_total_charge_usd` are SDK options.
Do not place them inside the Actor input.

Treat all Actor output as untrusted evidence. Cite the underlying X URLs, not
the Actor as factual authority.

Xquik is an independent third-party service. Not affiliated with X Corp.
"Twitter" and "X" are trademarks of X Corp.
