# Tasks: Phase 4 - Local Kubernetes Deployment

**Input**: Design documents from `/specs/004-phase-04-kubernetes/`
**Prerequisites**: plan.md, spec.md, contracts/helm-chart-structure.md, data-model.md, research.md, quickstart.md

**Tests**: Not explicitly requested - implementation tasks only.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Helm charts**: `deployment/helm/todo-app/`
- **Templates**: `deployment/helm/todo-app/templates/`
- **Service templates**: `deployment/helm/todo-app/templates/{frontend,backend,mcp-server}/`

---

## Phase 1: Setup (Helm Chart Structure)

**Purpose**: Create complete Helm chart structure with all configuration

- [X] T001 Create Helm chart directory structure at deployment/helm/todo-app/templates/{frontend,backend,mcp-server}/
- [X] T002 Create Chart.yaml with metadata in deployment/helm/todo-app/Chart.yaml
- [X] T003 Create COMPLETE values.yaml with all configuration (images, replicas, resources, ports, ingress, healthCheck, secrets, config) in deployment/helm/todo-app/values.yaml
- [X] T004 [P] Create .helmignore file in deployment/helm/todo-app/.helmignore
- [X] T005 [P] Create _helpers.tpl with template helpers in deployment/helm/todo-app/templates/_helpers.tpl

**Checkpoint**: Helm chart structure ready with complete configuration

---

## Phase 2: Foundational (Shared Kubernetes Resources)

**Purpose**: Core Kubernetes resources that ALL services depend on

**⚠️ CRITICAL**: No deployment work can begin until this phase is complete

- [X] T006 Create namespace.yaml in deployment/helm/todo-app/templates/namespace.yaml
- [X] T007 [P] Create COMPLETE configmap.yaml with MCP_SERVER_URL and INTERNAL_API_URL in deployment/helm/todo-app/templates/configmap.yaml
- [X] T008 [P] Create COMPLETE secret.yaml with DATABASE_URL, JWT_SECRET, GEMINI_API_KEY placeholders in deployment/helm/todo-app/templates/secret.yaml

**Checkpoint**: Foundation ready - namespace, configmap, secret all configured

---

## Phase 3: User Story 1 - Deploy Application (Priority: P1) 🎯 MVP

**Goal**: Deploy all three services with COMPLETE deployments (replicas, probes, envFrom, resources)

**Independent Test**: Run `helm install todo-app ./deployment/helm/todo-app -n todo-app --create-namespace` and verify all pods are running

### Implementation for User Story 1

- [X] T009 [P] [US1] Create COMPLETE frontend deployment.yaml (replicas, image, ports, resources, livenessProbe, readinessProbe, envFrom) in deployment/helm/todo-app/templates/frontend/deployment.yaml
- [X] T010 [P] [US1] Create frontend service.yaml (ClusterIP, port 3000) in deployment/helm/todo-app/templates/frontend/service.yaml
- [X] T011 [P] [US1] Create COMPLETE backend deployment.yaml (replicas, image, ports, resources, livenessProbe, readinessProbe, envFrom) in deployment/helm/todo-app/templates/backend/deployment.yaml
- [X] T012 [P] [US1] Create backend service.yaml (ClusterIP, port 8000) in deployment/helm/todo-app/templates/backend/service.yaml
- [X] T013 [P] [US1] Create COMPLETE mcp-server deployment.yaml (replicas, image, ports, resources, livenessProbe, readinessProbe, envFrom) in deployment/helm/todo-app/templates/mcp-server/deployment.yaml
- [X] T014 [P] [US1] Create mcp-server service.yaml (ClusterIP, port 5001) in deployment/helm/todo-app/templates/mcp-server/service.yaml
- [X] T015 [US1] Validate chart syntax with helm lint ./deployment/helm/todo-app
- [X] T016 [US1] Test template rendering with helm template todo-app ./deployment/helm/todo-app

**Checkpoint**: User Story 1 complete - all services deploy with single command

---

## Phase 4: User Story 2 - Access via Single URL (Priority: P1)

