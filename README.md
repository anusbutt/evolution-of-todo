# Phase 2 - Full-Stack Web Application

A modern, scalable task management web application built with Next.js 16, FastAPI, and PostgreSQL. This project transforms the Phase 1 console application into a multi-user web platform with authentication, persistent storage, and responsive design.

## Features

- **User Authentication**: Secure signup/login with JWT tokens (7-day expiration)
- **Task Management**: Create, view, edit, delete, and mark tasks complete
- **User Isolation**: Each user sees only their own tasks
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices
- **Dark Mode**: Toggle between light and dark themes
- **Search**: Filter tasks by title or description
- **Statistics**: View task completion metrics

## Tech Stack

### Frontend
- **Framework**: Next.js 16+ (App Router)
- **Language**: TypeScript 5.0+
- **Styling**: Tailwind CSS 4+
- **Forms**: React Hook Form 7+ with Zod validation
- **Testing**: Vitest, React Testing Library, Playwright

### Backend
- **Framework**: FastAPI 0.115+
- **Language**: Python 3.13+
- **ORM**: SQLModel 0.0.22+
- **Database**: Neon Serverless PostgreSQL 16+
- **Migrations**: Alembic 1.13+
- **Testing**: pytest, pytest-asyncio, httpx

### Authentication
- **Library**: Better Auth (JWT tokens)
- **Storage**: httpOnly cookies (XSS protection)
- **Security**: SameSite=Strict, HTTPS enforced

## Project Structure

```
hackathon_II/
├── frontend/               # Next.js 16 application
│   ├── app/                # App Router pages
│   │   ├── (auth)/         # Authentication routes
│   │   └── (dashboard)/    # Protected dashboard routes
│   ├── components/         # Reusable React components
│   │   ├── ui/             # UI primitives (Button, Input, Modal)
│   │   ├── tasks/          # Task-specific components
│   │   ├── auth/           # Authentication forms
│   │   └── layout/         # Layout components (Header, Footer)
│   ├── lib/                # Utilities and API client
│   ├── types/              # TypeScript type definitions
│   └── tests/              # Unit and E2E tests
│
├── backend/                # FastAPI application
│   ├── app/
│   │   ├── models/         # SQLModel database models
│   │   ├── schemas/        # Pydantic request/response schemas
│   │   ├── services/       # Business logic layer
│   │   ├── routes/         # API endpoints
│   │   ├── middleware/     # Auth, CORS, rate limiting
│   │   └── utils/          # Security and helper functions
│   ├── alembic/            # Database migrations
│   └── tests/              # Unit, integration, contract tests
│
├── specs/                  # Feature specifications
└── history/                # Development history (ADRs, PHRs)
```

## Prerequisites

- **Python**: 3.13 or higher
- **Node.js**: 22.x or higher
- **PostgreSQL**: 16+ (via Neon or local)
- **Git**: For version control

## Setup Instructions

### 1. Clone Repository

```bash
git clone <repository-url>
cd hackathon_II
```

### 2. Backend Setup

**Option A: Using UV (Recommended)**
```bash
# Navigate to backend directory
cd backend

# Install UV (if not already installed)
# Windows:
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
# macOS/Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv sync

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Copy environment file and configure
cp .env.example .env
# Edit .env with your database credentials and JWT secret

# Initialize database migrations
alembic upgrade head

# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Option B: Using pip**
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file and configure
cp .env.example .env
# Edit .env with your database credentials and JWT secret

# Initialize database migrations
alembic upgrade head

# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at `http://localhost:8000`
API documentation at `http://localhost:8000/docs`

### 3. Frontend Setup

```bash
# Navigate to frontend directory (from project root)
cd frontend

# Install dependencies
npm install

# Copy environment file and configure
cp .env.local.example .env.local
# Edit .env.local with backend API URL (default: http://localhost:8000)

# Run development server
npm run dev
```

Frontend will be available at `http://localhost:3000`

### 4. Database Setup (Neon)

