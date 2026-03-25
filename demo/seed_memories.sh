#!/bin/bash
# Seed Redis memory with "previous meeting" data so the demo shows memory recall working.
# Run this AFTER docker compose up -d and verifying health.

MEMORY_URL="http://localhost:8000/v1/long-term-memory"
NAMESPACE="chief-of-staff"

echo "Seeding memories for demo..."

# --- Alex Chen / Acme Corp (from a "previous debrief" on Feb 15, 2026) ---

curl -s -X POST "$MEMORY_URL/" \
  -H "Content-Type: application/json" \
  -d '{
    "memories": [{
      "id": "demo-alex-renewal",
      "text": "Meeting with Alex Chen (VP Partnerships, Acme Corp) on 2026-02-15: Discussed contract renewal for FY2026. Alex confirmed interest in renewing the MSA. Current agreement is $15K/month ($180K annually) expiring March 31, 2026. Alex wants to explore expanded scope to include mobile app redesign.",
      "namespace": "'"$NAMESPACE"'",
      "topics": ["meeting", "contract", "renewal"],
      "entities": ["Alex Chen", "Acme Corp"],
      "memory_type": "episodic",
      "event_date": "2026-02-15T10:00:00Z"
    }]
  }' | python3 -c "import sys,json; r=json.load(sys.stdin); print('[1/8] Stored: Alex Chen renewal discussion' if 'status' not in r or r.get('status') != 'error' else f'[1/8] FAILED: {r}')" 2>&1

curl -s -X POST "$MEMORY_URL/" \
  -H "Content-Type: application/json" \
  -d '{
    "memories": [{
      "id": "demo-alex-budget",
      "text": "Alex Chen at Acme Corp has budget authority up to $250K annually for design services. Anything above $200K requires VP Product sign-off. Learned on 2026-01-20.",
      "namespace": "'"$NAMESPACE"'",
      "topics": ["budget", "authority"],
      "entities": ["Alex Chen", "Acme Corp"],
      "memory_type": "semantic"
    }]
  }' | python3 -c "import sys,json; r=json.load(sys.stdin); print('[2/8] Stored: Alex Chen budget authority' if 'status' not in r or r.get('status') != 'error' else f'[2/8] FAILED: {r}')" 2>&1

curl -s -X POST "$MEMORY_URL/" \
  -H "Content-Type: application/json" \
  -d '{
    "memories": [{
      "id": "demo-alex-prefs",
      "text": "Alex Chen prefers quarterly reviews over monthly check-ins. He finds monthly meetings excessive for a retainer relationship. Prefers async updates via email between quarterly calls. Learned on 2026-02-15.",
      "namespace": "'"$NAMESPACE"'",
      "topics": ["preference", "communication"],
      "entities": ["Alex Chen", "Acme Corp"],
      "memory_type": "semantic"
    }]
  }' | python3 -c "import sys,json; r=json.load(sys.stdin); print('[3/8] Stored: Alex Chen preferences' if 'status' not in r or r.get('status') != 'error' else f'[3/8] FAILED: {r}')" 2>&1

curl -s -X POST "$MEMORY_URL/" \
  -H "Content-Type: application/json" \
  -d '{
    "memories": [{
      "id": "demo-alex-action",
      "text": "Action item from 2026-02-15 meeting with Alex Chen: Marvin to prepare pricing options for expanded scope (mobile + web) by March 2026 renewal discussion.",
      "namespace": "'"$NAMESPACE"'",
      "topics": ["action-item", "pricing"],
      "entities": ["Alex Chen", "Acme Corp", "Marvin"],
      "memory_type": "semantic"
    }]
  }' | python3 -c "import sys,json; r=json.load(sys.stdin); print('[4/8] Stored: Alex Chen action item' if 'status' not in r or r.get('status') != 'error' else f'[4/8] FAILED: {r}')" 2>&1

# --- Sarah Mitchell / Horizon Ventures ---

