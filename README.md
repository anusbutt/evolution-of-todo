# Task Management Application with AI Chatbot

A modern, full-stack task management application featuring an AI-powered chatbot for natural language task management. Built with Next.js 16, FastAPI, and integrated with Google's Gemini AI. Deployable to Kubernetes using Helm.

## Features

### Core Features
- **User Authentication**: Secure signup/login with JWT tokens
- **Task Management**: Create, view, edit, delete, and complete tasks
- **Task Priorities**: P1 (High), P2 (Medium), P3 (Low) with color indicators
- **Task Tags**: Categorize tasks with colored tags (Work, Personal, Shopping, etc.)
- **Search & Filter**: Find tasks by title, filter by status/priority/tags
- **Sort Tasks**: Sort by date, priority, or title (ascending/descending)
- **User Isolation**: Each user manages their own tasks
- **Responsive Design**: Desktop, tablet, and mobile support
- **Dark Mode**: Glassmorphism UI with indigo/violet theme

### AI Chatbot (Phase 3)
- **Natural Language Task Creation**: "Add buy groceries urgently" (with priority detection)
- **Task Viewing**: "Show my tasks" (with priority indicators)
- **Task Completion**: "Mark task 1 as done"
- **Task Deletion**: "Delete task 2"
- **Task Updates**: "Change task 1 to buy milk"
- **Priority Support**: "Add urgent task" creates P1 priority

