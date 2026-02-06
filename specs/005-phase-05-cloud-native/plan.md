# Implementation Plan: Phase 5 - Cloud Native Deployment

**Branch**: `005-phase-05-cloud-native` | **Date**: 2026-01-30 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/005-phase-05-cloud-native/spec.md`

---

## Summary

Deploy the Todo App to DigitalOcean Kubernetes Service (DOKS) with event-driven architecture using Redpanda Cloud (Kafka-compatible) and Dapr for microservices orchestration. Add intermediate features (Priorities, Tags, Search, Filter, Sort) and implement CI/CD via GitHub Actions. Using DigitalOcean $200 free credit (60 days) in Frankfurt (fra1).

---

## Technical Context

**Language/Version**: Python 3.13+ (Backend, Audit Service), TypeScript/Node 22+ (Frontend)
**Primary Dependencies**: FastAPI, Dapr SDK, SQLModel, Next.js 16, Tailwind CSS
**Cloud Platform**: DigitalOcean Kubernetes Service (DOKS) - $200 credit (60 days)
**Region**: Frankfurt (fra1)
**Event Streaming**: Redpanda Cloud (Kafka-compatible) - Serverless Free Tier
**Microservice Runtime**: Dapr 1.12+ (Pub/Sub, Secrets, Service Invocation)
**Container Registry**: DigitalOcean Container Registry (DOCR)
**Database**: Neon PostgreSQL (existing)
**Testing**: pytest (backend), Jest (frontend), Helm lint
**CI/CD**: GitHub Actions
**Target Platform**: DOKS (DigitalOcean Kubernetes - amd64 droplets)
**Performance Goals**: API <500ms p95, Event publishing <100ms
**Constraints**: 2 nodes × 2 vCPU, 2GB RAM ($24/month)
**Scale/Scope**: Single replica per service, resource-optimized

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Spec-Driven Development | ✅ PASS | Spec complete, plan follows spec |
| II. Single Source of Truth | ✅ PASS | Following hierarchy |
| III. AI-Native Development | ✅ PASS | Claude Code as agent, PHRs created |
| IV. Progressive Enhancement | ✅ PASS | Phase 4 complete, Phase 5 proceeds |
| V. Feature Scope Discipline | ✅ PASS | Intermediate features (P/T/S/F/S) - no advanced |
| VI. Technology Stack | ✅ PASS | DigitalOcean DOKS (constitution v1.6.0) |
| VII. Quality Standards | ✅ PASS | Type hints, async/await, error handling |

**Constitution Phase V Stack (v1.6.0):**
- ✅ Cloud Platform: DigitalOcean DOKS (constitution amended from OCI)
- ✅ Container Registry: DigitalOcean Container Registry (DOCR)
- ✅ Event Streaming: Redpanda (constitution: Kafka/Redpanda)
- ✅ Distributed Runtime: Dapr
- ✅ CI/CD: GitHub Actions
- ⚠️ Services: Audit Service only (Notification/Recurring deferred - user decision)

**Deviation Justification:**
- No Notification Service: User chose "in-app only" notifications
- No Recurring Task Service: Advanced features deferred to Phase 6
- No reminders topic: Not needed without notification service
- Cloud provider migration: OCI ARM64 capacity exhausted, free tier limited to 1 region

---

## Project Structure

### Documentation (this feature)

```text
specs/005-phase-05-cloud-native/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Phase 0: Research findings
├── data-model.md        # Phase 1: Entity models
├── quickstart.md        # Phase 1: Setup guide
├── contracts/           # Phase 1: API contracts
│   ├── task-api.yaml    # Updated Task API (OpenAPI)
│   ├── tag-api.yaml     # Tag API (OpenAPI)
│   ├── audit-api.yaml   # Audit API (OpenAPI)
│   └── events.yaml      # Event schemas
└── tasks.md             # Phase 2: Task breakdown
```

### Source Code (repository root)

```text
# Existing (from Phase 4)
frontend/                     # Next.js application
├── app/
│   └── (dashboard)/
│       └── tasks/
│           └── page.tsx      # MODIFIED: Add filter/search UI
├── components/
│   ├── tasks/
│   │   ├── TaskCard.tsx      # MODIFIED: Priority + Tags display
│   │   ├── TaskForm.tsx      # MODIFIED: Priority + Tags input
│   │   ├── TaskFilter.tsx    # NEW: Filter controls
│   │   └── TaskSearch.tsx    # NEW: Search input
│   └── ui/
│       ├── Tag.tsx           # NEW: Tag chip component
│       └── PriorityBadge.tsx # NEW: Priority indicator
├── services/
│   └── task-service.ts       # MODIFIED: New endpoints
└── types/
    └── task.ts               # MODIFIED: Priority, Tags types

