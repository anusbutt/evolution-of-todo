# Phase 0 Research: Phase 2 - Full-Stack Web Application

**Feature**: 002-phase-02-web-app
**Date**: 2026-01-13
**Purpose**: Document technical research, design decisions, and best practices for Phase 2 implementation

## Research Topics

### 1. Better Auth Integration (Python + TypeScript)

**Decision**: Use Better Auth with JWT tokens stored in httpOnly cookies

**Research Findings**:
- **Better Auth** is a comprehensive authentication library with built-in support for:
  - Password hashing (bcrypt/argon2)
  - JWT token generation and validation
  - Cookie management (httpOnly, SameSite, Secure flags)
  - Cross-platform support (Python + TypeScript)

**Implementation Pattern**:

**Backend (Python)**:
```python
from better_auth import BetterAuth, JWTConfig

# Initialize Better Auth
auth = BetterAuth(
    secret_key=os.getenv("JWT_SECRET"),
    jwt_config=JWTConfig(
        expiration_days=7,
        algorithm="HS256"
    )
)

# Signup
async def signup(email: str, name: str, password: str):
    # Hash password
    password_hash = auth.hash_password(password)
    # Create user in database
    user = await create_user(email, name, password_hash)
    # Generate JWT token
    token = auth.generate_token(user_id=user.id)
    return token

# Login
async def login(email: str, password: str):
    user = await get_user_by_email(email)
    if not user or not auth.verify_password(password, user.password_hash):
        raise InvalidCredentialsError()
    token = auth.generate_token(user_id=user.id)
    return token

# Verify token middleware
async def verify_token(token: str) -> int:
    payload = auth.decode_token(token)
    return payload["user_id"]
```

**Frontend (TypeScript)**:
```typescript
// Better Auth client config
import { BetterAuthClient } from "@better-auth/client";

export const authClient = new BetterAuthClient({
  apiUrl: process.env.NEXT_PUBLIC_API_URL,
  tokenStorageType: "cookie", // httpOnly
});

// Signup
async function signup(email: string, name: string, password: string) {
  const response = await authClient.signup({ email, name, password });
  // Token automatically stored in httpOnly cookie
  return response;
}

// Login
async function login(email: string, password: string) {
  const response = await authClient.login({ email, password });
  // Token automatically stored in httpOnly cookie
  return response;
}

// Logout
async function logout() {
  await authClient.logout();
  // Token automatically cleared from cookie
}
```

**Rationale**:
- **httpOnly cookies** prevent XSS attacks (JavaScript cannot access token)
- **SameSite=Strict** prevents CSRF attacks
- **Secure flag** ensures HTTPS-only transmission
- **7-day expiration** balances security and convenience
- **Stateless JWT** enables horizontal scalability (no server-side session storage)

**Alternatives Considered**:
- **Local storage JWT**: Rejected due to XSS vulnerability
- **Session-based auth**: Rejected due to server-side state requirement

---

### 2. SQLModel Async Query Best Practices

**Decision**: Use SQLModel with async/await for all database operations

**Research Findings**:
- SQLModel provides async support via SQLAlchemy's async engine
- Async operations prevent blocking during I/O-bound database queries
- Connection pooling essential for concurrent requests

**Implementation Pattern**:

**Database Setup**:
```python
from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession, AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

# Create async engine with connection pooling
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Log SQL queries in development
    pool_size=10,  # Max 10 connections
    max_overflow=20,  # Allow 20 overflow connections
    pool_pre_ping=True,  # Verify connections before use
)

# Create async session factory
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Dependency for FastAPI routes
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
```

**Model Definition**:
```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    name: str = Field(max_length=255)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    tasks: list["Task"] = Relationship(back_populates="user")

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200)
    description: str = Field(default="", max_length=1000)
    completed: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    user: Optional[User] = Relationship(back_populates="tasks")
```

**CRUD Operations**:
```python
from sqlmodel import select

# Create
async def create_task(session: AsyncSession, task_data: dict) -> Task:
    task = Task(**task_data)
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task

# Read (list with user_id filter)
async def get_tasks_by_user(session: AsyncSession, user_id: int) -> list[Task]:
    statement = select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc())
    results = await session.exec(statement)
    return results.all()

# Read (single)
async def get_task_by_id(session: AsyncSession, task_id: int, user_id: int) -> Optional[Task]:
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    result = await session.exec(statement)
    return result.first()

# Update
async def update_task(session: AsyncSession, task_id: int, user_id: int, updates: dict) -> Task:
    task = await get_task_by_id(session, task_id, user_id)
    if not task:
        raise TaskNotFoundError()
    for key, value in updates.items():
        setattr(task, key, value)
    task.updated_at = datetime.utcnow()
    await session.commit()
    await session.refresh(task)
    return task

# Delete
async def delete_task(session: AsyncSession, task_id: int, user_id: int) -> None:
    task = await get_task_by_id(session, task_id, user_id)
    if not task:
        raise TaskNotFoundError()
    await session.delete(task)
    await session.commit()
```