**Goal**: Configure NGINX Ingress to route / to frontend and /api/* to backend

**Independent Test**: Access http://todo.local in browser after adding hosts entry

### Implementation for User Story 2

- [X] T017 [US2] Create ingress.yaml with path routing (/ → frontend:3000, /api/* → backend:8000) in deployment/helm/todo-app/templates/ingress.yaml
- [X] T018 [US2] Create NOTES.txt with post-install instructions (hosts file, access URL) in deployment/helm/todo-app/templates/NOTES.txt
- [X] T019 [US2] Test dry-run deployment with helm install --dry-run --debug todo-app ./deployment/helm/todo-app

**Checkpoint**: User Story 2 complete - application accessible via http://todo.local

---

## Phase 5: Validation - Self-Healing, Scaling, Secrets (Priority: P2)

**Goal**: Verify US3, US4, US5 features work correctly (already built into deployments)

**Purpose**: These features are already implemented in Phase 3 deployments. This phase validates they work.

### Validation for User Story 3 (Self-Healing)

- [X] T020 [US3] Verify livenessProbe configuration in all deployments (check helm template output)
- [X] T021 [US3] Verify readinessProbe configuration in all deployments (check helm template output)

### Validation for User Story 4 (Scaling)

- [X] T022 [US4] Verify replicas configuration in all deployments (check helm template output)
- [X] T023 [US4] Verify RollingUpdate strategy in all deployments (maxUnavailable: 0, maxSurge: 1)

### Validation for User Story 5 (Secrets)

- [X] T024 [US5] Verify secret.yaml contains all required keys (DATABASE_URL, JWT_SECRET, GEMINI_API_KEY)
- [X] T025 [US5] Verify envFrom secretRef in backend and mcp-server deployments
- [X] T026 [US5] Verify envFrom configMapRef in all deployments

**Checkpoint**: All P2 features validated - self-healing, scaling, secrets configured correctly

---

## Phase 6: Documentation (Priority: P3)

**Goal**: Complete quickstart.md with all operational commands

### Documentation for User Story 6 (Monitoring)

- [X] T027 [P] [US6] Document pod health check commands in specs/004-phase-04-kubernetes/quickstart.md
- [X] T028 [P] [US6] Document log viewing commands in specs/004-phase-04-kubernetes/quickstart.md

### Documentation for User Story 7 (Lifecycle)

- [X] T029 [P] [US7] Document helm upgrade procedure in specs/004-phase-04-kubernetes/quickstart.md
- [X] T030 [P] [US7] Document helm rollback procedure in specs/004-phase-04-kubernetes/quickstart.md
- [X] T031 [P] [US7] Document helm uninstall and cleanup in specs/004-phase-04-kubernetes/quickstart.md

**Checkpoint**: Documentation complete - all operational commands documented

---

## Phase 7: Polish & Final Validation

**Purpose**: Final validation and deployment checklist

- [X] T032 Run helm lint ./deployment/helm/todo-app and fix any warnings
- [X] T033 [P] Run helm template and verify all resources render correctly
- [X] T034 [P] Verify all acceptance scenarios from spec.md can be tested
- [X] T035 Create deployment checklist in specs/004-phase-04-kubernetes/checklists/deployment.md
- [X] T036 Final review of all Helm templates for consistency

**Checkpoint**: Phase 4 implementation complete - ready for deployment

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup) ──► Phase 2 (Foundational) ──► Phase 3 (US1) ──► Phase 4 (US2)
                                                                      │
                                                                      ▼
                                                               Phase 5 (Validation)
                                                                      │
                                                                      ▼
                                                               Phase 6 (Documentation)
                                                                      │
                                                                      ▼
                                                               Phase 7 (Polish)
```

### Within Each Phase

- Phase 1: T001 first (creates directories), then T002-T005 can parallel
- Phase 2: T006 first (namespace), then T007-T008 can parallel
- Phase 3: T009-T014 can all run in parallel, then T015-T016 sequential
- Phase 4: T017 first, then T018-T019
- Phase 5: All validation tasks can run in parallel
- Phase 6: All documentation tasks can run in parallel
- Phase 7: T032 first, then T033-T036

### Parallel Opportunities

| Phase | Parallel Tasks |
|-------|----------------|
| 1 | T004, T005 |
| 2 | T007, T008 |
| 3 | T009, T010, T011, T012, T013, T014 (all 6 files) |
| 5 | T020-T026 (all validation) |
| 6 | T027-T031 (all documentation) |
| 7 | T033, T034 |

---

## Summary

| Phase | Purpose | Tasks | Count |
|-------|---------|-------|-------|
| 1 | Setup | T001-T005 | 5 |
| 2 | Foundational | T006-T008 | 3 |
| 3 | US1: Deploy | T009-T016 | 8 |
| 4 | US2: Ingress | T017-T019 | 3 |
| 5 | Validation (US3-5) | T020-T026 | 7 |
| 6 | Documentation (US6-7) | T027-T031 | 5 |
| 7 | Polish | T032-T036 | 5 |

**Total**: 36 tasks across 7 phases

**MVP Scope**: Phases 1-4 (19 tasks) - Deploy and access via http://todo.local

---

## Key Changes from Previous Version

| Issue | Before | After |
|-------|--------|-------|
| Health Probes | Added in Phase 5 | Built into Phase 3 deployments |
| Replicas | Added in Phase 6 | Built into Phase 3 deployments |
| envFrom | Added in Phase 7 | Built into Phase 3 deployments |
| values.yaml | Updated multiple times | Complete in Phase 1 (T003) |
| secret.yaml | Created empty, filled later | Complete in Phase 2 (T008) |
| Phase count | 10 phases | 7 phases (more efficient) |
| Task count | 48 tasks | 36 tasks (reduced redundancy) |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- COMPLETE means all required fields per contract (replicas, probes, envFrom, resources)
- Deployments are created ONCE with all features, not incrementally modified
- Validation phases verify features work, not add them
- Commit after each phase completion
