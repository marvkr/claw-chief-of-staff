# claw-chief-of-staff

An OpenClaw skill that acts as your AI Chief of Staff — prepping you for meetings and remembering what happened.

## What It Does

**Prep Mode**: Say "prep me for my meetings" and it:
1. Reads your **Calendar** for today's meetings (via Civic MCP Hub)
2. Searches your **Gmail** for recent threads with attendees (via Civic MCP Hub)
3. **Recalls past interactions** with the same people (via Redis Memory)
4. **Researches** attendees and their companies online (via Apify)
5. **Searches your documents** for relevant contracts, proposals, specs (via Contextual AI)
6. Generates a structured **briefing** with talking points

**Debrief Mode**: Say "the meeting just ended" and tell it what happened. It stores decisions, action items, preferences, and relationship context — so next time you meet that person, it's already prepared.

## Architecture

```
User → OpenClaw Gateway
         ├── Civic MCP Hub → Google Calendar, Gmail (read-only)
         ├── Redis Cloud + Agent Memory Server → memory_store / memory_recall / memory_forget
         ├── Apify → Google search for attendee/company news
         └── Contextual AI → RAG search over uploaded documents
```

### How Redis Cloud Memory Works

Redis Cloud serves as the persistent brain for your Chief of Staff. The `redis-agent-memory-server` connects to your Redis Cloud instance and provides semantic memory operations powered by OpenAI embeddings:

- **memory_store** — after a meeting debrief, stores decisions, action items, contact preferences, and relationship context as vector-indexed entries
- **memory_recall** — before a meeting, semantically searches past interactions with the same people (e.g., "what do I know about Alex Chen?" finds all related memories, not just exact name matches)
- **memory_forget** — removes outdated or incorrect memories on request

This means your meeting history, negotiation details, and contact preferences persist across sessions in Redis Cloud — so the agent is always prepared, even weeks later.

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
The memory server connects to Redis Cloud for persistent, cross-session storage.
```bash
cp .env.example .env
# Fill in your API keys in .env, including REDIS_URL from your Redis Cloud instance
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

## Sponsor Integrations

| Sponsor | Role | How It's Used |
|---------|------|---------------|
| **Redis Cloud** | Persistent agent memory | Vector-indexed storage via `redis-agent-memory-server` — stores/recalls meeting history, decisions, action items, and preferences across sessions using semantic search |
| **Civic** | Secure cloud tool access | MCP gateway to Google Calendar + Gmail with read-only guardrails and audit trail |
| **Contextual AI** | Document search (RAG) | Multi-hop retrieval over uploaded contracts, proposals, and specs |
| **Apify** | Deep attendee research | 6 scrapers — Google Search (news), LinkedIn Profile (bio/role), LinkedIn Company (size/industry), Twitter/X (recent activity), Website Crawler (About/Team pages), Crunchbase (funding/investors) |

## License

MIT