**Rationale**:
- **Async queries** prevent blocking, allow concurrent requests
- **Connection pooling** reuses connections for efficiency
- **Index on user_id, completed, created_at** optimizes common queries
- **User isolation enforced** at query level (WHERE user_id = :user_id)

**Alternatives Considered**:
- **Synchronous SQLModel**: Rejected due to blocking I/O
- **Raw SQL**: Rejected due to SQL injection risk and no type safety

---

### 3. Next.js App Router Auth Middleware Patterns

**Decision**: Use Next.js middleware for route protection with JWT validation

**Research Findings**:
- Next.js middleware runs before rendering pages (server-side)
- Middleware can read cookies and redirect before page loads
- Centralized auth logic in single `middleware.ts` file

**Implementation Pattern**:

**Middleware Configuration** (`middleware.ts`):
```typescript
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

// Protected routes that require authentication
const protectedRoutes = ["/tasks"];

// Public routes that redirect if already authenticated
const publicAuthRoutes = ["/login", "/signup"];

export function middleware(request: NextRequest) {
  const token = request.cookies.get("auth-token");
  const { pathname } = request.nextUrl;

  // Check if route is protected
  if (protectedRoutes.some((route) => pathname.startsWith(route))) {
    if (!token) {
      // Redirect to login if no token
      return NextResponse.redirect(new URL("/login", request.url));
    }
    // TODO: Optionally verify token validity with backend
    // For now, assume token presence = authenticated
  }

  // Redirect authenticated users away from auth pages
  if (publicAuthRoutes.some((route) => pathname.startsWith(route))) {
    if (token) {
      return NextResponse.redirect(new URL("/tasks", request.url));
    }
  }

  return NextResponse.next();
}

// Specify which routes middleware should run on
export const config = {
  matcher: [
    /*
     * Match all paths except static files and APIs
     */
    "/((?!api|_next/static|_next/image|favicon.ico).*)",
  ],
};
```

**API Client with Token Handling** (`lib/api-client.ts`):
```typescript
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

class ApiClient {
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      credentials: "include", // Include cookies in requests
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
    });

    if (!response.ok) {
      // Handle 401 Unauthorized (expired token)
      if (response.status === 401) {
        // Redirect to login
        window.location.href = "/login";
        throw new Error("Session expired");
      }

      const error = await response.json();
      throw new Error(error.message || "Request failed");
    }

    return response.json();
  }

  // Auth endpoints
  async signup(email: string, name: string, password: string) {
    return this.request("/auth/signup", {
      method: "POST",
      body: JSON.stringify({ email, name, password }),
    });
  }

  async login(email: string, password: string) {
    return this.request("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });
  }

  async logout() {
    return this.request("/auth/logout", { method: "POST" });
  }

  // Task endpoints
  async getTasks() {
    return this.request<Task[]>("/api/tasks");
  }

  async createTask(title: string, description: string) {
    return this.request<Task>("/api/tasks", {
      method: "POST",
      body: JSON.stringify({ title, description }),
    });
  }

  async updateTask(taskId: number, updates: Partial<Task>) {
    return this.request<Task>(`/api/tasks/${taskId}`, {
      method: "PUT",
      body: JSON.stringify(updates),
    });
  }

  async deleteTask(taskId: number) {
    return this.request(`/api/tasks/${taskId}`, { method: "DELETE" });
  }

  async toggleTaskComplete(taskId: number, completed: boolean) {
    return this.request<Task>(`/api/tasks/${taskId}/complete`, {
      method: "PATCH",
      body: JSON.stringify({ completed }),
    });
  }
}

export const apiClient = new ApiClient();
```

**Rationale**:
- **Middleware runs server-side** before page render (fast redirect)
- **Cookie-based auth** automatically included in requests
- **Centralized protection** logic in single file
- **Redirects prevent** unauthorized page access

**Alternatives Considered**:
- **Client-side useEffect checking**: Rejected due to flash of unauthorized content
- **Server components checking**: Possible but middleware is more centralized

---

### 4. Neon PostgreSQL Connection Pooling Configuration