1. Sign up at [neon.tech](https://neon.tech)
2. Create a new project
3. Copy the connection string (format: `postgresql+asyncpg://...`)
4. Add to `backend/.env` as `DATABASE_URL`

### 5. Verify Setup

1. Backend: Visit `http://localhost:8000/health` - should return `{"status": "healthy"}`
2. Frontend: Visit `http://localhost:3000` - should show landing page
3. Database: Run `alembic current` in backend directory - should show migration version

## Development Workflow

### Running Tests

**Backend:**
```bash
cd backend
pytest                          # Run all tests
pytest --cov=app               # With coverage report
pytest tests/unit              # Unit tests only
pytest tests/integration       # Integration tests only
```

**Frontend:**
```bash
cd frontend
npm test                        # Run unit tests
npm run test:coverage          # With coverage report
npm run test:e2e               # Run E2E tests with Playwright
```

### Code Quality

**Backend:**
```bash
cd backend
ruff check .                    # Linting
black .                         # Formatting
```

**Frontend:**
```bash
cd frontend
npm run lint                    # ESLint
npm run format                  # Prettier
npm run type-check             # TypeScript check
```

### Database Migrations

```bash
cd backend

# Create new migration after model changes
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history
```

## Environment Variables

### Backend (.env)
- `DATABASE_URL`: PostgreSQL connection string (asyncpg format)
- `JWT_SECRET`: Secret key for JWT token signing
- `JWT_ALGORITHM`: Algorithm for JWT (default: HS256)
- `JWT_EXPIRATION_DAYS`: Token validity period (default: 7)
- `CORS_ORIGINS`: Allowed frontend origins (comma-separated)
- `ENVIRONMENT`: development/production
- `RATE_LIMIT_PER_MINUTE`: API rate limit per user (default: 100)

### Frontend (.env.local)
- `NEXT_PUBLIC_API_URL`: Backend API base URL

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Create new user account
- `POST /api/auth/login` - Login with email/password
- `POST /api/auth/logout` - Clear authentication session
- `GET /api/auth/me` - Get current user info (protected)

### Tasks
- `GET /api/tasks` - List all user's tasks (protected)
- `POST /api/tasks` - Create new task (protected)
- `GET /api/tasks/{id}` - Get task by ID (protected)
- `PUT /api/tasks/{id}` - Update task (protected)
- `DELETE /api/tasks/{id}` - Delete task (protected)
- `PATCH /api/tasks/{id}/status` - Toggle task completion (protected)
- `GET /api/tasks/stats` - Get task statistics (protected)
- `GET /api/tasks/search?q=query` - Search tasks (protected)

### Health
- `GET /health` - Health check endpoint

## Performance Goals

- API response time: < 500ms p95 for CRUD operations
- Page load time: < 2 seconds for task list (up to 500 tasks)
- Database query time: < 100ms for task listing
- Frontend bundle size: < 500KB initial load
- Concurrent users: 100 simultaneous users without degradation

## Security Features

- **JWT Tokens**: 7-day expiration with httpOnly cookies
- **Password Hashing**: Bcrypt/Argon2 via Better Auth
- **User Isolation**: All queries filter by user_id
- **Rate Limiting**: 100 requests/minute per user
- **Input Validation**: Dual-layer (client Zod + server Pydantic)
- **CORS**: Configured for frontend origin only
- **HTTPS**: Enforced in production
- **SQL Injection Prevention**: Parameterized queries via SQLModel

## Testing Coverage

- Minimum 75% code coverage (constitution requirement)
- Unit tests: Models, services, utilities
- Integration tests: API endpoints, database operations
- E2E tests: Critical user flows (signup → login → tasks → logout)

## Deployment

### Frontend (Vercel)
1. Connect GitHub repository to Vercel
2. Set `NEXT_PUBLIC_API_URL` environment variable
3. Deploy from `main` branch

### Backend (Options)
- **Vercel Serverless Functions**: Deploy alongside frontend
- **Railway/Render**: Deploy as persistent API service
- **AWS/GCP/Azure**: Deploy with container orchestration

### Database (Neon)
- Already hosted and configured
- Connection pooling: 10 pool + 20 overflow
- Automatic backups and scaling

## Troubleshooting

### Backend Issues

**Database Connection Error:**
```bash
# Verify DATABASE_URL format
postgresql+asyncpg://user:password@host:port/dbname

# Test connection
python -c "import asyncpg; print('asyncpg installed')"
```

**Migration Conflicts:**
```bash
# Reset to specific version
alembic downgrade <revision>

# Regenerate migration
alembic revision --autogenerate -m "description"
```

### Frontend Issues

**Build Errors:**
```bash
# Clear cache
rm -rf .next node_modules
npm install
npm run build
```

**API Connection Issues:**
```bash
# Verify NEXT_PUBLIC_API_URL in .env.local
echo $NEXT_PUBLIC_API_URL

# Check CORS settings in backend
```

## Contributing

1. Create feature branch from `main`
2. Implement changes following code quality standards
3. Run tests and ensure 75%+ coverage
4. Commit with descriptive messages
5. Create pull request with summary

## License

MIT License - see LICENSE file for details

## Documentation

- Feature Specification: `specs/002-phase-02-web-app/spec.md`
- Implementation Plan: `specs/002-phase-02-web-app/plan.md`
- Task Breakdown: `specs/002-phase-02-web-app/tasks.md`
- Architecture Decisions: `history/adr/`

## Support

For issues or questions:
1. Check troubleshooting section above
2. Review API documentation at `/docs` endpoint
3. Consult feature specifications in `specs/` directory