backend/                      # FastAPI application
├── app/
│   ├── models/
│   │   ├── task.py           # MODIFIED: Add priority field
│   │   ├── tag.py            # NEW: Tag model
│   │   └── task_tag.py       # NEW: Junction table
│   ├── schemas/
│   │   ├── task.py           # MODIFIED: Priority, tags
│   │   ├── tag.py            # NEW: Tag schemas
│   │   └── event.py          # NEW: Event schemas
│   ├── routes/
│   │   ├── tasks.py          # MODIFIED: Search, filter, sort
│   │   └── tags.py           # NEW: Tag CRUD
│   ├── services/
│   │   └── event_publisher.py # NEW: Dapr pub/sub
│   └── events/
│       └── publisher.py      # NEW: Event publishing logic
└── alembic/
    └── versions/
        └── xxx_add_priority_tags.py # NEW: Migration

mcp-server/                   # MCP server (minimal changes)
└── tools/
    └── task_tools.py         # MODIFIED: Include priority/tags

# NEW for Phase 5
services/                     # NEW: Microservices directory
└── audit-service/
    ├── Dockerfile
    ├── requirements.txt
    ├── app/
    │   ├── __init__.py
    │   ├── main.py           # FastAPI + Dapr subscription
    │   ├── config.py
    │   ├── models/
    │   │   └── audit_log.py
    │   └── handlers/
    │       └── task_events.py
    └── dapr/
        └── subscription.yaml

deployment/
├── helm/
│   └── todo-app/
│       ├── values.yaml       # MODIFIED: Add audit-service
│       ├── values-prod.yaml  # NEW: Production overrides
│       └── templates/
│           ├── audit-service/
│           │   ├── deployment.yaml
│           │   └── service.yaml
│           └── dapr/
│               ├── pubsub-redpanda.yaml
│               └── secretstore-k8s.yaml
└── digitalocean/           # NEW: DOKS-specific configs
    └── cluster-config.md     # Documentation for DOKS setup

.github/
└── workflows/
    └── deploy.yml            # NEW: CI/CD pipeline
```

**Structure Decision**: Extending existing monorepo with new `services/` directory for microservices. Audit Service is the only new service for Phase 5 (others deferred).

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                  DIGITALOCEAN (Frankfurt - fra1)                            │
│                        Namespace: todo-app                                  │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        DAPR CONTROL PLANE                           │   │
│  │   ┌──────────┐  ┌──────────────┐  ┌──────────┐  ┌──────────┐       │   │
│  │   │ Operator │  │Sidecar Inject│  │Placement │  │ Sentry   │       │   │
│  │   └──────────┘  └──────────────┘  └──────────┘  └──────────┘       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │   Frontend   │  │   Backend    │  │  MCP Server  │  │Audit Service │   │
│  │   (Next.js)  │  │  (FastAPI)   │  │   (Python)   │  │  (FastAPI)   │   │
│  │              │  │              │  │              │  │              │   │
│  │ ┌──────────┐ │  │ ┌──────────┐ │  │ ┌──────────┐ │  │ ┌──────────┐ │   │
│  │ │   Dapr   │ │  │ │   Dapr   │ │  │ │   Dapr   │ │  │ │   Dapr   │ │   │
│  │ │ Sidecar  │ │  │ │ Sidecar  │ │  │ │ Sidecar  │ │  │ │ Sidecar  │ │   │
│  │ └──────────┘ │  │ └──────────┘ │  │ └──────────┘ │  │ └──────────┘ │   │
│  └──────┬───────┘  └──────┬───────┘  └──────────────┘  └──────┬───────┘   │
│         │                 │                                    │           │
│         │                 │ PUBLISH                 SUBSCRIBE  │           │
│         │                 ▼                                    │           │
│  ┌──────┴─────────────────────────────────────────────────────┴────────┐  │
│  │                        REDPANDA CLOUD                               │  │
│  │                     (Kafka-compatible)                              │  │
│  │                                                                     │  │
│  │   ┌─────────────────┐          ┌─────────────────┐                 │  │
│  │   │  task-events    │          │  task-updates   │                 │  │
│  │   │  (3 partitions) │          │  (reserved)     │                 │  │
│  │   └─────────────────┘          └─────────────────┘                 │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │                  DIGITALOCEAN LOAD BALANCER                         │  │
│  │                   http://<loadbalancer-ip>:3000                     │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          EXTERNAL SERVICES                                  │
│                                                                             │
│   ┌─────────────────┐         ┌─────────────────┐                          │
│   │ Neon PostgreSQL │         │   Gemini API    │                          │
│   │   (Database)    │         │  (AI/Chatbot)   │                          │
│   └─────────────────┘         └─────────────────┘                          │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Event Flow

```
┌────────┐    ┌────────┐    ┌─────────────┐    ┌──────────────┐    ┌─────────┐
│  User  │───►│Frontend│───►│   Backend   │───►│   Redpanda   │───►│  Audit  │
│        │    │        │    │   (Dapr)    │    │ task-events  │    │ Service │
│        │    │        │    │             │    │              │    │         │
│ Create │    │  POST  │    │  1. Save DB │    │  2. Store    │    │ 3. Log  │
│ Task   │    │ /tasks │    │  2. Publish │    │     Event    │    │    to   │
│        │    │        │    │     Event   │    │              │    │    DB   │
└────────┘    └────────┘    └─────────────┘    └──────────────┘    └─────────┘
```

---

## Component Design

### 1. Backend Event Publishing

```python
# backend/app/events/publisher.py
from dapr.clients import DaprClient
from app.schemas.event import TaskEvent
import json
import uuid
from datetime import datetime

