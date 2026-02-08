# Phase 5: Cloud-Native Deployment

## Overview
Production deployment to DigitalOcean Kubernetes Service (DOKS) with automated CI/CD pipeline.

## Features
- ✅ Automated CI/CD with GitHub Actions
- ✅ Docker images pushed to DigitalOcean Container Registry (DOCR)
- ✅ Helm-based Kubernetes deployments
- ✅ Production-ready configuration
- ✅ Health checks and smoke tests
- ✅ Event-driven audit service (Dapr + Redpanda)

## Tech Stack
| Component | Technology |
|-----------|------------|
| Cloud Provider | DigitalOcean |
| Kubernetes | DOKS (DigitalOcean Kubernetes Service) |
| Container Registry | DOCR (DigitalOcean Container Registry) |
| CI/CD | GitHub Actions |
| Package Manager | Helm |
| Event Streaming | Redpanda (Kafka-compatible) |
| Sidecar | Dapr |

## Architecture
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              INTERNET                                        │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DIGITALOCEAN KUBERNETES (DOKS)                           │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        LoadBalancer                                  │   │
│  │                    (Public IP: 209.38.176.98)                       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  ┌──────────────────┐      ┌──────────────────┐     ┌─────────────────┐   │
│  │    FRONTEND      │ ───► │    BACKEND       │ ──► │   MCP SERVER    │   │
│  │    (Next.js)     │      │    (FastAPI)     │     │   (Python)      │   │
│  │    Port 3000     │      │    Port 8000     │     │   Port 3001     │   │
│  └──────────────────┘      └──────────────────┘     └─────────────────┘   │
│                                    │                        │              │
│                                    ▼                        ▼              │
│                            ┌──────────────────────────────────┐            │
│                            │         GEMINI AI API           │            │
│                            │      (Google Cloud - External)   │            │
│                            └──────────────────────────────────┘            │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                    ┌──────────────────────────────┐
                    │      NEON POSTGRESQL         │
                    │    (Managed Cloud DB)        │
                    └──────────────────────────────┘
```

## CI/CD Pipeline
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CI/CD PIPELINE                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Push to GitHub (main/master)                                               │
│         │                                                                    │
│         ▼                                                                    │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  STAGE 1: TEST                                                       │   │
│  │  • Python backend tests (pytest)                                     │   │
│  │  • Frontend tests (vitest)                                           │   │
│  │  • Linting (ruff, eslint)                                           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│         │                                                                    │
│         ▼                                                                    │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  STAGE 2: BUILD                                                      │   │
│  │  • docker build frontend → push to DOCR                             │   │
│  │  • docker build backend → push to DOCR                              │   │
│  │  • docker build mcp-server → push to DOCR                           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│         │                                                                    │
│         ▼                                                                    │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  STAGE 3: DEPLOY                                                     │   │
│  │  • helm upgrade --install to DOKS                                   │   │
│  │  • Apply secrets and configmaps                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│         │                                                                    │
│         ▼                                                                    │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  STAGE 4: SMOKE TEST                                                 │   │
│  │  • Health check frontend                                            │   │
│  │  • Health check backend API                                         │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Folder Structure
```
phase-05/
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions CI/CD pipeline
│
├── deployment/
│   └── helm/
│       └── todo-app/
│           └── values-prod.yaml # Production Helm values
│
├── services/
│   └── audit-service/          # Event-driven audit service
│       ├── Dockerfile
│       ├── main.py
│       └── requirements.txt
│
└── README.md
```

## Required Secrets (GitHub)
```
DIGITALOCEAN_ACCESS_TOKEN  # DigitalOcean API token
DATABASE_URL               # Neon PostgreSQL connection string
JWT_SECRET                 # JWT signing secret
GEMINI_API_KEY            # Google Gemini API key
```

## Deployment Commands
```bash
# Manual deployment (if needed)
doctl kubernetes cluster kubeconfig save todo-app-cluster

helm upgrade --install todo-app ./deployment/helm/todo-app \
  --namespace todo-app \
  --create-namespace \
  -f ./deployment/helm/todo-app/values-prod.yaml \
  --set secrets.databaseUrl="$DATABASE_URL" \
  --set secrets.jwtSecret="$JWT_SECRET" \
  --set secrets.geminiApiKey="$GEMINI_API_KEY"
```

## Live URL
```
http://209.38.176.98:3000
```

## Key Learnings
- CI/CD pipeline design with GitHub Actions
- Container registry management (DOCR)
- Kubernetes deployment with Helm
- Cloud-native architecture patterns
- Secrets management in Kubernetes
- Health checks and monitoring

## Built with ❤️ by anusbutt
