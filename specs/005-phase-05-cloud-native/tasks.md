# Tasks: Phase 5 - Cloud Native Deployment

**Input**: Design documents from `/specs/005-phase-05-cloud-native/`
**Prerequisites**: plan.md (complete), spec.md (complete)

**Tests**: Not explicitly requested - implementation tasks only

**Organization**: Tasks grouped by user story for independent implementation and testing

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1-US9)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, cloud accounts, and tooling setup

- [x] T001 Create feature branch `005-phase-05-cloud-native` from main
- [x] ~~T002 Create Oracle Cloud Infrastructure (OCI) free tier account~~ → **REPLACED by T021a (DigitalOcean)**
- [x] T003 Create Redpanda Cloud free tier account (serverless)
- [x] ~~T004 [P] Install OCI CLI and configure authentication~~ → **REPLACED by T022a (doctl CLI)**
- [x] T005 [P] Install Dapr CLI v1.12+ for local development
- [x] T006 [P] Create services/ directory structure per plan.md
- [x] T007 Add Dapr SDK dependencies to backend/pyproject.toml

**Note**: T002/T004 originally for OCI. T021-T037 originally for OCI/OKE but replaced with DigitalOcean/DOKS due to ARM64 capacity exhaustion in Mumbai region.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Database Models (create first for Alembic autogenerate)

- [x] T008 [P] Create Priority enum and update Task model in backend/app/models/task.py
- [x] T009 [P] Create Tag model in backend/app/models/tag.py
- [x] T010 [P] Create TaskTag junction model in backend/app/models/task_tag.py
- [x] T011 [P] Create AuditLog model in backend/app/models/audit_log.py
- [x] T012 Update backend/app/models/__init__.py to export new models

### Schemas

- [x] T013 [P] Create Tag schemas in backend/app/schemas/tag.py
- [x] T014 [P] Create Event schemas in backend/app/schemas/event.py
- [x] T015 Update Task schemas with priority and tags in backend/app/schemas/task.py
- [x] T016 Update frontend/types/task.ts with priority and tags types

### Database Migration

- [x] T017 Generate Alembic migration with `alembic revision --autogenerate -m "add_priority_tags_audit"`
- [x] T018 Review and adjust generated migration in backend/alembic/versions/
- [x] T019 Add default tags seed data to migration (Work, Personal, Shopping, Health, Finance)
- [x] T020 Run database migration `alembic upgrade head`

**Checkpoint**: Database ready with priority, tags, and audit_log tables - user story implementation can begin

---

## Phase 3: User Story 1 - Cloud Deployment (Priority: P1) 🎯 MVP

**Goal**: Deploy the app to DigitalOcean Kubernetes Service (DOKS) with all services running

**Independent Test**: Access app via DigitalOcean Load Balancer IP, all pods healthy, health checks passing

**Migration Note**: Tasks T021-T037 replaced from OCI/OKE to DigitalOcean/DOKS. OCI ARM64 capacity exhausted in Mumbai, free tier limited to 1 region. DigitalOcean provides $200 credit and reliable provisioning in Frankfurt (fra1).

### Implementation for US1

- [x] T021a [US1] Create DigitalOcean account with $200 free credit (replaces T021 OCI account) ✅ DONE
- [x] T022a [US1] Install doctl CLI v1.150+ and authenticate (`doctl auth init`) ✅ DONE
- [x] T023a [US1] Create DOKS cluster in Frankfurt (`doctl kubernetes cluster create`) ✅ DONE
- [x] T024a [US1] Configure kubectl to connect to DOKS (`doctl kubernetes cluster kubeconfig save`) ✅ DONE (auto)
- [x] T025a [US1] Create DigitalOcean Container Registry (`doctl registry create`) ✅ DONE
- [x] T026a [P] [US1] Update frontend/Dockerfile for amd64 production build ✅ DONE
- [x] T027a [P] [US1] Update backend/Dockerfile for amd64 production build ✅ DONE
- [x] T028a [P] [US1] Update mcp-server/Dockerfile for amd64 production build ✅ DONE
- [x] T029a [US1] Login to DOCR and build/push Docker images ✅ DONE
- [x] T030a [US1] Integrate DOCR with DOKS cluster (`doctl registry kubernetes-manifest`) ✅ DONE
- [x] T031a [US1] Update values-prod.yaml with DOKS-specific configuration ✅ DONE
- [x] T032a [US1] Create `todo-app` namespace in DOKS cluster ✅ DONE
- [x] T033a [US1] Create Kubernetes secrets (todo-secrets) via Helm --set ✅ DONE
- [x] T034a [US1] Deploy application using Helm to DOKS ✅ DONE (Revision 2)
- [x] T035a [US1] Verify LoadBalancer services get external IPs → 209.38.115.191:3000 ✅ DONE
- [x] T036a [US1] Verify all pods are running with `kubectl get pods -n todo-app` ✅ DONE (3/3 Running)
- [x] T037a [US1] Document DOKS setup steps in deployment/digitalocean/cluster-config.md ✅ DONE