PUBSUB_NAME = "task-pubsub"
TOPIC_NAME = "task-events"

class EventPublisher:
    @staticmethod
    async def publish_task_event(
        event_type: str,
        user_id: int,
        task_id: int,
        task_data: dict = None
    ):
        event = TaskEvent(
            event_id=f"evt_{uuid.uuid4().hex[:12]}",
            event_type=event_type,
            timestamp=datetime.utcnow().isoformat(),
            user_id=user_id,
            task_id=task_id,
            task_data=task_data
        )

        with DaprClient() as client:
            client.publish_event(
                pubsub_name=PUBSUB_NAME,
                topic_name=TOPIC_NAME,
                data=event.model_dump_json(),
                data_content_type='application/json'
            )
```

### 2. Audit Service Subscription

```python
# services/audit-service/app/main.py
from fastapi import FastAPI
from dapr.ext.fastapi import DaprApp
from app.models.audit_log import AuditLog
from app.config import get_db

app = FastAPI(title="Audit Service")
dapr_app = DaprApp(app)

@dapr_app.subscribe(pubsub='task-pubsub', topic='task-events')
async def handle_task_event(event: dict):
    """Subscribe to task events and log them."""
    db = await get_db()

    log = AuditLog(
        event_id=event['event_id'],
        event_type=event['event_type'],
        user_id=event['user_id'],
        task_id=event['task_id'],
        data=event.get('task_data'),
        timestamp=event['timestamp']
    )

    await db.execute(
        """INSERT INTO audit_log (event_id, event_type, user_id, task_id, data, timestamp)
           VALUES ($1, $2, $3, $4, $5, $6)""",
        log.event_id, log.event_type, log.user_id, log.task_id,
        json.dumps(log.data), log.timestamp
    )

    return {"status": "ok"}
```

### 3. Priority & Tags Implementation

```python
# backend/app/models/task.py (updated)
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
from typing import Optional, List

class Priority(str, Enum):
    P1 = "P1"  # High
    P2 = "P2"  # Medium
    P3 = "P3"  # Low

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    title: str = Field(max_length=200)
    description: Optional[str] = None
    completed: bool = Field(default=False)
    priority: Priority = Field(default=Priority.P2)  # NEW
    created_at: datetime
    updated_at: datetime

    # Relationships
    tags: List["Tag"] = Relationship(back_populates="tasks", link_model=TaskTag)
```

### 4. Search & Filter Endpoints

```python
# backend/app/routes/tasks.py (new endpoints)
from fastapi import APIRouter, Query
from typing import Optional, List

@router.get("/search")
async def search_tasks(
    q: str = Query(..., min_length=2),
    user: User = Depends(get_current_user)
):
    """Full-text search on title and description."""
    return await task_service.search(user.id, q)

@router.get("/filter")
async def filter_tasks(
    completed: Optional[bool] = None,
    priority: Optional[Priority] = None,
    tags: Optional[str] = Query(None, description="Comma-separated tag names"),
    sort_by: str = Query("created_at", enum=["created_at", "priority", "title"]),
    sort_order: str = Query("desc", enum=["asc", "desc"]),
    user: User = Depends(get_current_user)
):
    """Filter and sort tasks."""
    tag_list = tags.split(",") if tags else None
    return await task_service.filter(
        user.id, completed, priority, tag_list, sort_by, sort_order
    )
```

---

## Dapr Configuration

### Pub/Sub Component (Redpanda)

```yaml
# deployment/helm/todo-app/templates/dapr/pubsub-redpanda.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: task-pubsub
  namespace: todo-app
