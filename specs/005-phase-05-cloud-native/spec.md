# Specification: Phase 5 - Cloud Native Deployment

**Feature**: 005-phase-05-cloud-native
**Version**: 1.0.0
**Date**: 2026-01-30
**Status**: Draft

---

## 1. Overview

### 1.1 Purpose

Transform the Todo App from local Kubernetes (Minikube) to a production-ready cloud-native architecture on DigitalOcean Kubernetes Service (DOKS) with event-driven messaging via Redpanda Cloud and microservices orchestration using Dapr.

### 1.2 Scope

**In Scope:**
- DigitalOcean Kubernetes Service (DOKS) deployment (Frankfurt - fra1)
- DigitalOcean Container Registry (DOCR) for container images
- Redpanda Cloud for event streaming (Kafka-compatible)
- Dapr for microservices building blocks
- Audit Service for event logging
- Intermediate features: Priorities, Tags, Search, Filter, Sort
- GitHub Actions CI/CD pipeline
- $200 free credit (60 days) - sufficient for hackathon duration

**Out of Scope:**
- Advanced features (Due Dates, Reminders, Recurring Tasks) - deferred to Phase 6
- Notification Service - not needed without reminders
- Recurring Task Service - not needed without recurring tasks
- Custom domain / TLS certificates (beyond DigitalOcean defaults)
- Resources beyond $200 credit budget

### 1.3 Success Criteria

| Criteria | Measurement |
|----------|-------------|
| App deployed to DOKS | All pods running, accessible via Load Balancer URL |
| Events flowing through Redpanda | task-events topic receiving messages |
| Audit Service logging events | All CRUD operations logged |
| Dapr sidecars operational | Pub/Sub, State, Secrets working |
| CI/CD pipeline functional | Push to main triggers full deployment |
| Intermediate features working | Priorities, Tags, Search, Filter, Sort functional |
| Budget compliance | Within $200 credit budget |

---

## 2. Architecture

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DIGITALOCEAN (Frankfurt - fra1)                          │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │              DIGITALOCEAN KUBERNETES SERVICE (DOKS)                    │  │
│  │                    Cluster: todo-app-cluster                          │  │
│  │                                                                       │  │
│  │   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                  │  │
│  │   │  Frontend   │  │   Backend   │  │ MCP Server  │                  │  │
│  │   │  (Next.js)  │  │  (FastAPI)  │  │  (Python)   │                  │  │
│  │   │             │  │             │  │             │                  │  │
│  │   │ ┌─────────┐ │  │ ┌─────────┐ │  │ ┌─────────┐ │                  │  │
│  │   │ │  Dapr   │ │  │ │  Dapr   │ │  │ │  Dapr   │ │                  │  │
│  │   │ │ Sidecar │ │  │ │ Sidecar │ │  │ │ Sidecar │ │                  │  │
│  │   │ └─────────┘ │  │ └─────────┘ │  │ └─────────┘ │                  │  │
│  │   └──────┬──────┘  └──────┬──────┘  └─────────────┘                  │  │
│  │          │                │                                           │  │
│  │          │                │ Publish Events                            │  │
│  │          │                ▼                                           │  │
│  │          │    ┌───────────────────────┐                              │  │
│  │          │    │   DAPR CONTROL PLANE  │                              │  │
│  │          │    │  (Pub/Sub, State,     │                              │  │
│  │          │    │   Secrets, Invoke)    │                              │  │
│  │          │    └───────────┬───────────┘                              │  │
│  │          │                │                                           │  │
│  │          │                ▼                                           │  │
│  │   ┌──────┴────────────────────────────────────────────────────────┐  │  │
│  │   │                    REDPANDA CLOUD                              │  │  │
│  │   │                  (Kafka-compatible)                            │  │  │
│  │   │                                                                │  │  │
│  │   │    ┌──────────────┐        ┌──────────────┐                   │  │  │
│  │   │    │ task-events  │        │ task-updates │                   │  │  │
│  │   │    │    topic     │        │    topic     │                   │  │  │
│  │   │    └──────┬───────┘        └──────────────┘                   │  │  │
│  │   └───────────┼───────────────────────────────────────────────────┘  │  │
│  │               │                                                       │  │
│  │               ▼                                                       │  │
│  │   ┌─────────────────┐                                                │  │
│  │   │  Audit Service  │                                                │  │
│  │   │   (FastAPI)     │                                                │  │
│  │   │                 │                                                │  │
│  │   │ ┌─────────────┐ │                                                │  │
│  │   │ │ Dapr Sidecar│ │                                                │  │
│  │   │ └─────────────┘ │                                                │  │
│  │   └─────────────────┘                                                │  │
│  │                                                                       │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                        NEON POSTGRESQL                                │  │
│  │                    (External - Serverless DB)                         │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                           GITHUB ACTIONS                                    │
│                                                                             │
│   [Push] → [Test] → [Build Images] → [Push to DOCR] → [Deploy to DOKS]    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Component Overview