**Checkpoint**: App deployed to DOKS, accessible via DigitalOcean Load Balancer IP

---

## Phase 4: User Story 2 - Event-Driven Architecture (Priority: P1)

**Goal**: Backend publishes task events to Redpanda via Dapr Pub/Sub

**Independent Test**: Create a task, verify event appears in Redpanda Console

**Dependencies**: US1 complete (DOKS running)

### Implementation for US2

- [x] T038 [US2] Create Redpanda Cloud serverless cluster ✅ DONE
- [x] T039 [US2] Create `task-events` topic with 3 partitions in Redpanda Cloud ✅ DONE
- [x] T040 [US2] Create `task-updates` topic (reserved for future use) ✅ DONE
- [x] T041 [US2] Generate Redpanda SASL credentials and note bootstrap servers ✅ DONE
- [x] T042 [US2] Create backend/app/events/ directory and __init__.py ✅ DONE
- [x] T043 [US2] Create event publisher service in backend/app/events/publisher.py ✅ DONE
- [x] T044 [US2] Add event publishing to task create in backend/app/routes/tasks.py ✅ DONE
- [x] T045 [US2] Add event publishing to task update in backend/app/routes/tasks.py ✅ DONE
- [x] T046 [US2] Add event publishing to task delete in backend/app/routes/tasks.py ✅ DONE
- [x] T047 [US2] Add event publishing to task complete in backend/app/routes/tasks.py ✅ DONE
- [x] T048 [US2] Create Dapr Pub/Sub component for Redpanda ✅ DONE (secretstore removed - built-in)
- [x] T049 [US2] ~~Create Dapr Secrets component~~ SKIPPED (Dapr has built-in kubernetes secretstore)
- [x] T050 [US2] Create DOKS secret for Redpanda credentials (redpanda-secrets) ✅ DONE
- [x] T051 [US2] Install Dapr v1.16.8 on DOKS cluster using `dapr init -k` ✅ DONE
- [x] T052 [US2] Update deployments to enable Dapr sidecar injection ✅ DONE
- [x] T053 [US2] Redeploy backend with Dapr sidecar enabled ✅ DONE (2/2 Running)
- [x] T054 [US2] Verify events flowing in Redpanda Cloud Console ✅ DONE (4 events published)

**Checkpoint**: Task operations publish events to Redpanda via Dapr

---

## Phase 5: User Story 3 - Audit Logging (Priority: P1)

**Goal**: Audit Service consumes events and logs all task operations

**Independent Test**: Create/update/delete tasks, verify entries in audit_log table and GET /api/audit endpoint

**Dependencies**: US2 complete (events flowing to Redpanda)

### Implementation for US3