### Kubernetes Deployment (Phase 4)
- **Docker Containerization**: All services packaged as containers
- **Helm Chart**: One-command deployment to Kubernetes
- **Ingress Routing**: Single URL access (http://todo.local)
- **Self-Healing**: Automatic pod restart on failure
- **Zero-Downtime Updates**: Rolling deployment strategy
- **Configuration Management**: ConfigMaps and Secrets

### Cloud Native Deployment (Phase 5)
- **DigitalOcean Kubernetes (DOKS)**: Production-grade Kubernetes cluster
- **Event-Driven Architecture**: Dapr pub/sub with Redpanda Cloud (Kafka-compatible)
- **Audit Service**: Microservice consuming task events for audit logging
- **CI/CD Pipeline**: GitHub Actions for automated build, test, and deploy
- **Container Registry**: DigitalOcean Container Registry (DOCR)

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js 16, TypeScript, Tailwind CSS |
| Backend | FastAPI, Python 3.13+, SQLModel |
| Database | PostgreSQL 16+ (Neon Serverless) |
| AI | Google Gemini API (gemini-2.0-flash) |
| Auth | JWT with httpOnly cookies |
| Containers | Docker |
| Orchestration | Kubernetes (DOKS), Helm |
| Cloud Platform | DigitalOcean (DOKS, DOCR) |
| Event Streaming | Redpanda Cloud (Kafka-compatible) |
| Microservices | Dapr (Pub/Sub, Secrets) |
| CI/CD | GitHub Actions |

## Project Structure

```
hackathon_II/
├── frontend/                 # Next.js application
│   ├── app/                  # App Router pages
│   │   ├── (auth)/           # Login, Signup pages
│   │   └── (dashboard)/      # Protected task pages
│   ├── components/           # React components
│   │   ├── chat/             # AI chatbot components
│   │   ├── tasks/            # Task management (TaskFilters, TaskForm, etc.)
│   │   └── ui/               # UI primitives (PriorityBadge, TagChip, etc.)
│   ├── services/             # API service clients
│   └── types/                # TypeScript definitions
│
├── backend/                  # FastAPI application
│   ├── app/
│   │   ├── models/           # Database models (Task, Tag, AuditLog)
│   │   ├── schemas/          # Request/Response schemas
│   │   ├── services/         # Business logic
│   │   ├── routes/           # API endpoints (tasks, tags, audit)
│   │   ├── events/           # Event publishing (Dapr pub/sub)
│   │   └── middleware/       # Auth, CORS, rate limiting
│   ├── alembic/              # Database migrations
│   └── tests/                # Backend tests
│
├── mcp-server/               # MCP Tool Server (AI tools)
│   ├── tools/                # Task management tools (with priority)
│   ├── models/               # Shared models
│   └── server.py             # MCP server entry
│
├── services/                 # Microservices (Phase 5)
│   └── audit-service/        # Audit log consumer
│       ├── app/              # FastAPI + Dapr subscription
│       └── Dockerfile        # Production container
│
├── deployment/               # Kubernetes deployment
│   ├── helm/
│   │   └── todo-app/         # Helm chart
│   │       ├── values.yaml   # Local configuration
│   │       ├── values-prod.yaml  # DOKS production config
│   │       └── templates/    # K8s resources (+ audit-service, dapr)
│   └── digitalocean/         # DOKS setup documentation
│
├── .github/
│   └── workflows/
│       └── deploy.yml        # CI/CD pipeline (test → build → deploy)
│
├── specs/                    # Feature specifications
│   └── 005-phase-05-cloud-native/  # Current phase
│
└── history/                  # Development records
    ├── adr/                  # Architecture decisions
    └── prompts/              # Prompt history
```

## Quick Start

### Prerequisites
- Python 3.13+
- Node.js 22+
- PostgreSQL 16+ (or Neon account)
- Gemini API key

### 1. Environment Setup

**Backend** (`backend/.env`):
```env
DATABASE_URL=postgresql+asyncpg://user:pass@host/db?ssl=require
JWT_SECRET=your-secret-key
GEMINI_API_KEY=your-gemini-api-key
```

**Frontend** (`frontend/.env.local`):
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 2. Install Dependencies

```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### 3. Run Database Migrations

```bash
cd backend
alembic upgrade head
```

### 4. Start Services

```bash
# Terminal 1: Backend (port 8000)
cd backend
uvicorn app.main:app --reload --port 8000

# Terminal 2: Frontend (port 3000)
cd frontend
npm run dev
```

### 5. Access Application

Open http://localhost:3000

---

## Kubernetes Deployment (Phase 4)

Deploy the entire application to Kubernetes with a single command.

### Prerequisites

- Docker Desktop
- Minikube v1.32+
- kubectl v1.29+
- Helm v3.14+

### Quick Deploy

```bash
# 1. Start Minikube
minikube start --driver=docker
minikube addons enable ingress

# 2. Build Docker images
docker build -t todo-frontend:latest ./frontend
docker build -t todo-backend:latest ./backend
docker build -t todo-mcp-server:latest ./mcp-server

# 3. Load images into Minikube
minikube image load todo-frontend:latest
minikube image load todo-backend:latest
minikube image load todo-mcp-server:latest

# 4. Create secrets override file (override.yaml)
cat > deployment/helm/override.yaml << EOF
secrets:
  databaseUrl: "postgresql+asyncpg://user:pass@host/db?ssl=require"
  jwtSecret: "your-jwt-secret"
  geminiApiKey: "your-gemini-api-key"
EOF

# 5. Deploy with Helm
helm install todo-app ./deployment/helm/todo-app -n todo-app --create-namespace -f deployment/helm/override.yaml

# 6. Start tunnel (keep running)
minikube tunnel

# 7. Add to hosts file
# Windows: C:\Windows\System32\drivers\etc\hosts
# Linux/Mac: /etc/hosts
# Add: 127.0.0.1 todo.local

# 8. Access application
# Open: http://todo.local
```

### Kubernetes Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     KUBERNETES CLUSTER                          │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    NAMESPACE: todo-app                    │  │
│  │                                                           │  │
│  │   ┌─────────┐   ┌─────────┐   ┌─────────────┐            │  │
│  │   │Frontend │   │ Backend │   │ MCP-Server  │            │  │
│  │   │  :3000  │   │  :8000  │   │   :5001     │            │  │
│  │   └────┬────┘   └────┬────┘   └─────────────┘            │  │
│  │        │             │                                    │  │
│  │        └──────┬──────┘                                    │  │
│  │               │                                           │  │
│  │        ┌──────┴──────┐                                    │  │
│  │        │   INGRESS   │  /     → frontend                  │  │
│  │        │ todo.local  │  /api/* → backend                  │  │
│  │        └─────────────┘                                    │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Helm Commands

```bash
# Check deployment status
kubectl get pods -n todo-app

# View logs
kubectl logs -n todo-app -l app=backend

# Scale a service
kubectl scale deployment backend -n todo-app --replicas=3

# Upgrade deployment
helm upgrade todo-app ./deployment/helm/todo-app -n todo-app -f deployment/helm/override.yaml

# Rollback
helm rollback todo-app -n todo-app

# Uninstall
helm uninstall todo-app -n todo-app
kubectl delete namespace todo-app
```

### Docker Compose (Alternative)

For simpler local development without Kubernetes:

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## Cloud Native Deployment (Phase 5)

Deploy to DigitalOcean Kubernetes Service (DOKS) with event-driven architecture.

### Prerequisites

- DigitalOcean account with $200 credit
- `doctl` CLI installed and authenticated
- `kubectl` and `helm` installed
- Redpanda Cloud account (free tier)

### Setup Steps

```bash
# 1. Install doctl and authenticate
doctl auth init

# 2. Create DOKS cluster (Frankfurt region)
doctl kubernetes cluster create todo-app-cluster \
  --region fra1 \
  --node-pool "name=default;size=s-2vcpu-2gb;count=2"

# 3. Save kubeconfig
doctl kubernetes cluster kubeconfig save todo-app-cluster

# 4. Create Container Registry
doctl registry create todo-app-registry

# 5. Build and push images
doctl registry login
docker build -t registry.digitalocean.com/todo-app-registry/frontend:latest ./frontend
docker build -t registry.digitalocean.com/todo-app-registry/backend:latest ./backend
docker build -t registry.digitalocean.com/todo-app-registry/mcp-server:latest ./mcp-server
docker build -t registry.digitalocean.com/todo-app-registry/audit-service:latest ./services/audit-service
docker push registry.digitalocean.com/todo-app-registry/frontend:latest
docker push registry.digitalocean.com/todo-app-registry/backend:latest
docker push registry.digitalocean.com/todo-app-registry/mcp-server:latest
docker push registry.digitalocean.com/todo-app-registry/audit-service:latest

# 6. Integrate registry with cluster
doctl registry kubernetes-manifest | kubectl apply -f -

# 7. Install Dapr on cluster
dapr init -k

# 8. Create secrets
kubectl create namespace todo-app
kubectl create secret generic todo-secrets -n todo-app \
  --from-literal=database-url="$DATABASE_URL" \
  --from-literal=jwt-secret="$JWT_SECRET" \
  --from-literal=gemini-api-key="$GEMINI_API_KEY"
kubectl create secret generic redpanda-secrets -n todo-app \
  --from-literal=brokers="$REDPANDA_BROKERS" \
  --from-literal=username="$REDPANDA_USERNAME" \
  --from-literal=password="$REDPANDA_PASSWORD"

# 9. Deploy with Helm
helm upgrade --install todo-app ./deployment/helm/todo-app \
  -n todo-app \
  -f ./deployment/helm/todo-app/values-prod.yaml

# 10. Get Load Balancer IP
kubectl get svc frontend-service -n todo-app -w
```

### Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                  DIGITALOCEAN (Frankfurt - fra1)                            │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                     DOKS CLUSTER (todo-app namespace)                 │  │
│  │                                                                       │  │
│  │   ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐        │  │
│  │   │ Frontend │  │ Backend  │  │   MCP    │  │ Audit Service│        │  │
│  │   │ (Next.js)│  │ (FastAPI)│  │  Server  │  │  (FastAPI)   │        │  │
│  │   │ + Dapr   │  │ + Dapr   │  │ + Dapr   │  │   + Dapr     │        │  │
│  │   └────┬─────┘  └────┬─────┘  └──────────┘  └──────┬───────┘        │  │
│  │        │             │ PUBLISH               SUBSCRIBE │              │  │
│  │        │             └──────────┬───────────────────────┘             │  │
│  │        │                        ▼                                     │  │
│  │        │        ┌───────────────────────────────────┐                 │  │
│  │        │        │       REDPANDA CLOUD              │                 │  │
│  │        │        │   (task-events topic via Dapr)    │                 │  │
│  │        │        └───────────────────────────────────┘                 │  │
│  │        │                                                              │  │
│  │  ┌─────┴─────────────────────────────────────────────────────────┐   │  │
│  │  │              DIGITALOCEAN LOAD BALANCER                       │   │  │
│  │  │                  http://<IP>:3000                             │   │  │
│  │  └───────────────────────────────────────────────────────────────┘   │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/deploy.yml`) automates:

1. **Test**: Run pytest (backend) and vitest (frontend)
2. **Build**: Build and push Docker images to DOCR
3. **Deploy**: Helm upgrade to DOKS cluster
4. **Smoke Test**: Verify health checks pass

Configure these GitHub Secrets:
- `DIGITALOCEAN_ACCESS_TOKEN`
- `DATABASE_URL`
- `JWT_SECRET`
- `GEMINI_API_KEY`
- `REDPANDA_BROKERS`
- `REDPANDA_USERNAME`
- `REDPANDA_PASSWORD`

### Costs

- DOKS: ~$24/month (2 nodes × $12)
- Load Balancer: ~$12/month
- DOCR: Free tier (500MB)
- **Total**: ~$36/month ($200 credit = ~5 months)

---

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/auth/signup | Create account |
| POST | /api/auth/login | Login |
| POST | /api/auth/logout | Logout |
| GET | /api/auth/me | Current user |

### Tasks
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/tasks | List tasks (with priority/tags) |
| POST | /api/tasks | Create task (with priority, tag_ids) |
| PUT | /api/tasks/{id} | Update task (with priority, tag_ids) |
| DELETE | /api/tasks/{id} | Delete task |
| PATCH | /api/tasks/{id}/status | Toggle complete |
| GET | /api/tasks/stats | Task statistics |
| GET | /api/tasks/search | Search tasks by title/description |

### Tags
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/tags | List all tags |
| POST | /api/tags | Create tag (name, color) |
| DELETE | /api/tags/{id} | Delete tag |

### Audit (Phase 5)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/audit | List audit logs (task events) |

### Chat
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/chat | Send message to AI |

## Chat Commands

| Command | Example |
|---------|---------|
| Add task | "Add buy groceries" |
| List tasks | "Show my tasks" |
| Complete | "Mark task 1 as done" |
| Delete | "Delete task 2" |
| Update | "Change task 1 to buy milk" |

## Development

### Running Tests

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm test
```

### Code Quality

- Backend: Black, isort, mypy
- Frontend: ESLint, Prettier

## Troubleshooting

### Database Connection
```bash
# Ensure DATABASE_URL uses asyncpg driver
postgresql+asyncpg://user:pass@host/db?ssl=require
```

### Chat Not Working
1. Verify `GEMINI_API_KEY` is set in backend/.env
2. Check backend logs for API errors
3. Ensure user is logged in

### Build Errors
```bash
# Clear caches
rm -rf frontend/.next backend/__pycache__
npm install && pip install -r requirements.txt
```

## License

MIT License