| Component | Technology | Purpose |
|-----------|------------|---------|
| Cloud Platform | DigitalOcean DOKS (Frankfurt) | Managed Kubernetes ($200 credit) |
| Event Streaming | Redpanda Cloud | Kafka-compatible messaging |
| Microservice Runtime | Dapr | Pub/Sub, State, Secrets, Service Invocation |
| Container Registry | DigitalOcean Container Registry (DOCR) | Managed image storage |
| CI/CD | GitHub Actions | Automated deployment pipeline |
| Database | Neon PostgreSQL | Serverless PostgreSQL (existing) |
| Audit Service | FastAPI + Dapr | Event logging microservice |

### 2.3 Event Flow

```
┌────────────┐     ┌────────────┐     ┌─────────────┐     ┌──────────────┐
│   User     │────►│  Backend   │────►│  Redpanda   │────►│Audit Service │
│  Action    │     │   API      │     │ task-events │     │              │
│            │     │            │     │             │     │  Logs to DB  │
│ - Create   │     │ Publishes  │     │  Stores &   │     │              │
│ - Update   │     │  Event     │     │  Delivers   │     │              │
│ - Delete   │     │            │     │             │     │              │
│ - Complete │     │            │     │             │     │              │
└────────────┘     └────────────┘     └─────────────┘     └──────────────┘
```

---

## 3. User Stories

### US1: Cloud Deployment (P1)
**As a** developer
**I want** the app deployed to DigitalOcean Kubernetes (DOKS)
**So that** it's accessible on the internet with production-grade infrastructure

**Acceptance Criteria:**
- [ ] DOKS cluster created in Frankfurt (fra1)
- [ ] All pods (frontend, backend, mcp-server, audit-service) running
- [ ] App accessible via DigitalOcean Load Balancer URL
- [ ] Health checks passing for all services

### US2: Event-Driven Architecture (P1)
**As a** system
**I want** task operations to publish events
**So that** services can react to changes asynchronously

**Acceptance Criteria:**
- [ ] Redpanda Cloud cluster created (free tier)
- [ ] `task-events` topic created
- [ ] Backend publishes events on create/update/delete/complete
- [ ] Events contain: event_id, event_type, user_id, task_id, task_data, timestamp
- [ ] Dapr Pub/Sub component configured for Redpanda

### US3: Audit Logging (P1)
**As an** administrator
**I want** all task operations logged
**So that** I can track user activity and debug issues

**Acceptance Criteria:**
- [ ] Audit Service deployed and subscribed to `task-events`
- [ ] All events persisted to `audit_log` table
- [ ] Logs include: event_id, event_type, user_id, task_id, data, timestamp
- [ ] GET /api/audit endpoint returns recent logs (admin only)

### US4: Task Priorities (P2)
**As a** user
**I want** to assign priorities to tasks
**So that** I can focus on what's most important

**Acceptance Criteria:**
- [ ] Task model has `priority` field (P1=High, P2=Medium, P3=Low)
- [ ] Default priority is P2 (Medium)
- [ ] UI shows priority indicator (color-coded)
- [ ] Can change priority when creating or editing task
- [ ] Priority included in task-events

### US5: Task Tags (P2)
**As a** user
**I want** to add tags to tasks
**So that** I can categorize and organize them

**Acceptance Criteria:**
- [ ] Tag model created (id, name, color)
- [ ] Many-to-many relationship between Task and Tag
- [ ] Can add/remove tags when creating or editing task
- [ ] UI shows tags as colored chips
- [ ] Pre-defined tags: Work, Personal, Shopping, Health, Finance

