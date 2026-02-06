---
id: 004
title: Implement Phase 3 DOKS Deployment
stage: green
date: 2026-02-05
surface: agent
model: claude-opus-4-5-20251101
feature: 005-phase-05-cloud-native
branch: 005-phase-05-cloud-native
user: architect
command: /sp.implement phase 3
labels: ["deployment", "digitalocean", "doks", "helm", "docker"]
links:
  spec: specs/005-phase-05-cloud-native/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - frontend/Dockerfile
  - backend/Dockerfile
  - mcp-server/Dockerfile
  - deployment/helm/todo-app/values-prod.yaml
  - deployment/helm/todo-app/templates/frontend/service.yaml
  - deployment/digitalocean/cluster-config.md
  - specs/005-phase-05-cloud-native/tasks.md
tests:
  - curl http://209.38.115.191:3000/ → HTTP 200
  - kubectl get pods -n todo-app → 3/3 Running
  - kubectl get svc -n todo-app → frontend LoadBalancer 209.38.115.191
---

## Prompt

/sp.implement phase 3. Execute Phase 3 (US1 - Cloud Deployment) tasks T021a-T037a to deploy the Todo App to DigitalOcean Kubernetes Service (DOKS) in Frankfurt.

## Response snapshot

Completed all 17 Phase 3 tasks (T021a-T037a):

1. **Dockerfiles** (T026a-T028a): Removed ARM64 `--platform=$BUILDPLATFORM` from frontend, updated comments for amd64/DOKS.
2. **Backend Dockerfile fix**: Added `--no-install-project` flag to first `uv sync` to fix build order issue (deps before source copy).
3. **Docker builds**: Built all 3 images (frontend, backend, mcp-server) and pushed to `registry.digitalocean.com/todo-app/`.
4. **values-prod.yaml** (T031a): Rewrote with DOCR image URLs, `registry-todo-app` pull secret, amd64 nodeSelector, right-sized resources for 2GB nodes.
5. **Frontend service template**: Changed hardcoded `ClusterIP` to `{{ .Values.serviceType | default "ClusterIP" }}` for LoadBalancer support.
6. **Helm deploy**: `helm upgrade --install` with secrets passed via `--set`. Revision 2 applied after service type fix.
7. **Verification**: All 3 pods Running (1/1), frontend LoadBalancer at `209.38.115.191:3000`, HTTP 200 confirmed.
8. **Documentation** (T037a): Created `deployment/digitalocean/cluster-config.md` with full setup guide.

## Outcome

- ✅ Impact: Todo App live on the internet at http://209.38.115.191:3000
- 🧪 Tests: curl HTTP 200, all pods Running 1/1, LoadBalancer IP assigned
- 📁 Files: 7 files modified/created
- 🔁 Next prompts: Phase 4 (US2 - Event-Driven Architecture with Redpanda + Dapr)
- 🧠 Reflection: DigitalOcean provisioned in ~5 minutes vs OCI's 1+ hour failure. Standard amd64 eliminated buildx complexity. Helm secret.yaml conflict required deleting kubectl-created secret.

## Evaluation notes (flywheel)

- Failure modes observed: uv sync build order (needed --no-install-project), Helm secret ownership conflict, hardcoded ClusterIP in service template
- Graders run and results (PASS/FAIL): PASS - all 17 tasks complete, app accessible
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to Phase 4 (Redpanda + Dapr event architecture)