**Decision**: Use Neon's built-in connection pooling with asyncpg driver

**Research Findings**:
- Neon Serverless PostgreSQL provides built-in connection pooling
- Connection string format: `postgresql://user:pass@host/db?sslmode=require`
- Recommended pool size: 10-20 connections for typical web apps
- Use asyncpg driver for async Python support

**Implementation Pattern**:

**Environment Configuration** (`.env`):
```bash
# Neon PostgreSQL connection string
DATABASE_URL=postgresql+asyncpg://user:password@ep-cool-forest-123456.us-east-2.aws.neon.tech/dbname?sslmode=require

# JWT configuration
JWT_SECRET=your-secret-key-here-change-in-production

# CORS configuration
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
```

**Database Connection** (`database.py`):
```python
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

# Create async engine with connection pooling
engine = create_async_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL query logging in development
    pool_size=10,  # Number of persistent connections
    max_overflow=20,  # Additional connections when pool exhausted
    pool_timeout=30,  # Seconds to wait for available connection
    pool_recycle=3600,  # Recycle connections after 1 hour
    pool_pre_ping=True,  # Verify connection health before use
)

# Create async session factory
async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Don't expire objects after commit
)

# Create tables (run once on startup)
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

# FastAPI dependency
async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
```

**FastAPI Integration** (`main.py`):
```python
from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    await create_db_and_tables()
    yield
    # Shutdown: Close engine
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

# Use session in routes
@app.get("/api/tasks")
async def get_tasks(
    session: AsyncSession = Depends(get_session),
    user_id: int = Depends(get_current_user_id)
):
    tasks = await get_tasks_by_user(session, user_id)
    return tasks
```

**Rationale**:
- **Connection pooling** reuses connections, reduces latency
- **pool_pre_ping** prevents using stale connections
- **pool_recycle** prevents long-lived connection issues
- **Neon handles** additional pooling at infrastructure level

**Alternatives Considered**:
- **No pooling**: Rejected due to poor performance (connection overhead)
- **PGBouncer**: Not needed with Neon's built-in pooling

---

### 5. Rate Limiting Implementation Strategies

**Decision**: Use slowapi for rate limiting with Redis or in-memory backend

**Research Findings**:
- Rate limiting prevents abuse and DoS attacks
- Constitution requires 100 requests/minute per user
- slowapi integrates with FastAPI seamlessly
- Can use Redis for distributed rate limiting or in-memory for simplicity

**Implementation Pattern**:

**Simple In-Memory Rate Limiting** (`middleware/rate_limit.py`):
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Initialize limiter
limiter = Limiter(
    key_func=get_remote_address,  # Or use user_id from JWT
    default_limits=["100/minute"],  # Constitution requirement
)

# FastAPI integration
from fastapi import FastAPI, Request

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Apply to routes
from slowapi import Limiter

@app.get("/api/tasks")
@limiter.limit("100/minute")
async def get_tasks(request: Request):
    return {"tasks": []}
```

**User-Based Rate Limiting** (Better for authenticated APIs):
```python
def get_user_id_from_token(request: Request) -> str:
    token = request.cookies.get("auth-token")
    if not token:
        return get_remote_address(request)  # Fallback to IP
    try:
        payload = auth.decode_token(token)
        return f"user:{payload['user_id']}"
    except:
        return get_remote_address(request)

