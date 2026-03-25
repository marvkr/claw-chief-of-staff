# claw-chief-of-staff

An AI Chief of Staff for founders, execs, and business owners. A human one costs $150-250K/year — 90% of the job is information gathering, memory, and coordination. Now you don't need one.

Say "prep me for my meetings" and the agent pulls your calendar, researches each attendee across 6 sources, surfaces relevant emails and docs, and delivers a structured briefing with talking points and open action items. Say "debrief" after and it remembers everything for next time.

| Integration | What It Does |
|---|---|
| **Civic** | Reads your Gmail and Google Calendar (read-only, with audit trail) |
| **Apify** | Scrapes LinkedIn, Crunchbase, Google News, Twitter/X, company websites, and web per attendee |
| **Contextual AI** | Multi-hop RAG over your meeting transcripts, contracts, proposals, and specs |
| **Redis Cloud** | Persistent semantic memory across sessions — decisions, action items, preferences, relationship context |

## How It Works

### Prep Mode

```
> prep me for my meetings today
```

1. Pulls your **Calendar** for today's meetings (Civic)
2. Searches your **Gmail** for recent threads with attendees (Civic)
3. **Recalls past interactions** — decisions, preferences, open action items (Redis Cloud)
4. **Researches attendees** across 6 sources — LinkedIn profile, LinkedIn company, Crunchbase, Google News, Twitter/X, company website (Apify)
5. **Searches your documents** for relevant contracts, proposals, specs (Contextual AI)
6. Compiles a structured **briefing** with talking points and open items

### Debrief Mode

```
> the meeting with Alex just ended. We agreed to extend the contract
  for 12 months at $200K. He prefers quarterly reviews. I need to
  send the revised contract by Friday.
```

The agent stores decisions, action items, preferences, and relationship context — so next time you meet that person, it's already prepared.

### Memory

```
> what do you remember about Acme Corp?
```

Redis Cloud is the persistent brain. The `redis-agent-memory-server` uses OpenAI embeddings for semantic search — "what do I know about Alex Chen?" finds all related memories, not just exact name matches. Memory operations:

- **memory_store** — saves decisions, action items, preferences, and entity info after debriefs
- **memory_recall** — semantically searches past interactions before meetings
- **memory_forget** — removes outdated or incorrect memories on request

## Architecture

```
User → OpenClaw Gateway
         ├── Civic MCP Hub → Google Calendar, Gmail (read-only)
         ├── Redis Cloud + Agent Memory Server → memory_store / memory_recall / memory_forget
         ├── Apify → 6 scrapers (Google, LinkedIn Profile, LinkedIn Company, Twitter, Website, Crunchbase)
         └── Contextual AI → RAG search over uploaded documents
```

## Setup

### Prerequisites
- Docker Desktop running
- OpenClaw installed
- Python 3.9+

### 1. Install the skill
```bash
clawhub install YOUR_USERNAME/claw-chief-of-staff
```

### 2. Start Redis Memory Server
```bash
cp .env.example .env
# Fill in your API keys in .env, including REDIS_URL from Redis Cloud
# (https://cloud.redis.io → Database → Connect → Redis CLI for the connection string)
docker compose up -d
```

### 3. Install the Redis memory plugin
```bash
openclaw plugins install openclaw-redis-agent-memory
```

### 4. Install the Civic skill
```bash
clawhub install civictechuser/openclaw-civic-skill
```

### 5. Set up Civic OAuth (on a SEPARATE device)
Visit your Civic Hub and connect Google Calendar + Gmail with read-only scopes.

### 6. Set up Contextual AI
```bash
pip install -r requirements.txt
python3 scripts/setup_contextual.py
# Copy the printed CONTEXTUAL_AGENT_ID to your .env
```

Upload relevant documents (contracts, proposals, specs) via the Contextual AI dashboard.

### 7. Configure OpenClaw
Copy `openclaw.json` to your OpenClaw config directory, or merge the plugin/skill entries into your existing config.

## Usage

```
> prep me for my meetings today

> prep me for my meeting with Alex Chen

> the meeting with Alex just ended. We agreed to extend the contract
  for 12 months at $200K. He prefers quarterly reviews. I need to
  send the revised contract by Friday.

> what do you remember about Acme Corp?
```

## License

MIT
