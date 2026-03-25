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
         ├── Redis Memory → memory_store / memory_recall / memory_forget
         ├── Apify → Google search for attendee/company news
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
# Fill in your API keys in .env
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
| **Redis** | Persistent agent memory | Stores/recalls meeting history, decisions, action items, preferences across sessions |
| **Civic** | Secure cloud tool access | MCP gateway to Google Calendar + Gmail with read-only guardrails and audit trail |
| **Contextual AI** | Document search (RAG) | Multi-hop retrieval over uploaded contracts, proposals, and specs |
| **Apify** | Web research | Google search for recent news about meeting attendees and their companies |

## License

MIT
