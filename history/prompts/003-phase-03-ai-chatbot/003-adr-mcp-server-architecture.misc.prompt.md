---
id: 003
title: ADR MCP Server Architecture
stage: misc
date: 2026-01-16
surface: agent
model: claude-opus-4.5
feature: 003-phase-03-ai-chatbot
branch: 003-phase-03-ai-chatbot
user: architect
command: /sp.adr
labels: ["phase-3", "ai-chatbot", "mcp", "architecture", "adr"]
links:
  spec: specs/003-phase-03-ai-chatbot/spec.md
  ticket: null
  adr: history/adr/006-mcp-server-architecture.md
  pr: null
files:
  - history/adr/006-mcp-server-architecture.md
tests:
  - N/A (documentation)
---

## Prompt

/sp.adr

## Response snapshot

Created ADR-006: MCP Server Architecture documenting the decision to deploy MCP as a separate service:

**Decision**: Deploy MCP Server as independent service on port 5001 with HTTP/SSE transport

**Key Points**:
- Constitution compliance (Phase III mandate)
- Independent scaling capability
- Fault isolation from main backend
- Phase 4 containerization ready
- Shared PostgreSQL database

**Alternatives Rejected**:
1. Embedded MCP in Backend - Violates constitution, tight coupling
2. stdio Transport - Not a separate service, subprocess management issues
3. Separate Database - Overkill complexity for current scale

**Architecture**:
```
Frontend (3000) → Backend (8000) → MCP Server (5001) → PostgreSQL
```

## Outcome

- ✅ Impact: ADR-006 created documenting MCP architecture decision
- 🧪 Tests: N/A - documentation artifact
- 📁 Files: 1 file created (ADR-006)
- 🔁 Next prompts: /sp.tasks to generate task breakdown
- 🧠 Reflection: ADR captures rationale for separate service architecture, enabling future reference

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Significance check PASS (Impact, Alternatives, Scope all true)
- Prompt variant (if applicable): Standard /sp.adr flow
- Next experiment (smallest change to try): N/A - proceeding to tasks