- [x] T055 [US3] Create services/audit-service/ directory structure ✅ DONE
- [x] T056 [US3] Create services/audit-service/requirements.txt with FastAPI, Dapr, asyncpg ✅ DONE
- [x] T057 [US3] Create services/audit-service/app/__init__.py ✅ DONE
- [x] T058 [US3] Create services/audit-service/app/config.py with database config ✅ DONE
- [x] T059 [US3] Create services/audit-service/app/models/audit_log.py ✅ DONE
- [x] T060 [US3] Create services/audit-service/app/handlers/task_events.py ✅ DONE
- [x] T061 [US3] Create services/audit-service/app/main.py with Dapr subscription ✅ DONE
- [x] T062 [US3] Create services/audit-service/Dockerfile for production (amd64) ✅ DONE
- [x] T063 [US3] Create Dapr subscription config in services/audit-service/dapr/subscription.yaml ✅ DONE
- [x] T064 [US3] Build audit-service image and push to DOCR ✅ DONE
- [x] T065 [US3] Add audit-service deployment to Helm chart ✅ DONE
- [x] T066 [US3] Add audit-service service to Helm chart ✅ DONE
- [x] T067 [US3] Update values.yaml and values-prod.yaml with audit-service config ✅ DONE
- [x] T068 [US3] Deploy audit-service to DOKS with Helm upgrade ✅ DONE (Revision 10)
- [x] T069 [US3] Create GET /api/audit endpoint in backend/app/routes/audit.py ✅ DONE
- [x] T070 [US3] Register audit router in backend/app/main.py ✅ DONE
- [x] T071 [US3] Verify audit logs appearing in database after task operations ✅ DONE (all 4 event types)

**Checkpoint**: All task CRUD operations logged to audit_log table

---

## Phase 6: User Story 4 - Task Priorities (Priority: P2)

**Goal**: Users can assign and view task priorities (P1/P2/P3)

**Independent Test**: Create task with priority P1, verify red indicator shown, filter by priority works

**Dependencies**: Phase 2 (Foundation), US2 (for event publishing updates)

### Implementation for US4

- [x] T072 [US4] Update task service to handle priority in backend/app/services/task_service.py ✅ DONE (UI Redesign)
- [x] T073 [US4] Update POST /api/tasks to accept priority in backend/app/routes/tasks.py ✅ DONE
- [x] T074 [US4] Update PUT /api/tasks/{id} to accept priority in backend/app/routes/tasks.py ✅ DONE
- [x] T075 [US4] Include priority in task-events payload in backend/app/events/publisher.py ✅ DONE
- [x] T076 [US4] Create PriorityBadge component in frontend/components/ui/priority-badge.tsx ✅ DONE
- [x] T077 [US4] Update TaskCard to display priority badge in frontend/components/tasks/task-item.tsx ✅ DONE
- [x] T078 [US4] Update TaskForm to include priority select in frontend/components/tasks/task-form.tsx ✅ DONE
- [x] T079 [US4] Update task service for priority in frontend (integrated in tasks page) ✅ DONE

**Checkpoint**: Tasks display color-coded priority indicators (Red=P1, Yellow=P2, Green=P3) ✅ COMPLETE

---

## Phase 7: User Story 5 - Task Tags (Priority: P2)

**Goal**: Users can add tags to categorize tasks

**Independent Test**: Add Work and Shopping tags to a task, verify colored chips displayed

**Dependencies**: Phase 2 (Foundation), US2 (for event publishing updates)

### Implementation for US5

- [x] T080 [US5] Create Tag routes in backend/app/routes/tags.py (GET, POST, DELETE) ✅ DONE
- [x] T081 [US5] Register tags router in backend/app/main.py ✅ DONE
- [x] T082 [US5] Update task service to handle tag associations in backend/app/services/task_service.py ✅ DONE
- [x] T083 [US5] Update POST /api/tasks to accept tag_ids in backend/app/routes/tasks.py ✅ DONE
- [x] T084 [US5] Update PUT /api/tasks/{id} to accept tag_ids in backend/app/routes/tasks.py ✅ DONE
- [x] T085 [US5] Include tags in task-events payload in backend/app/events/publisher.py ✅ DONE
- [x] T086 [US5] Create Tag chip component in frontend/components/ui/tag-chip.tsx ✅ DONE
- [x] T087 [US5] Update TaskCard to display tags in frontend/components/tasks/task-item.tsx ✅ DONE
- [x] T088 [US5] Update TaskForm with tag selection checkboxes in frontend/components/tasks/task-form.tsx ✅ DONE
- [x] T089 [US5] Create tag service in frontend (integrated in tasks page) ✅ DONE

**Checkpoint**: Tasks display colored tag chips, can add/remove tags ✅ COMPLETE

