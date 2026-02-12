<div align="center">

# Evolution of Todo

### From Console to Cloud — A Full-Stack AI-Powered Task Manager

[![Live Demo](https://img.shields.io/badge/Live_Demo-Vercel-black?style=for-the-badge&logo=vercel)](https://evolution-of-todo.vercel.app)
[![Backend API](https://img.shields.io/badge/API-HuggingFace_Spaces-yellow?style=for-the-badge&logo=huggingface)](https://huggingface.co/spaces/anusbutt/todo-app)
[![GitHub](https://img.shields.io/badge/Source-GitHub-181717?style=for-the-badge&logo=github)](https://github.com/anusbutt/evolution-of-todo)

**Next.js 16** | **FastAPI** | **AI Chatbot** | **MCP Tools** | **Kubernetes** | **Neon PostgreSQL**

---

*A hackathon project demonstrating the evolution of a simple todo app through 5 progressive phases — from a Python console script to a cloud-native, AI-powered task management platform.*

</div>

---

## Highlights

- **AI-Powered Chatbot** — Manage tasks with natural language via an integrated AI assistant (Groq Llama 3.3 70B + MCP tool server)
- **Recurring Tasks** — Set daily, weekly, or monthly recurrence; completing a task auto-creates the next instance
- **Glassmorphism UI** — Modern dark-mode interface with frosted-glass cards, indigo/violet gradients, and smooth animations
- **Multi-Language** — Responds in English and Urdu based on user input
- **Spec-Driven Development** — Every line of code traces back to a spec, plan, and task ID

---

## Features

### Task Management
| Feature | Description |
|---------|-------------|
| **CRUD Operations** | Create, read, update, and delete tasks with a polished form UI |
| **Priority Levels** | P1 (High), P2 (Medium), P3 (Low) with color-coded badges and borders |
| **Recurring Tasks** | Daily / Weekly / Monthly recurrence — auto-creates next instance on completion |
| **Tags** | Categorize tasks with colored tags (Work, Personal, Shopping, Health, etc.) |
| **Search & Filter** | Full-text search, filter by status / priority / tags, sort by date / priority / title |
| **URL Persistence** | Filter and sort state saved in the URL — shareable and bookmarkable |
| **Statistics** | Real-time task stats with completion percentage and priority breakdown |

### AI Chatbot
| Feature | Description |
|---------|-------------|
| **Natural Language** | "Add a daily task to drink water" — creates a recurring P2 task |
| **Smart Completion** | "Mark buy groceries as done" — looks up the task and completes it |
| **Priority Detection** | "Add an urgent task to fix the bug" — creates as P1 |
| **Task Listing** | "Show my tasks" — formatted list with priority and status |
| **Bilingual** | Detects Urdu and responds in Urdu; defaults to English |
| **MCP Architecture** | Tools exposed via Model Context Protocol (stdio transport) |

### Authentication & Security
| Feature | Description |
|---------|-------------|
| **JWT Auth** | Secure signup/login with httpOnly cookie tokens |
| **User Isolation** | Each user sees only their own tasks |
| **Rate Limiting** | 100 requests/minute per user |
| **Security Headers** | X-Content-Type-Options, X-Frame-Options, HSTS in production |
| **CORS** | Configured for production and development origins |

### UI / UX
| Feature | Description |
|---------|-------------|
| **Dark Mode** | Glassmorphism design with backdrop blur and gradient accents |
| **Responsive** | Mobile-first layout — works on phones, tablets, and desktops |
| **Animations** | Staggered list animations, hover lifts, smooth transitions |
| **Accessible** | Keyboard navigation, ARIA labels, focus management |

---

## Tech Stack

<div align="center">

| Layer | Technology |
|:------|:-----------|
| **Frontend** | Next.js 16, React 19, TypeScript, Tailwind CSS 4 |
| **Backend** | FastAPI, Python 3.13, SQLModel, Pydantic v2 |
| **Database** | Neon PostgreSQL (serverless), Alembic migrations |
| **AI/LLM** | Groq (Llama 3.3 70B), OpenAI Agents SDK |
| **MCP Server** | Model Context Protocol (stdio transport), 5 task tools |
| **Auth** | JWT with httpOnly cookies, bcrypt password hashing |
| **Hosting** | Vercel (frontend), HuggingFace Spaces (backend) |
| **Containers** | Docker, Kubernetes (Helm), Minikube |
| **CI/CD** | GitHub Actions |

</div>

---

## The 5 Phases

This project was built incrementally, each phase adding a new layer of complexity:

```
Phase I    Console Todo App          Python, in-memory, pytest
    |
Phase II   Full-Stack Web App        Next.js + FastAPI + Neon DB
    |
Phase III  AI Chatbot Integration    OpenAI Agents SDK + MCP Tools
    |
Phase IV   Kubernetes Deployment     Minikube + Helm + Ingress
    |
Phase V    Cloud-Native Platform     HF Spaces + Vercel + CI/CD
```

---

## Quick Start

### Prerequisites

- Python 3.13+
- Node.js 22+
- PostgreSQL 16+ (or a [Neon](https://neon.tech) account)

### 1. Clone & Configure

```bash
git clone https://github.com/anusbutt/evolution-of-todo.git
cd evolution-of-todo
```

**Backend** — create `phase-02/backend/.env`:
```env
DATABASE_URL=postgresql+asyncpg://user:pass@host/db?ssl=require
JWT_SECRET=your-secret-key
GROQ_API_KEY=your-groq-api-key
```

**Frontend** — create `phase-02/frontend/.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 2. Install & Run

```bash
# Backend
cd phase-02/backend
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8000

# Frontend (new terminal)
cd phase-02/frontend
npm install
npm run dev
```

### 3. Open

Visit **http://localhost:3000** — sign up, create tasks, and chat with the AI.

---

## Project Structure

```
evolution-of-todo/
|
+-- phase-01/                        # Phase I: Console App
|   +-- todo.py                      # CLI todo manager
|   +-- tests/                       # pytest test suite
|
+-- phase-02/                        # Phase II-V: Web App
|   +-- frontend/                    # Next.js 16 application
|   |   +-- app/(auth)/              # Login & Signup pages
|   |   +-- app/(dashboard)/tasks/   # Main task management page
|   |   +-- components/
|   |   |   +-- chat/                # AI chatbot sidebar
|   |   |   +-- tasks/               # TaskForm, TaskItem, TaskList, TaskFilters, TaskStats
|   |   |   +-- ui/                  # Reusable UI primitives
|   |   +-- types/                   # TypeScript type definitions
|   |   +-- services/                # API client & chat service
|   |
|   +-- backend/                     # FastAPI application
|   |   +-- app/
|   |   |   +-- models/              # SQLModel: Task, User, Tag, AuditLog
|   |   |   +-- schemas/             # Pydantic request/response schemas
|   |   |   +-- services/            # Business logic (task, chat, user)
|   |   |   +-- routes/              # REST API endpoints
|   |   |   +-- middleware/           # Auth, CORS, rate limiting
|   |   +-- mcp_server/              # MCP Tool Server (stdio)
|   |   |   +-- tools.py             # 5 task management tools
|   |   |   +-- server_stdio.py      # MCP stdio transport entrypoint
|   |   +-- alembic/                 # Database migrations
|   |
|   +-- deployment/                  # Kubernetes (Helm chart)
|
+-- specs/                           # SDD feature specifications
+-- history/                         # Prompt history & ADRs
+-- .specify/                        # SpecKit Plus templates
```

---

## API Reference

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/auth/signup` | Create a new account |
| `POST` | `/api/auth/login` | Login (sets httpOnly cookie) |
| `POST` | `/api/auth/logout` | Logout (clears cookie) |
| `GET` | `/api/auth/me` | Get current user |

### Tasks
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/tasks` | List all tasks |
| `POST` | `/api/tasks` | Create task (title, priority, tags, recurrence) |
| `PUT` | `/api/tasks/{id}` | Update task |
| `DELETE` | `/api/tasks/{id}` | Delete task |
| `PATCH` | `/api/tasks/{id}/status` | Toggle completion (triggers recurrence) |
| `GET` | `/api/tasks/stats` | Task statistics |
| `GET` | `/api/tasks/search?q=` | Search by title/description |

### Tags
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/tags` | List all tags |
| `POST` | `/api/tags` | Create tag (name, color) |
| `DELETE` | `/api/tags/{id}` | Delete tag |

### Chat
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/chat` | Send message to AI chatbot |

---

## AI Chat Examples

```
You:   Add a weekly task to review PRs
Bot:   Done! I've added "review PRs" as a weekly recurring task (due next week).

You:   Show my tasks
Bot:   Here are your tasks:
       1. review PRs [P2] [Weekly] - Due: Feb 19
       2. buy groceries [P2] - Completed

You:   Mark review PRs as done
Bot:   Done! "review PRs" marked as complete.
       Next occurrence created (due Feb 26).

You:   مجھے ایک ٹاسک بنا دو پانی پینا
Bot:   میں نے "پانی پینا" ٹاسک بنا دیا ہے۔
```

---

## Development Methodology

This project follows **Spec-Driven Development (SDD)** — every feature flows through a strict loop:

```
Constitution  -->  Spec  -->  Plan  -->  Tasks  -->  Implementation
   (WHY)          (WHAT)     (HOW)    (BREAKDOWN)     (CODE)
```

- Every code file references its Task ID: `[Task]: T110 [US11]`
- Architecture decisions are recorded as ADRs in `history/adr/`
- Every AI interaction is logged as a PHR in `history/prompts/`

---

## Deployment

### Current Production Setup

| Component | Platform | URL |
|-----------|----------|-----|
| Frontend | Vercel | [evolution-of-todo.vercel.app](https://evolution-of-todo.vercel.app) |
| Backend | HuggingFace Spaces | [huggingface.co/spaces/anusbutt/todo-app](https://huggingface.co/spaces/anusbutt/todo-app) |
| Database | Neon PostgreSQL | Serverless (auto-scaling) |

### Kubernetes (Local)

```bash
minikube start --driver=docker
minikube addons enable ingress
helm install todo-app ./phase-02/deployment/helm/todo-app -n todo-app --create-namespace
minikube tunnel
# Visit http://todo.local
```

---

## License

MIT License

---

<div align="center">

**Built with passion at Hackathon II**

Made with Next.js, FastAPI, and a lot of AI

</div>
