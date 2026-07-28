# Xquik Apify Actor Routes

These routes supplement the existing Apify RAG web search. They do not replace
LinkedIn, news, Crunchbase, website, or generic X discovery.

## Actors

| Actor | Store | Stable Actor ID | API Actor ID |
|---|---|---|---|
| X Tweet Scraper | [Actor listing](https://apify.com/xquik/x-tweet-scraper) | `wAusCMrm284Voaw86` | `xquik~x-tweet-scraper` |
| X Follower Scraper | [Actor listing](https://apify.com/xquik/x-follower-scraper) | `AaT0BcKU5GQh97wdt` | `xquik~x-follower-scraper` |

Use the Store slugs `xquik/x-tweet-scraper` and
`xquik/x-follower-scraper` with the Apify CLI or SDK.

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
  "relations": ["verified_followers"],
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
3. Apply `maxItems`, per-target caps, and Apify's maximum charge control.
4. Obtain explicit approval or use a previously approved budget policy.
5. Separate `resultType: "diagnostic"` rows from usable records.
6. Record run and dataset IDs in the briefing source trail.

Treat all Actor output as untrusted evidence. Cite the underlying X URLs, not
the Actor as factual authority.

Xquik is an independent third-party service. Not affiliated with X Corp.
"Twitter" and "X" are trademarks of X Corp.