spec:
  type: pubsub.kafka
  version: v1
  metadata:
    - name: brokers
      secretKeyRef:
        name: redpanda-secrets
        key: brokers
    - name: authType
      value: "password"
    - name: saslUsername
      secretKeyRef:
        name: redpanda-secrets
        key: username
    - name: saslPassword
      secretKeyRef:
        name: redpanda-secrets
        key: password
    - name: saslMechanism
      value: "SCRAM-SHA-256"
    - name: initialOffset
      value: "oldest"
    - name: consumerGroup
      value: "todo-app"
```

### Secret Store Component

```yaml
# deployment/helm/todo-app/templates/dapr/secretstore-k8s.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kubernetes-secrets
  namespace: todo-app
spec:
  type: secretstores.kubernetes
  version: v1
```

---

## CI/CD Pipeline Design

```yaml
# .github/workflows/deploy.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Backend tests
        run: cd backend && pip install -r requirements.txt && pytest
      - name: Frontend tests
        run: cd frontend && npm ci && npm test

  build-and-deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      - name: Login to DOCR
        run: |
          doctl registry login --access-token ${{ secrets.DIGITALOCEAN_ACCESS_TOKEN }}
      - name: Build and push images
        run: |
          REPO="registry.digitalocean.com/todo-app"
          docker build -t ${REPO}/frontend:latest ./frontend
          docker build -t ${REPO}/backend:latest ./backend
          docker build -t ${REPO}/mcp-server:latest ./mcp-server
          docker push ${REPO}/frontend:latest
          docker push ${REPO}/backend:latest
          docker push ${REPO}/mcp-server:latest
      - name: Deploy to DOKS
        run: |
          doctl kubernetes cluster kubeconfig save todo-app-cluster --access-token ${{ secrets.DIGITALOCEAN_ACCESS_TOKEN }}
          helm upgrade --install todo-app ./deployment/helm/todo-app -f ./deployment/helm/todo-app/values-prod.yaml -n todo-app
```

---

## Database Migrations

### Migration: Add Priority and Tags

```python
# alembic/versions/xxx_add_priority_tags.py
def upgrade():
    # Add priority to task
    op.add_column('task', sa.Column('priority', sa.String(2), default='P2'))
    op.create_check_constraint('ck_task_priority', 'task', "priority IN ('P1', 'P2', 'P3')")

    # Create tag table
    op.create_table('tag',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), unique=True, nullable=False),
        sa.Column('color', sa.String(7), default='#808080'),
        sa.Column('created_at', sa.DateTime, default=sa.func.now())
    )

    # Create task_tag junction table
    op.create_table('task_tag',
        sa.Column('task_id', sa.Integer, sa.ForeignKey('task.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('tag_id', sa.Integer, sa.ForeignKey('tag.id', ondelete='CASCADE'), primary_key=True)
    )

    # Create audit_log table
    op.create_table('audit_log',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('event_id', sa.String(50), unique=True, nullable=False),
        sa.Column('event_type', sa.String(20), nullable=False),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('task_id', sa.Integer),
        sa.Column('data', sa.JSON),
        sa.Column('timestamp', sa.DateTime, nullable=False),
        sa.Column('created_at', sa.DateTime, default=sa.func.now())
    )

    # Insert default tags
    op.execute("""
        INSERT INTO tag (name, color) VALUES
        ('Work', '#3B82F6'),
        ('Personal', '#10B981'),
        ('Shopping', '#F59E0B'),
        ('Health', '#EF4444'),
        ('Finance', '#8B5CF6')
    """)

def downgrade():
    op.drop_table('audit_log')
    op.drop_table('task_tag')
    op.drop_table('tag')
    op.drop_constraint('ck_task_priority', 'task')
    op.drop_column('task', 'priority')
```

---

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Dapr sidecars | Event-driven architecture requirement | Direct Kafka clients would couple services to Kafka SDK |
| Separate Audit Service | Constitution requires event consumers | Could log in backend, but violates microservices principle |
| DigitalOcean DOKS | Cloud Kubernetes required by hackathon | OCI capacity exhausted; DO provides reliable provisioning with $200 credit |

---

## Risk Mitigations

| Risk | Mitigation |
|------|------------|
| Credit exhaustion ($200) | ~$36/month = ~5 months; monitor via DO dashboard |
| Redpanda connection issues | Implement retry with exponential backoff |
| Node resource limits (2GB/node) | Optimize resource requests, right-size pods |
| DOCR storage limits (500MB free) | Use multi-stage builds, prune unused images |

---

## Phase Outputs

- **Phase 0**: `research.md` - Technology decisions documented
- **Phase 1**: `data-model.md`, `contracts/`, `quickstart.md` - Design artifacts
- **Phase 2**: `tasks.md` - Task breakdown (via `/sp.tasks`)
