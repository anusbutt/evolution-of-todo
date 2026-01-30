# Data Model: Phase 4 - Kubernetes Resources

**Feature**: 004-phase-04-kubernetes
**Date**: 2026-01-22

## Overview

Phase 4 does not introduce new application data models. Instead, it defines Kubernetes resource models that orchestrate the existing application.

## Kubernetes Resources

### Namespace

**Purpose**: Logical isolation for all application resources

| Field | Value | Description |
|-------|-------|-------------|
| name | `todo-app` | Unique namespace identifier |
| labels | `app: todo-app` | Resource grouping |

---

### Deployments

#### Frontend Deployment

| Field | Value | Description |
|-------|-------|-------------|
| name | `frontend` | Deployment identifier |
| replicas | `1` (default) | Number of pod instances |
| image | `todo-frontend:latest` | Docker image |
| port | `3000` | Container port |
| resources.requests.cpu | `100m` | Minimum CPU |
| resources.requests.memory | `128Mi` | Minimum memory |
| resources.limits.cpu | `500m` | Maximum CPU |
| resources.limits.memory | `512Mi` | Maximum memory |

#### Backend Deployment

| Field | Value | Description |
|-------|-------|-------------|
| name | `backend` | Deployment identifier |
| replicas | `1` (default) | Number of pod instances |
| image | `todo-backend:latest` | Docker image |
| port | `8000` | Container port |
| resources.requests.cpu | `200m` | Minimum CPU |
| resources.requests.memory | `256Mi` | Minimum memory |
| resources.limits.cpu | `1000m` | Maximum CPU |
| resources.limits.memory | `1Gi` | Maximum memory |

#### MCP Server Deployment

| Field | Value | Description |
|-------|-------|-------------|
| name | `mcp-server` | Deployment identifier |
| replicas | `1` (default) | Number of pod instances |
| image | `todo-mcp-server:latest` | Docker image |
| port | `5001` | Container port |
| resources.requests.cpu | `100m` | Minimum CPU |
| resources.requests.memory | `128Mi` | Minimum memory |
| resources.limits.cpu | `500m` | Maximum CPU |
| resources.limits.memory | `512Mi` | Maximum memory |

---

### Services

#### Frontend Service

| Field | Value | Description |
|-------|-------|-------------|
| name | `frontend` | Service identifier |
| type | `ClusterIP` | Internal service |
| port | `3000` | Service port |
| targetPort | `3000` | Pod port |
| selector | `app: frontend` | Pod selection |

#### Backend Service

| Field | Value | Description |
|-------|-------|-------------|
| name | `backend` | Service identifier |
| type | `ClusterIP` | Internal service |
| port | `8000` | Service port |
| targetPort | `8000` | Pod port |
| selector | `app: backend` | Pod selection |

#### MCP Server Service

| Field | Value | Description |
|-------|-------|-------------|
| name | `mcp-server` | Service identifier |
| type | `ClusterIP` | Internal service |
| port | `5001` | Service port |
| targetPort | `5001` | Pod port |
| selector | `app: mcp-server` | Pod selection |

---

### Ingress

| Field | Value | Description |
|-------|-------|-------------|
| name | `todo-ingress` | Ingress identifier |
| host | `todo.local` | External hostname |
| path `/` | → `frontend:3000` | Frontend routing |
| path `/api/*` | → `backend:8000` | Backend API routing |
| annotations | NGINX rewrite rules | Path handling |

---

### ConfigMap

| Field | Key | Description |
|-------|-----|-------------|
| name | `todo-config` | ConfigMap identifier |
| data | `MCP_SERVER_URL` | Internal MCP server URL |
| data | `INTERNAL_API_URL` | Internal backend URL |

---

### Secret

| Field | Key | Description |
|-------|-----|-------------|
| name | `todo-secrets` | Secret identifier |
| data | `DATABASE_URL` | Neon PostgreSQL connection string |
| data | `JWT_SECRET` | JWT signing key |
| data | `GEMINI_API_KEY` | Gemini API key for chatbot |

---

## Resource Relationships

```
┌─────────────────────────────────────────────────────────────┐
│                    Namespace: todo-app                      │
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  ConfigMap  │  │   Secret    │  │   Ingress   │         │
│  │ todo-config │  │ todo-secrets│  │ todo-ingress│         │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘         │
│         │                │                │                 │
│         └────────────────┼────────────────┘                 │
│                          │                                  │
│  ┌───────────────────────┼───────────────────────┐         │
│  │                       ▼                       │         │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐        │
│  │  │ Deployment  │ │ Deployment  │ │ Deployment  │        │
│  │  │  frontend   │ │   backend   │ │ mcp-server  │        │
│  │  └──────┬──────┘ └──────┬──────┘ └──────┬──────┘        │
│  │         │               │               │               │
│  │  ┌──────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐        │
│  │  │   Service   │ │   Service   │ │   Service   │        │
│  │  │  frontend   │ │   backend   │ │ mcp-server  │        │
│  │  │  :3000      │ │   :8000     │ │   :5001     │        │
│  │  └─────────────┘ └─────────────┘ └─────────────┘        │
│  └─────────────────────────────────────────────────────────┤
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Health Checks

### Liveness Probes

| Service | Path | Port | Initial Delay | Period |
|---------|------|------|---------------|--------|
| frontend | `/` | 3000 | 30s | 10s |
| backend | `/api/health` | 8000 | 30s | 10s |
| mcp-server | `/health` | 5001 | 30s | 10s |

### Readiness Probes

| Service | Path | Port | Initial Delay | Period |
|---------|------|------|---------------|--------|
| frontend | `/` | 3000 | 5s | 5s |
| backend | `/api/health` | 8000 | 5s | 5s |
| mcp-server | `/health` | 5001 | 5s | 5s |
