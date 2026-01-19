# Task Management Application with AI Chatbot

A modern, full-stack task management application featuring an AI-powered chatbot for natural language task management. Built with Next.js 16, FastAPI, and integrated with Google's Gemini AI.

## Features

### Core Features
- **User Authentication**: Secure signup/login with JWT tokens
- **Task Management**: Create, view, edit, delete, and complete tasks
- **User Isolation**: Each user manages their own tasks
- **Responsive Design**: Desktop, tablet, and mobile support
- **Dark Mode**: Light/dark theme toggle

### AI Chatbot (Phase 3)
- **Natural Language Task Creation**: "Add buy groceries"
- **Task Viewing**: "Show my tasks"
- **Task Completion**: "Mark task 1 as done"
- **Task Deletion**: "Delete task 2"
- **Task Updates**: "Change task 1 to buy milk"

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js 16, TypeScript, Tailwind CSS |
| Backend | FastAPI, Python 3.13+, SQLModel |
| Database | PostgreSQL 16+ (Neon Serverless) |
| AI | Google Gemini API (gemini-2.0-flash) |
| Auth | JWT with httpOnly cookies |

## Project Structure

```
hackathon_II/
├── frontend/                 # Next.js application
│   ├── app/                  # App Router pages
│   │   ├── (auth)/           # Login, Signup pages
│   │   └── (dashboard)/      # Protected task pages
│   ├── components/           # React components
│   │   ├── chat/             # AI chatbot components
│   │   ├── tasks/            # Task management components
│   │   ├── ui/               # UI primitives
│   │   └── layout/           # Header, Footer
│   ├── services/             # API service clients
│   ├── lib/                  # Utilities
│   └── types/                # TypeScript definitions
│
├── backend/                  # FastAPI application
│   ├── app/
│   │   ├── models/           # Database models
│   │   ├── schemas/          # Request/Response schemas
│   │   ├── services/         # Business logic
│   │   ├── routes/           # API endpoints
│   │   ├── middleware/       # Auth, CORS, rate limiting
│   │   └── utils/            # Helpers
│   ├── alembic/              # Database migrations
│   └── tests/                # Backend tests
│
├── mcp-server/               # MCP Tool Server (AI tools)
│   ├── tools/                # Task management tools
│   ├── models/               # Shared models
│   └── server.py             # MCP server entry
│
├── specs/                    # Feature specifications
│   ├── 002-phase-02-web-app/
│   └── 003-phase-03-ai-chatbot/
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
| GET | /api/tasks | List tasks |
| POST | /api/tasks | Create task |
| PUT | /api/tasks/{id} | Update task |
| DELETE | /api/tasks/{id} | Delete task |
| PATCH | /api/tasks/{id}/status | Toggle complete |
| GET | /api/tasks/stats | Task statistics |

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