---

## Phase 8: User Story 6 - Search Tasks (Priority: P2)

**Goal**: Users can search tasks by title and description

**Independent Test**: Create "Buy milk" and "Buy bread" tasks, search "Buy", both appear

**Dependencies**: Phase 2 (Foundation only)

### Implementation for US6

- [x] T090 [US6] Implement search_tasks method in backend/app/services/task_service.py ✅ DONE
- [x] T091 [US6] Create GET /api/tasks/search endpoint in backend/app/routes/tasks.py ✅ DONE
- [x] T092 [US6] Create TaskSearch component in frontend/components/tasks/task-filters.tsx ✅ DONE (integrated into TaskFilters)
- [x] T093 [US6] Add search input to tasks page in frontend/app/(dashboard)/tasks/page.tsx ✅ DONE
- [x] T094 [US6] Implement debounced search in frontend (client-side filtering - instant) ✅ DONE
- [x] T095 [US6] Update task-service with search method (client-side via useMemo) ✅ DONE

**Checkpoint**: Search input filters tasks by title/description in real-time ✅ COMPLETE

---

## Phase 9: User Story 7 - Filter Tasks (Priority: P2)

**Goal**: Users can filter tasks by status, priority, and tags

**Independent Test**: Filter by completed=false and priority=P1, only matching tasks shown

**Dependencies**: US4 (Priority), US5 (Tags) - needs priority/tags to filter by

### Implementation for US7

- [x] T096 [US7] Implement filter_tasks method (client-side via useMemo in tasks/page.tsx) ✅ DONE
- [x] T097 [US7] Create GET /api/tasks/filter endpoint (not needed - client-side filtering) ✅ SKIPPED
- [x] T098 [US7] Create TaskFilter component in frontend/components/tasks/task-filters.tsx ✅ DONE
- [x] T099 [US7] Add filter controls to tasks page in frontend/app/(dashboard)/tasks/page.tsx ✅ DONE
- [x] T100 [US7] Implement URL query param persistence for filters ✅ DONE (useSearchParams)
- [x] T101 [US7] Update task-service with filter method (client-side via useMemo) ✅ DONE

**Checkpoint**: Filter bar allows filtering by status, priority, tags with URL persistence ✅ COMPLETE

---

## Phase 10: User Story 8 - Sort Tasks (Priority: P2)

**Goal**: Users can sort tasks by created_at, priority, or title

**Independent Test**: Sort by priority ascending, P1 tasks appear first

**Dependencies**: US7 (Filter) - sort is part of filter endpoint

### Implementation for US8

- [x] T102 [US8] Add sort parameters (client-side via useMemo in tasks/page.tsx) ✅ DONE
- [x] T103 [US8] Update GET /api/tasks/filter (not needed - client-side sorting) ✅ SKIPPED
- [x] T104 [US8] Add sort dropdown to TaskFilter component in task-filters.tsx ✅ DONE (lines 273-318)
- [x] T105 [US8] Implement sort direction toggle in TaskFilter ✅ DONE (lines 113-122)
- [x] T106 [US8] Persist sort state in URL query params (sortBy, sortDir) ✅ DONE
- [x] T107 [US8] Default sort to created_at descending ✅ DONE (line 53-55)

**Checkpoint**: Sort dropdown changes task order, persisted in URL ✅ COMPLETE

---

## Phase 11: User Story 9 - CI/CD Pipeline (Priority: P1)

**Goal**: Automated deployment via GitHub Actions on push to main

**Independent Test**: Push to main, verify workflow runs, images built, deployed to DOKS

**Dependencies**: US1 (DOKS deployed)

### Implementation for US9

- [x] T108 [US9] Create .github/workflows/ directory ✅ DONE
- [x] T109 [US9] Create .github/workflows/deploy.yml CI/CD workflow ✅ DONE
- [x] T110 [US9] Add test job (pytest backend, npm test frontend) ✅ DONE
- [x] T111 [US9] Add build job (docker build and push to DOCR) ✅ DONE
- [x] T112 [US9] Add deploy job (doctl kubeconfig save + helm upgrade to DOKS) ✅ DONE
- [x] T113 [US9] Add smoke-test job (verify deployment health via Load Balancer IP) ✅ DONE
- [x] T114 [US9] Configure GitHub repository secrets (DIGITALOCEAN_ACCESS_TOKEN, REDPANDA_*) ✅ DONE
- [x] T115 [US9] Test pipeline with push to feature branch first ✅ DONE (Pipeline running)
- [x] T116 [US9] Document CI/CD setup in .github/workflows/README.md ✅ DONE

