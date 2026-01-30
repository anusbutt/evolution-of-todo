# Research: Phase 4 - Local Kubernetes Deployment

**Feature**: 004-phase-04-kubernetes
**Date**: 2026-01-22
**Status**: Complete

## Technology Decisions

### 1. Local Kubernetes Cluster

**Decision**: Minikube

**Rationale**:
- Constitution specifies "Kubernetes via Minikube" for Phase IV
- Minikube is the most mature local Kubernetes solution
- Works with Docker Desktop as driver
- Built-in addon system for ingress, dashboard, etc.
- Single-node cluster sufficient for local development

**Alternatives Considered**:
- Kind (Kubernetes in Docker): Lighter weight but fewer addons
- k3s: Designed for edge/IoT, overkill for local dev
- Docker Desktop Kubernetes: Limited configuration options

---

### 2. Package Manager

**Decision**: Helm Charts

**Rationale**:
- Constitution specifies "Helm Charts" for Phase IV
- Industry standard for Kubernetes package management
- Templating enables environment-specific configuration
- Single command deployment (helm install)
- Built-in upgrade and rollback support
- Version history for releases

**Alternatives Considered**:
- Kustomize: Simpler but less flexible for complex apps
- Plain YAML manifests: Too many files to manage manually
- Terraform: Overkill for local Kubernetes

---

### 3. AIOps Tools

**Decision**: kubectl-ai and kagent

**Rationale**:
- Constitution specifies "kubectl-ai, kagent" for Phase IV
- kubectl-ai: Natural language Kubernetes commands
- kagent: AI-powered cluster analysis and optimization
- Enhances developer experience
- Reduces learning curve for Kubernetes operations

**Alternatives Considered**:
- Standard kubectl only: Steeper learning curve
- k9s: TUI but no AI assistance

---

### 4. Ingress Controller

**Decision**: NGINX Ingress (Minikube addon)

**Rationale**:
- Built into Minikube as addon (easy setup)
- Industry standard ingress controller
- Supports path-based routing needed for frontend/backend split
- Well-documented configuration options

**Alternatives Considered**:
- Traefik: More features but more complex setup
- Kong: Enterprise features unnecessary for local dev
- HAProxy: Less Kubernetes-native

---

### 5. Resource Limits

**Decision**: Per-service resource limits with cluster cap of 4 CPU, 8GB RAM

**Rationale**:
- Constitution specifies "Minikube with resource limits (4 CPU, 8GB RAM)"
- Prevents cluster from consuming all host resources
- Ensures fair resource distribution among services
- Mirrors production constraints

**Resource Allocation**:
| Service | CPU Request | CPU Limit | Memory Request | Memory Limit |
|---------|-------------|-----------|----------------|--------------|
| Frontend | 100m | 500m | 128Mi | 512Mi |
| Backend | 200m | 1000m | 256Mi | 1Gi |
| MCP Server | 100m | 500m | 128Mi | 512Mi |

---

### 6. Image Strategy

**Decision**: Load local images into Minikube

**Rationale**:
- Faster than pushing to registry and pulling
- Works offline once images are built
- `minikube image load` command
- No registry credentials needed

**Alternatives Considered**:
- Docker Hub: Requires network, slower iteration
- Local registry: Additional complexity
- `imagePullPolicy: Never`: Requires eval $(minikube docker-env)

---

### 7. Health Check Strategy

**Decision**: HTTP health checks on existing endpoints

**Rationale**:
- Backend already has `/api/health` endpoint
- Frontend responds to `/` with 200
- MCP server can use `/health` endpoint
- Kubernetes native liveness/readiness probes

**Configuration**:
- Liveness: Check if container is alive (restart if fails)
- Readiness: Check if container can serve traffic (remove from load balancer if fails)

---

### 8. Secret Management

**Decision**: Kubernetes Secrets (base64 encoded)

**Rationale**:
- Constitution specifies "Kubernetes Secrets" for Phase IV+
- Native Kubernetes resource
- Can be referenced in pods as environment variables
- Helm can template secret values from values.yaml

**Secrets Required**:
- DATABASE_URL
- JWT_SECRET
- GEMINI_API_KEY

---

## Architecture Decisions Summary

| Component | Technology | Reason |
|-----------|------------|--------|
| Cluster | Minikube | Constitution requirement |
| Packaging | Helm Charts | Constitution requirement |
| AIOps | kubectl-ai, kagent | Constitution requirement |
| Ingress | NGINX (Minikube addon) | Built-in, standard |
| Images | Local load | Fastest iteration |
| Secrets | K8s Secrets | Native, secure |
| Health | HTTP probes | Standard pattern |

---

## Resolved Questions

1. **Q: How to handle cross-service communication?**
   A: Kubernetes Services provide internal DNS (e.g., `backend.todo-app.svc.cluster.local`)

2. **Q: How to expose application externally?**
   A: Ingress with host `todo.local` + hosts file entry pointing to Minikube IP

3. **Q: How to handle environment-specific configuration?**
   A: Helm values.yaml with different values per environment

4. **Q: How to ensure zero-downtime upgrades?**
   A: Rolling update strategy with maxUnavailable: 0 and readiness probes