curl -s -X POST "$MEMORY_URL/" \
  -H "Content-Type: application/json" \
  -d '{
    "memories": [{
      "id": "demo-sarah-profile",
      "text": "Sarah Mitchell (Partner, Horizon Ventures) led our $500K seed round in September 2025. She sits on our board. Quarterly check-ins scheduled. Sarah is focused on our path to $1M ARR and wants us to land 2 more enterprise clients before considering Series A.",
      "namespace": "'"$NAMESPACE"'",
      "topics": ["investor", "board", "fundraising"],
      "entities": ["Sarah Mitchell", "Horizon Ventures"],
      "memory_type": "semantic"
    }]
  }' | python3 -c "import sys,json; r=json.load(sys.stdin); print('[5/8] Stored: Sarah Mitchell profile' if 'status' not in r or r.get('status') != 'error' else f'[5/8] FAILED: {r}')" 2>&1

curl -s -X POST "$MEMORY_URL/" \
  -H "Content-Type: application/json" \
  -d '{
    "memories": [{
      "id": "demo-sarah-q4",
      "text": "Meeting with Sarah Mitchell (Horizon Ventures) on 2025-12-18: Q4 board meeting. Sarah was pleased with growth trajectory. Asked us to focus on net revenue retention as key metric. Wants to see case studies published before Series A conversations. Next board meeting April 15, 2026.",
      "namespace": "'"$NAMESPACE"'",
      "topics": ["board-meeting", "metrics", "series-a"],
      "entities": ["Sarah Mitchell", "Horizon Ventures"],
      "memory_type": "episodic",
      "event_date": "2025-12-18T14:00:00Z"
    }]
  }' | python3 -c "import sys,json; r=json.load(sys.stdin); print('[6/8] Stored: Sarah Mitchell Q4 board notes' if 'status' not in r or r.get('status') != 'error' else f'[6/8] FAILED: {r}')" 2>&1

# --- James Rodriguez / TechFlow ---

curl -s -X POST "$MEMORY_URL/" \
  -H "Content-Type: application/json" \
  -d '{
    "memories": [{
      "id": "demo-james-profile",
      "text": "James Rodriguez is CTO at TechFlow. TechFlow is building a developer-facing API management platform. They are fundraising for Series A. James values clean design handoffs and fast iteration. Engagement started February 2026 at $12K/month.",
      "namespace": "'"$NAMESPACE"'",
      "topics": ["client", "engagement"],
      "entities": ["James Rodriguez", "TechFlow"],
      "memory_type": "semantic"
    }]
  }' | python3 -c "import sys,json; r=json.load(sys.stdin); print('[7/8] Stored: James Rodriguez profile' if 'status' not in r or r.get('status') != 'error' else f'[7/8] FAILED: {r}')" 2>&1

curl -s -X POST "$MEMORY_URL/" \
  -H "Content-Type: application/json" \
  -d '{
    "memories": [{
      "id": "demo-james-phase1",
      "text": "Meeting with James Rodriguez (CTO, TechFlow) on 2026-03-10: Phase 1 design system handoff complete. James called it the best design handoff they have received. Phase 2 kicks off with developer portal — API playground is the hero feature. James wants dark mode as default. Action item: Marvin to send Phase 2 wireframes by March 28.",
      "namespace": "'"$NAMESPACE"'",
      "topics": ["meeting", "design-system", "handoff"],
      "entities": ["James Rodriguez", "TechFlow"],
      "memory_type": "episodic",
      "event_date": "2026-03-10T16:00:00Z"
    }]
  }' | python3 -c "import sys,json; r=json.load(sys.stdin); print('[8/8] Stored: James Rodriguez Phase 1 completion' if 'status' not in r or r.get('status') != 'error' else f'[8/8] FAILED: {r}')" 2>&1

echo ""
echo "Done! All 8 memories seeded."
echo ""
echo "Verify with:"
echo '  curl -s http://localhost:8000/v1/long-term-memory/search -H "Content-Type: application/json" -d '"'"'{"text": "Alex Chen Acme Corp", "namespace": {"eq": "chief-of-staff"}, "limit": 3}'"'"' | python3 -m json.tool'