**Checkpoint**: Push to main triggers full CI/CD pipeline with deployment to DOKS

---

## Phase 12: Polish & Cross-Cutting Concerns

**Purpose**: Final integration, documentation, and cleanup

- [x] T117 Update MCP server tools to include priority/tags in mcp-server/tools/ ✅ DONE
- [x] T118 Update chatbot prompts to handle priority and tags ✅ DONE
- [x] T119 [P] Update README.md with Phase 5 deployment instructions ✅ DONE
- [x] T120 [P] Create .env.example with all required environment variables ✅ DONE
- [x] T121 Test full application flow (create task with priority/tags, verify event, check audit) ✅ VERIFIED
- [x] T122 Verify all pods running and health checks passing on DOKS ✅ VERIFIED (4/4 pods Running)
- [x] T123 Verify DigitalOcean Load Balancer accessible (frontend) ✅ VERIFIED (209.38.115.191:3000)
- [ ] T124 Clean up unused resources and verify credit budget usage ⚠️ MANUAL (check DO dashboard)

**Checkpoint**: Phase 5 Cloud Native Deployment complete!

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - can start immediately
- **Phase 2 (Foundational)**: Depends on T007 (Dapr SDK) - BLOCKS all user stories
- **Phase 3 (US1)**: Depends on Phase 2
- **Phase 4 (US2)**: Depends on US1 (T036a - pods running on DOKS)
- **Phase 5 (US3)**: Depends on US2 (T054 - events flowing)
- **Phase 6-7 (US4, US5)**: Depends on Phase 2 + US2 (for event updates)
- **Phase 8 (US6)**: Depends on Phase 2 only
- **Phase 9 (US7)**: Depends on US4 + US5
- **Phase 10 (US8)**: Depends on US7
- **Phase 11 (US9)**: Depends on US1 (OKE deployed)
- **Phase 12 (Polish)**: Depends on all user stories being complete

### User Story Dependencies

| Story | Can Start After | Hard Dependencies |
|-------|-----------------|-------------------|
| US1 (Cloud) | Phase 2 | None |
| US2 (Events) | US1 | DOKS deployed (T036a) |
| US3 (Audit) | US2 | Events flowing (T054) |
| US4 (Priority) | US2 | Event publisher exists (T043) |
| US5 (Tags) | US2 | Event publisher exists (T043) |
| US6 (Search) | Phase 2 | None |
| US7 (Filter) | US4 + US5 | Priority & Tags implemented |
| US8 (Sort) | US7 | Filter endpoint exists (T097) |
| US9 (CI/CD) | US1 | OKE deployed (T036) |

### Critical Path

```
Phase 1 → Phase 2 → US1 (Cloud) → US2 (Events) → US3 (Audit)
                                       │
                                       ├──→ US4 (Priority) ─┐
                                       │                    ├──→ US7 (Filter) → US8 (Sort)
                                       ├──→ US5 (Tags) ─────┘
                                       │
                                       └──→ US9 (CI/CD)

                    Phase 2 → US6 (Search) [independent track]
```

### Parallel Opportunities

**Phase 1 (2 parallel):**
- T005, T006 can run in parallel (Dapr CLI, services/ directory)

**Phase 2 (4 parallel for models, 2 parallel for schemas):**
- T008, T009, T010, T011 (models) can run in parallel
- T013, T014 (schemas) can run in parallel

**Phase 3 (3 parallel for Dockerfiles):**
- T024, T025, T026 (Dockerfiles) can run in parallel

**After US2, these can start (but not fully parallel):**
- US4 (Priority) and US5 (Tags) can run in parallel
- US6 (Search) can run anytime after Phase 2
- US9 (CI/CD) can run anytime after US1 (DOKS deployed)

