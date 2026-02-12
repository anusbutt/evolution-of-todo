---
id: 011
title: "Phase 14 Recurring Tasks Implementation"
stage: green
date: 2026-02-12
surface: agent
model: claude-opus-4-6
feature: recurring-tasks-us11
branch: master
user: developer
command: implement
labels: ["recurring-tasks", "US11", "phase-14", "backend", "frontend", "MCP"]
links:
  spec: specs/002-phase-02-web-app/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - phase-02/backend/alembic/versions/b4d7e8f9a2c3_add_recurrence_fields.py
  - phase-02/backend/app/models/task.py
  - phase-02/backend/mcp_server/models.py
  - phase-02/backend/app/schemas/task.py
  - phase-02/backend/app/services/task_service.py
  - phase-02/backend/mcp_server/tools.py
  - phase-02/backend/mcp_server/server_stdio.py
  - phase-02/backend/app/services/chat_service.py
  - phase-02/frontend/types/index.ts
  - phase-02/frontend/components/tasks/task-item.tsx
tests:
  - none (manual verification via chatbot pending)
---

## Prompt

Implement the following plan:

# Implement Recurring Tasks Feature (Phase 14, T110-T124)

## Context
User wants recurring tasks (daily/weekly/monthly). When a recurring task is completed, the system auto-creates a fresh copy with the next due date. SDD artifacts (spec US11, plan, tasks T110-T124) are already updated. This plan covers implementation.

**Deployed at:** Backend on HF Spaces, Frontend on Vercel, DB on Neon PostgreSQL.

---

[Full 12-step implementation plan for: migration, backend model, MCP model, schemas, recurrence logic, MCP tools, tool schemas, system prompt, frontend types, frontend UI, migration run, deploy & verify]

## Response snapshot

Implemented all 10 files for the recurring tasks feature (US11, Phase 14):

1. **Alembic migration** (`b4d7e8f9a2c3`): Adds `recurrence_pattern`, `recurrence_parent_id` (FK), `due_date` columns to `tasks` table with index.
2. **Backend Task model**: Added 3 nullable fields with FK constraint and index.
3. **MCP Task model**: Mirrored 3 fields (no FK, matching existing pattern).
4. **Pydantic schemas**: Added `recurrence_pattern` to TaskCreate/TaskUpdate with validators (daily/weekly/monthly), added 3 fields to TaskResponse.
5. **Task service**: Added `_calculate_next_due_date()` helper (handles monthly edge cases), `_create_next_recurring_task()` auto-creates next instance on completion, `create_task` sets initial due_date, `update_task_status` triggers recurrence.
6. **MCP tools**: `add_task` accepts `recurrence_pattern`, calculates initial `due_date`; `complete_task` auto-creates next recurring task with response; `list_tasks` includes recurrence info.
7. **MCP server schemas**: Added `recurrence_pattern` enum property to `add_task` tool schema; updated dispatch.
8. **System prompt**: Added recurring task instructions for the AI chatbot.
9. **Frontend types**: Added `recurrence_pattern`, `due_date`, `recurrence_parent_id` to Task/TaskResponse interfaces and `recurrence_pattern` to TaskCreatePayload.
10. **Frontend UI**: Added recurrence badge (Repeat icon + pattern) and due date display (Calendar icon) to task-item component.

## Outcome

- ✅ Impact: Full recurring tasks feature across backend, MCP server, and frontend
- 🧪 Tests: Manual verification needed — create recurring task via chatbot, complete it, verify auto-creation
- 📁 Files: 10 files modified/created
- 🔁 Next prompts: Run Alembic migration on Neon DB, deploy backend to HF Spaces, deploy frontend to Vercel, verify end-to-end
- 🧠 Reflection: Clean implementation following existing patterns. Monthly calculation handles edge cases (Feb 28/29). Recurrence triggers on completion only (no scheduler needed).

## Evaluation notes (flywheel)

- Failure modes observed: None during implementation
- Graders run and results (PASS/FAIL): N/A — manual verification pending
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Add recurrence dropdown to frontend task creation form for direct UI-based recurring task creation