limiter = Limiter(
    key_func=get_user_id_from_token,
    default_limits=["100/minute"],
)
```

**Rationale**:
- **100 requests/minute** as specified in constitution
- **Per-user limiting** better than per-IP for authenticated APIs
- **In-memory** sufficient for Phase 2 (single instance)
- **Graceful failure** returns 429 Too Many Requests

**Alternatives Considered**:
- **Redis-backed**: Deferred to Phase 4/5 (multi-instance)
- **Nginx rate limiting**: Deferred to Phase 4/5 (infrastructure level)

---

## Design Decision Summary

| Topic | Decision | Rationale |
|-------|----------|-----------|
| **Authentication** | Better Auth + JWT + httpOnly cookies | XSS prevention, stateless, constitution-compliant |
| **Database ORM** | SQLModel with async queries | Type-safe, SQL injection prevention, async performance |
| **Frontend Routing** | Next.js App Router + middleware | Server-side protection, file-based routing, SEO-friendly |
| **Connection Pooling** | Neon built-in + asyncpg (10 pool, 20 overflow) | Efficient connection reuse, low latency |
| **Rate Limiting** | slowapi in-memory (100 req/min per user) | Constitution-compliant, simple for Phase 2 |

---

## Security Considerations

### 1. JWT Token Security
- ✅ **httpOnly cookies**: Prevent XSS attacks (JS cannot access)
- ✅ **SameSite=Strict**: Prevent CSRF attacks
- ✅ **Secure flag**: HTTPS-only transmission in production
- ✅ **7-day expiration**: Balance security and convenience
- ✅ **Secret key**: Strong random key from environment variable

### 2. Database Security
- ✅ **Parameterized queries**: SQLModel ORM prevents SQL injection
- ✅ **User isolation**: All queries filter by user_id from JWT
- ✅ **Foreign keys**: Enforce referential integrity
- ✅ **SSL mode required**: Encrypted database connections

### 3. Input Validation
- ✅ **Client-side**: Zod schemas for immediate feedback
- ✅ **Server-side**: Pydantic schemas for security (never trust client)
- ✅ **Max lengths**: Title (200 chars), description (1000 chars)
- ✅ **Required fields**: Title non-empty, email valid format

### 4. CORS Configuration
- ✅ **Allowed origins**: Whitelist frontend domains only
- ✅ **Credentials**: Allow cookies in CORS requests
- ✅ **Methods**: Restrict to GET, POST, PUT, DELETE, PATCH
- ✅ **Headers**: Restrict to Content-Type, Authorization

---

## Performance Optimization Strategies

### 1. Database Indexes
```sql
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
CREATE INDEX idx_tasks_created_at ON tasks(created_at DESC);
```
**Impact**: 10-100x faster query performance for filtered/sorted queries

### 2. Connection Pooling
- **Pool size**: 10 persistent connections
- **Max overflow**: 20 additional connections
- **Impact**: 50-100ms latency reduction per query

### 3. Frontend Bundle Optimization
- **Code splitting**: Lazy load route components
- **Tree shaking**: Remove unused dependencies
- **Image optimization**: Next.js automatic optimization
- **Target**: < 500KB initial bundle size

### 4. API Response Caching
- **Deferred to Phase 3**: Redis caching layer
- **Phase 2**: Fresh data on every request (simpler, acceptable for MVP)

---

## Testing Strategy

### Backend Testing
- **Unit tests**: Models, services (80% coverage target)
- **Integration tests**: API endpoints with test database
- **Contract tests**: Validate OpenAPI schema compliance

### Frontend Testing
- **Component tests**: Vitest + React Testing Library
- **E2E tests**: Playwright for critical user flows
- **Visual regression**: Deferred to Phase 3

### Test Database
- **Separate test database**: Avoid polluting development data
- **Fixtures**: Pytest fixtures for common test data
- **Cleanup**: Truncate tables after each test

---

## Development Workflow

### 1. Backend Development
```bash
cd backend
uv venv
source .venv/bin/activate  # or .venv\Scripts\Activate.ps1 on Windows
uv pip install -r requirements.txt
uvicorn app.main:app --reload  # Runs on http://localhost:8000
```

### 2. Frontend Development
```bash
cd frontend
npm install  # or pnpm install, yarn install
npm run dev  # Runs on http://localhost:3000
```

### 3. Database Migrations
```bash
cd backend
alembic revision --autogenerate -m "Create users and tasks tables"
alembic upgrade head
```

### 4. Running Tests
```bash
# Backend tests
cd backend
pytest --cov=app --cov-report=term-missing

# Frontend tests
cd frontend
npm test  # Unit tests
npm run test:e2e  # E2E tests
```

---

## Deployment Considerations

### Environment Variables

**Backend** (`.env`):
```bash
DATABASE_URL=postgresql+asyncpg://...
JWT_SECRET=your-secret-key
CORS_ORIGINS=https://yourdomain.com
ENVIRONMENT=production
```

**Frontend** (`.env.local`):
```bash
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```

### Vercel Deployment

**Frontend**:
- Connect GitHub repository
- Set environment variables in Vercel dashboard
- Automatic deployments on push to main

**Backend**:
- Deploy as Vercel Serverless Function or dedicated API host
- Configure CORS to allow frontend domain
- Set DATABASE_URL to Neon connection string

---

## Conclusion

All technical unknowns have been researched and documented. Key decisions:
- **Authentication**: Better Auth + JWT + httpOnly cookies
- **Database**: SQLModel + async queries + connection pooling
- **Frontend**: Next.js App Router + middleware auth
- **Rate limiting**: slowapi in-memory (100 req/min)

**Next Phase**: Create data-model.md and API contracts (Phase 1)