---

## Parallel Example: Foundation Models

```bash
# Launch all model files in parallel:
Task: T008 "Create Priority enum and update Task model"
Task: T009 "Create Tag model"
Task: T010 "Create TaskTag junction model"
Task: T011 "Create AuditLog model"

# After models complete, update __init__.py:
Task: T012 "Update models __init__.py"
```

## Parallel Example: Cloud Deployment (US1)

```bash
# Launch Dockerfile updates in parallel:
Task: T026a "Update frontend/Dockerfile for amd64 production"
Task: T027a "Update backend/Dockerfile for amd64 production"
Task: T028a "Update mcp-server/Dockerfile for amd64 production"

# After Dockerfiles complete, build and push images to DOCR:
Task: T029a "Build and push Docker images to DOCR"
```

---

## Implementation Strategy

### MVP First (US1 + US2 + US3)

1. Complete Phase 1: Setup (T001-T007) ✅ DONE
2. Complete Phase 2: Foundational (T008-T020) ✅ DONE
3. Complete Phase 3: US1 Cloud Deployment (T021a-T037a) - 2 tasks done, 15 remaining
4. **VALIDATE**: App accessible on DOKS via Load Balancer IP
5. Complete Phase 4: US2 Event Architecture (T038-T054)
6. **VALIDATE**: Events flowing to Redpanda
7. Complete Phase 5: US3 Audit Service (T055-T071)
8. **DEPLOY/DEMO**: Core event-driven architecture complete

### Incremental Delivery

After MVP:
1. Add US6 (Search) → Can start immediately after Phase 2
2. Add US4 (Priority) → Requires US2, Test → Deploy
3. Add US5 (Tags) → Requires US2, Test → Deploy
4. Add US7 (Filter) → Requires US4+US5, Test → Deploy
5. Add US8 (Sort) → Requires US7, Test → Deploy
6. Add US9 (CI/CD) → Automate future deployments
7. Polish → Final release

---

## Summary

| Metric | Value |
|--------|-------|
| **Total Tasks** | 124 (T001-T124) |
| **Phase 1 (Setup)** | 7 tasks (2 replaced by Phase 3) ✅ COMPLETE |
| **Phase 2 (Foundational)** | 13 tasks (T008-T020) ✅ COMPLETE |
| **US1 (Cloud/DOKS)** | 17 tasks (T021a-T037a) - 2 done (account+CLI), 15 remaining |
| **US2 (Events)** | 17 tasks (T038-T054) |
| **US3 (Audit)** | 17 tasks (T055-T071) |
| **US4 (Priority)** | 8 tasks (T072-T079) |
| **US5 (Tags)** | 10 tasks (T080-T089) |
| **US6 (Search)** | 6 tasks (T090-T095) |
| **US7 (Filter)** | 6 tasks (T096-T101) |
| **US8 (Sort)** | 6 tasks (T102-T107) |
| **US9 (CI/CD)** | 9 tasks (T108-T116) |
| **Polish** | 8 tasks (T117-T124) |
| **Parallel Opportunities** | 10+ task groups |
| **MVP Scope** | US1 + US2 + US3 (51 tasks, 49 remaining) |
| **Platform** | DigitalOcean Kubernetes Service (DOKS) |
| **Region** | Frankfurt (fra1) |

---

## Notes

- DOKS uses **amd64 (x86_64) architecture** - standard Docker builds, no buildx platform flag needed
- Dapr sidecars add ~100MB memory per pod - monitor resource limits on 2GB nodes
- Redpanda free tier: 5GB storage, 1MB/s throughput - sufficient for this phase
- **DOKS budget**: ~$36/month ($24 nodes + $12 LB) = ~5 months on $200 credit
- Event publishing is fire-and-forget (async) - don't block API response
- Filter/Sort endpoints reuse same method with different params
- Use `doctl` for cluster management, `kubectl` for workload operations
- DigitalOcean Load Balancer provides external access (HTTP, TLS available via annotation)
- Images built locally and pushed to DOCR (`doctl registry login && docker push`)
- DOCR integrates natively with DOKS - no imagePullSecrets needed after `doctl registry kubernetes-manifest`