### US6: Search Tasks (P2)
**As a** user
**I want** to search my tasks
**So that** I can quickly find specific items

**Acceptance Criteria:**
- [ ] GET /api/tasks/search?q={query} endpoint
- [ ] Searches title and description (case-insensitive)
- [ ] Returns matching tasks ordered by relevance
- [ ] UI search input with debounced query
- [ ] Minimum 2 characters to trigger search

### US7: Filter Tasks (P2)
**As a** user
**I want** to filter my tasks
**So that** I can view specific subsets

**Acceptance Criteria:**
- [ ] GET /api/tasks/filter endpoint with query params
- [ ] Filter by: completed (true/false), priority (P1/P2/P3), tags (comma-separated)
- [ ] Multiple filters can be combined (AND logic)
- [ ] UI filter controls (dropdowns, checkboxes)
- [ ] Filter state persisted in URL query params

### US8: Sort Tasks (P2)
**As a** user
**I want** to sort my tasks
**So that** I can view them in my preferred order

**Acceptance Criteria:**
- [ ] Sort options: created_at, priority, title
- [ ] Sort direction: ascending, descending
- [ ] Default: created_at descending (newest first)
- [ ] UI sort dropdown with direction toggle
- [ ] Sort state persisted in URL query params

### US9: CI/CD Pipeline (P1)
**As a** developer
**I want** automated deployments
**So that** code changes are tested and deployed automatically

**Acceptance Criteria:**
- [ ] GitHub Actions workflow triggers on push to main
- [ ] Pipeline stages: test → build → push → deploy → smoke-test
- [ ] All services built and pushed to DigitalOcean Container Registry (DOCR)
- [ ] `kubectl apply` or Helm upgrade deploys new versions
- [ ] Failed tests block deployment
- [ ] Slack/email notification on failure (optional)

---

## 4. Technical Requirements

### 4.1 DigitalOcean Cloud Platform

#### 4.1.1 DOKS Cluster Specification

| Resource | Specification |
|----------|---------------|
| Platform | DigitalOcean Kubernetes Service (DOKS) |
| Kubernetes Version | v1.31+ (latest stable) |
| Region | Frankfurt (fra1) |
| Namespace | todo-app |
| Node Pool | 2× Basic Droplets (s-2vcpu-2gb, $12/month each) |
| Architecture | amd64 (standard x86_64) |
| Duration | $200 credit for 60 days (~3 months hackathon) |
| Network | VPC (auto-managed by DigitalOcean) |
| Ingress | DigitalOcean Load Balancer ($12/month) |

#### 4.1.2 Container Registry (DOCR)

| Setting | Value |
|---------|-------|
| Registry | DigitalOcean Container Registry (DOCR) |
| Tier | Starter (free, 500MB storage) or Basic ($5/month, 5GB) |
| Access | doctl registry login (API token auth) |
| Images | todo-app/frontend, todo-app/backend, todo-app/mcp-server, todo-app/audit-service |

### 4.2 Redpanda Cloud

#### 4.2.1 Cluster Specification

| Resource | Specification |
|----------|---------------|
| Tier | Serverless (free tier) |
| Cloud Provider | Any (Redpanda is global) |
| Topics | task-events, task-updates |
| Partitions | 3 per topic |
| Retention | 7 days |
| Max Message Size | 1 MB |

#### 4.2.2 Topics

| Topic | Purpose | Producers | Consumers |
|-------|---------|-----------|-----------|
| task-events | Task CRUD operations | Backend | Audit Service |
| task-updates | Real-time sync (future) | Backend | (Reserved for WebSocket gateway) |

#### 4.2.3 Event Schema

```json
{
  "event_id": "evt_abc123def456",
  "event_type": "created | updated | deleted | completed",
  "timestamp": "2026-01-30T10:30:00Z",
  "user_id": 123,
  "task_id": 456,
  "task_data": {
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "priority": "P2",
    "tags": ["Shopping", "Personal"]
  }
}
```

### 4.3 Dapr Configuration

#### 4.3.1 Building Blocks Required

| Block | Purpose | Component |
|-------|---------|-----------|
| Pub/Sub | Event messaging | Redpanda |
| State Store | Distributed state (optional) | Redis / PostgreSQL |
| Secrets | Credential management | Kubernetes Secrets |
| Service Invocation | Service-to-service calls | Built-in |

