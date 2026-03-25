# Video Demo Guide

## Demo Scenario

You're **Marvin Kaunda, Founder of BetterDesign** — a design studio working with enterprise clients. You have 3 meetings today and you need your AI Chief of Staff to prep you.

### The 3 Meetings

| Time | Meeting | Person | Company | What's Happening |
|------|---------|--------|---------|-----------------|
| 10:00 AM | Partnership Review | Alex Chen | Acme Corp | Contract renewal negotiation — expanding from $15K to $20K/month, adding mobile scope |
| 2:00 PM | Investor Check-in | Sarah Mitchell | Horizon Ventures | Quarterly update — Q1 numbers, runway, asks for intros |
| 4:00 PM | Product Integration Sync | James Rodriguez | TechFlow | Phase 2 kickoff — developer portal design, dark mode discussion |

---

## Pre-Demo Setup (do this before recording)

### 1. Create Google Calendar Events

Create these 3 events in your Google Calendar for today:

**Event 1: Partnership Review — Acme Corp**
- Time: 10:00 AM - 11:00 AM
- Description: "Contract renewal discussion — reviewing expanded scope for FY2026"
- Add attendee: alex.chen@acmecorp.com (or a real email you control)

**Event 2: Investor Update — Horizon Ventures**
- Time: 2:00 PM - 2:30 PM
- Description: "Q1 2026 quarterly investor check-in"
- Add attendee: sarah.mitchell@horizonvc.com (or a real email you control)

**Event 3: Design System Sync — TechFlow**
- Time: 4:00 PM - 4:45 PM
- Description: "Phase 2 kickoff — developer portal design review"
- Add attendee: james@techflow.dev (or a real email you control)

### 2. Send Yourself Fake Email Threads

Send a few emails to/from yourself (or between accounts you control) so Gmail search has something to surface:

**Thread 1** (about Acme Corp renewal):
- Subject: "Re: FY2026 Contract Renewal — BetterDesign x Acme"
- Body: "Hi Marvin, following up on our Jan conversation. We'd like to discuss expanding scope to include mobile. Can we review pricing options on our next call? Budget-wise, I'm working with $200-250K annually. — Alex"

**Thread 2** (about investor update):
- Subject: "Re: Q1 Board Materials"
- Body: "Thanks for the draft Marvin. Numbers look strong. A few things I'd like to dig into on our call: (1) the capacity constraint, (2) timeline for the productized offering, (3) a couple warm intros I have in mind. — Sarah"

**Thread 3** (about TechFlow):
- Subject: "Re: Phase 2 Wireframes"
- Body: "Marvin — Phase 1 handoff was great, cleanest we've received. For Phase 2, the API playground is the hero. Also want to discuss dark mode as default for the portal. We're pitching investors next month so polish matters. — James"

### 3. Upload Documents to Contextual AI

Upload these 3 files from `demo/sample-docs/` to your Contextual AI dashboard:
- `acme_corp_master_services_agreement.md` — the Acme Corp contract
- `horizon_ventures_q1_2026_update.md` — investor update
- `techflow_api_integration_spec.md` — TechFlow integration spec

**How**: Go to your Contextual AI dashboard → select your datastore → upload files. If they only accept PDF, convert with: `pandoc file.md -o file.pdf` (or print-to-PDF from any markdown viewer).

### 4. Seed Redis Memories (Previous Debrief)

Make sure Docker is running and the memory server is healthy:
```bash
docker compose up -d
curl http://localhost:8000/v1/health
```

Then seed memories from a "previous meeting" so the demo shows memory recall working:
```bash
bash demo/seed_memories.sh
```

### 5. Verify Everything is Running

```bash
# Redis memory server
curl -s http://localhost:8000/v1/health | python3 -m json.tool

# Test memory recall
curl -s http://localhost:8000/v1/memory/recall \
  -H "Content-Type: application/json" \
  -d '{"query": "Alex Chen Acme Corp", "namespace": "chief-of-staff", "limit": 3}' | python3 -m json.tool

# Test Apify (quick check)
python3 scripts/apify_research.py --names "test" --companies "test" 2>&1 | head -5

# Test Contextual AI
python3 scripts/contextual_search.py --query "Acme Corp contract terms" 2>&1 | head -5
```

---

## Demo Script (what to say/show in the video)

### Scene 1: The Hook (30 seconds)

> "A human Chief of Staff costs $150-250K a year. Ninety percent of that job is information gathering, memory, and coordination. I built an AI that does all of it."

Show the OpenClaw interface. Type:

```
prep me for my meetings today
```

### Scene 2: Watch It Work (60-90 seconds)

Narrate as the agent runs through each step:

> "It's pulling my calendar... found 3 meetings today."

> "Now it's searching my email for recent threads with each attendee..."

> "It's checking its memory — I debriefed it after my last meeting with Alex Chen, so it remembers the contract details and his preferences."

> "Now it's researching each person across 6 sources — LinkedIn, Crunchbase, Twitter, Google News, their company website..."

> "And finally, it's searching my uploaded documents — contracts, proposals, specs — for anything relevant."

### Scene 3: The Briefing (60 seconds)

Walk through one complete briefing (Alex Chen is the best one — richest data):

> "Here's what I get — a structured briefing for each meeting."

Highlight the sections:
- **Memory**: "It remembers from our last debrief that Alex has budget authority up to $250K and prefers quarterly reviews"
- **Email**: "Recent thread about the renewal — he's working with $200-250K annually"
- **Research**: "LinkedIn, Crunchbase data about Acme Corp, recent news"
- **Documents**: "It found the relevant contract — current rate is $15K/month, expiring March 31"
- **Talking points**: "Synthesized from all sources — suggests discussing expanded scope, pricing tiers"

> "I didn't look any of this up. The agent pulled it from 4 different systems in under a minute."

### Scene 4: The Debrief (30-45 seconds)

> "Now the meeting's over. I tell it what happened."

Type:
```
The meeting with Alex Chen just ended. We agreed to renew the contract for 12 months at $20K/month — that's $240K annually, up from $180K. The expanded scope includes mobile app redesign. Alex wants quarterly reviews instead of monthly. I need to send the revised contract by Friday March 28. Alex also mentioned they're evaluating their design tools budget in Q3 — potential upsell opportunity.
```

> "It stores every decision, action item, preference, and relationship detail. Next time I meet Alex — or anyone at Acme — this all surfaces automatically."

### Scene 5: The Close (15 seconds)

> "Calendar, email, memory, research, documents — all synthesized into one briefing. That's an AI Chief of Staff."

---

## Troubleshooting

- **No calendar events**: Make sure the events are created for today's date and Civic OAuth is connected
- **No email results**: Emails need to be in the last 14 days (search uses `newer_than:14d`)
- **Memory recall empty**: Run `seed_memories.sh` and verify with the curl test above
- **Apify slow**: The 6 scrapers run sequentially, can take 30-60 seconds. For the demo, this is fine — narrate while it runs
- **Contextual AI no results**: Make sure documents are uploaded AND the datastore has finished indexing (can take a few minutes after upload)