#### 4.3.2 Dapr Components

**Pub/Sub Component:**
```yaml
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
```

**Secrets Component:**
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kubernetes-secrets
  namespace: todo-app
spec:
  type: secretstores.kubernetes
  version: v1
```

### 4.4 Database Schema Changes

#### 4.4.1 New Tables

**Tag Table:**
```sql
CREATE TABLE tag (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    color VARCHAR(7) DEFAULT '#808080',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Pre-populate default tags
INSERT INTO tag (name, color) VALUES
    ('Work', '#3B82F6'),
    ('Personal', '#10B981'),
    ('Shopping', '#F59E0B'),
    ('Health', '#EF4444'),
    ('Finance', '#8B5CF6');
```

**Task-Tag Junction Table:**
```sql
CREATE TABLE task_tag (
    task_id INTEGER REFERENCES task(id) ON DELETE CASCADE,
    tag_id INTEGER REFERENCES tag(id) ON DELETE CASCADE,
    PRIMARY KEY (task_id, tag_id)
);
```

**Audit Log Table:**
```sql
CREATE TABLE audit_log (
    id SERIAL PRIMARY KEY,
    event_id VARCHAR(50) UNIQUE NOT NULL,
    event_type VARCHAR(20) NOT NULL,
    user_id INTEGER NOT NULL,
    task_id INTEGER,
    data JSONB,
    timestamp TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_log_user_id ON audit_log(user_id);
CREATE INDEX idx_audit_log_timestamp ON audit_log(timestamp DESC);
CREATE INDEX idx_audit_log_event_type ON audit_log(event_type);
```

#### 4.4.2 Task Table Modifications

```sql
-- Add priority column
ALTER TABLE task ADD COLUMN priority VARCHAR(2) DEFAULT 'P2'
    CHECK (priority IN ('P1', 'P2', 'P3'));

-- Add index for priority filtering
CREATE INDEX idx_task_priority ON task(user_id, priority);
```

### 4.5 API Endpoints

#### 4.5.1 New/Modified Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/tasks/search?q={query} | Search tasks |
| GET | /api/tasks/filter | Filter tasks with query params |
| GET | /api/tags | List all tags |
| POST | /api/tags | Create new tag |
| DELETE | /api/tags/{id} | Delete tag |
| GET | /api/audit | List audit logs (admin) |

#### 4.5.2 Modified Task Endpoints

**Create Task (POST /api/tasks):**
```json
// Request
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "priority": "P1",
  "tag_ids": [1, 3]
}

// Response
{
  "id": 123,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "priority": "P1",
  "tags": [
    {"id": 1, "name": "Work", "color": "#3B82F6"},
    {"id": 3, "name": "Shopping", "color": "#F59E0B"}
  ],
  "created_at": "2026-01-30T10:00:00Z",
  "updated_at": "2026-01-30T10:00:00Z"
}
```

**Filter Tasks (GET /api/tasks/filter):**
```
GET /api/tasks/filter?completed=false&priority=P1&tags=Work,Shopping&sort=priority&order=asc
```

### 4.6 CI/CD Pipeline

#### 4.6.1 GitHub Actions Workflow

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│  Push   │────►│  Test   │────►│  Build  │────►│  Push   │────►│ Deploy  │
│ to main │     │ pytest  │     │ Docker  │     │ to DOCR │     │ to DOKS │
│         │     │ eslint  │     │ amd64   │     │         │     │ Helm    │
└─────────┘     └─────────┘     └─────────┘     └─────────┘     └─────────┘
                     │
                     │ Fail
                     ▼
                ┌─────────┐
                │  Stop   │
                │ Notify  │
                └─────────┘
```

#### 4.6.2 Required Secrets

| Secret | Description |
|--------|-------------|
| DIGITALOCEAN_ACCESS_TOKEN | DigitalOcean API token (read/write) |
| DOCR_REGISTRY | DOCR registry endpoint (registry.digitalocean.com) |
| KUBECONFIG | DOKS cluster kubeconfig (base64 encoded) |
| REDPANDA_BROKERS | Redpanda bootstrap servers |
| REDPANDA_USERNAME | SASL username |
| REDPANDA_PASSWORD | SASL password |

---

## 5. UI Changes

### 5.1 Task Card Updates

```
┌─────────────────────────────────────────────────────────────────┐
│ ┌───┐                                                           │
│ │ ○ │  Buy groceries                              [P1] ●        │
│ └───┘                                                           │
│       Milk, eggs, bread                                         │
│                                                                 │
│       ┌──────────┐ ┌────────────┐ ┌──────────┐                 │
│       │ Shopping │ │  Personal  │ │  Health  │                 │
│       └──────────┘ └────────────┘ └──────────┘                 │
│                                                                 │
│       Created: Jan 30, 2026                    [Edit] [Delete] │
└─────────────────────────────────────────────────────────────────┘

Priority Indicator:
● P1 (High)   = Red
● P2 (Medium) = Yellow
● P3 (Low)    = Green
```

### 5.2 Filter Bar

```
┌─────────────────────────────────────────────────────────────────┐
│  🔍 Search tasks...                                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Status: [All ▼]    Priority: [All ▼]    Sort: [Newest ▼]     │
│                                                                 │
│  Tags: [Work] [Personal] [Shopping] [Health] [Finance]         │
│         ✓       ✓                                              │
└─────────────────────────────────────────────────────────────────┘
```

### 5.3 Task Form Updates

```
┌─────────────────────────────────────────────────────────────────┐
│                        Add New Task                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Title *                                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Buy groceries                                            │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Description                                                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Milk, eggs, bread                                        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Priority                                                       │
│  ○ P1 (High)   ● P2 (Medium)   ○ P3 (Low)                     │
│                                                                 │
│  Tags                                                           │
│  [✓ Shopping] [  Work  ] [  Personal  ] [  Health  ]          │
│                                                                 │
│                              [Cancel]  [Save Task]             │
└─────────────────────────────────────────────────────────────────┘
```

---

## 6. Non-Functional Requirements

### 6.1 Performance

| Metric | Target |
|--------|--------|
| API Response Time (p95) | < 500ms |
| Event Publishing Latency | < 100ms |
| Search Query Time | < 200ms |
| Page Load Time | < 3s |

### 6.2 Reliability

| Metric | Target |
|--------|--------|
| Uptime | 99% (free tier limitation) |
| Event Delivery | At-least-once |
| Data Durability | 99.9% (Neon guarantee) |

### 6.3 Scalability

| Component | Limit |
|-----------|-------|
| DOKS Nodes | 2 (s-2vcpu-2gb droplets) |
| Pod Replicas | 1 per service |
| Redpanda Storage | 5 GB |
| Redpanda Throughput | 1 MB/s |

### 6.4 Security

- All secrets stored in Kubernetes Secrets
- Redpanda connection uses SASL/SCRAM authentication
- DigitalOcean API token with scoped access
- No sensitive data in logs or events

---

## 7. Constraints

### 7.1 DigitalOcean Budget Constraints

| Service | Cost | Impact |
|---------|------|--------|
| DOKS Control Plane | Free | Managed by DigitalOcean |
| Worker Nodes (2×) | $24/month | 2 vCPU, 2GB RAM each |
| Load Balancer | $12/month | Single entry point |
| DOCR (Starter) | Free | 500MB image storage |
| Total Monthly | ~$36/month | ~5 months on $200 credit |
| Redpanda | Free tier | 5 GB storage, 1 MB/s |
| Neon | Free tier | 0.5 GB storage, 1 compute |

### 7.2 Technical Constraints

- No custom domain (use Load Balancer IPs)
- Single replica per service (resource optimization)
- amd64 architecture (standard x86_64 droplets)
- $200 credit budget (sufficient for hackathon)

---

## 8. Dependencies

### 8.1 External Services

| Service | Purpose | Account Required |
|---------|---------|------------------|
| DigitalOcean | DOKS, DOCR, Load Balancer | Yes ($200 credit, card required) |
| Redpanda Cloud | Kafka messaging | Yes (free tier) |
| Neon | PostgreSQL database | Yes (existing) |
| GitHub | Source code, Actions | Yes (existing) |
| Google AI | Gemini API | Yes (existing key) |

### 8.2 Internal Dependencies

| Dependency | Required By |
|------------|-------------|
| Phase 4 Helm Chart | Base for Phase 5 deployment |
| Backend API | Event publishing |
| Database migrations | New tables (tag, task_tag, audit_log) |

---

## 9. Risks & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| $200 credit exhaustion | Services stop | Low | ~$36/month = ~5 months coverage |
| Redpanda Cloud outage | Events not delivered | Low | Implement retry logic, fallback |
| Node resource limits | Pod scheduling fails | Medium | Optimize resource requests, right-size |
| DigitalOcean outage | Services unavailable | Low | Frankfurt region is well-provisioned |
| Database connection limits | Service failures | Medium | Connection pooling |

---

## 10. Acceptance Scenarios

### Scenario 1: Cloud Deployment
```gherkin
Given the Phase 5 infrastructure is configured
When I run the CI/CD pipeline
Then all services are deployed to DOKS
And I can access the app via the DigitalOcean Load Balancer URL
And all health checks pass
```

### Scenario 2: Event Publishing
```gherkin
Given I am logged in
When I create a new task with title "Test Event"
Then an event is published to Redpanda
And the event contains event_type "created"
And the Audit Service logs the event
```

### Scenario 3: Task Priorities
```gherkin
Given I am on the task creation form
When I select priority "P1 (High)"
And I save the task
Then the task is displayed with a red priority indicator
And I can filter tasks by P1 priority
```

### Scenario 4: Task Tags
```gherkin
Given I am editing a task
When I add tags "Work" and "Shopping"
And I save the task
Then the task displays both tags as colored chips
And I can filter tasks by the "Work" tag
```

### Scenario 5: Search
```gherkin
Given I have tasks with titles "Buy milk" and "Buy bread"
When I search for "Buy"
Then both tasks appear in the results
And tasks not matching "Buy" are hidden
```

### Scenario 6: Filter and Sort
```gherkin
Given I have tasks with different priorities and completion status
When I filter by "completed=false" and "priority=P1"
And I sort by "title ascending"
Then only incomplete P1 tasks are shown
And they are sorted alphabetically by title
```

---

## 11. Glossary

| Term | Definition |
|------|------------|
| DOKS | DigitalOcean Kubernetes Service (managed Kubernetes) |
| DOCR | DigitalOcean Container Registry (managed image storage) |
| Droplet | DigitalOcean virtual machine (worker node) |
| doctl | DigitalOcean CLI tool |
| Redpanda | Kafka-compatible event streaming platform |
| Dapr | Distributed Application Runtime - microservices building blocks |
| Pub/Sub | Publish/Subscribe messaging pattern |

---

## 12. References

- [DigitalOcean Kubernetes (DOKS)](https://docs.digitalocean.com/products/kubernetes/)
- [DigitalOcean Container Registry (DOCR)](https://docs.digitalocean.com/products/container-registry/)
- [doctl CLI Reference](https://docs.digitalocean.com/reference/doctl/)
- [Redpanda Cloud Documentation](https://docs.redpanda.com/current/deploy/deployment-option/cloud/)
- [Dapr Documentation](https://docs.dapr.io/)
- [Constitution](../../.specify/memory/constitution.md) - Phase V requirements

---

## Appendix A: Project Structure (Phase 5)

```
hackathon_II/
├── frontend/                      # Next.js frontend (updated)
├── backend/                       # FastAPI backend (updated)
├── mcp-server/                    # MCP server (unchanged)
│
├── services/                      # NEW: Microservices
│   └── audit-service/
│       ├── Dockerfile
│       ├── requirements.txt
│       └── app/
│           ├── __init__.py
│           ├── main.py
│           ├── config.py
│           └── handlers/
│               └── task_events.py
│
├── deployment/
│   ├── helm/
│   │   └── todo-app/
│   │       ├── values.yaml
│   │       ├── values-prod.yaml   # NEW: Production values
│   │       └── templates/
│   │           ├── audit-service/ # NEW: Audit service templates
│   │           └── dapr/          # NEW: Dapr components
│   │
│   └── digitalocean/            # NEW: DOKS-specific configs
│       └── cluster-config.md
│
├── .github/
│   └── workflows/
│       └── deploy.yml             # NEW: CI/CD pipeline
│
└── specs/
    └── 005-phase-05-cloud-native/
        ├── spec.md                # This file
        ├── plan.md
        └── tasks.md
```
