# Quickstart Guide: Phase 3 - AI Chatbot

**Date**: 2026-01-15
**Feature**: 003-phase-03-ai-chatbot

## Prerequisites

- Phase 2 running (Frontend, Backend, PostgreSQL)
- Gemini API key
- Python 3.12+
- Node.js 18+

---

## Setup Steps

### 1. Get Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a new API key
3. Copy the key for use in environment variables

### 2. Configure Environment Variables

**Backend (.env additions)**:
```bash
# Add to existing backend/.env
GEMINI_API_KEY=your-gemini-api-key
MCP_SERVER_URL=http://localhost:5001
```

**MCP Server (.env)**:
```bash
# Create mcp-server/.env
DATABASE_URL=postgresql+asyncpg://neondb_owner:xxx@ep-xxx.neon.tech/neondb
MCP_PORT=5001
```

### 3. Install Dependencies

**Backend**:
```bash
cd backend
pip install openai-agents-sdk
```

**MCP Server**:
```bash
cd mcp-server
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Run Database Migration

```bash
cd backend
alembic upgrade head  # Adds conversations and messages tables
```

### 5. Start Services

**Terminal 1 - MCP Server**:
```bash
cd mcp-server
python server.py
# Server running on http://localhost:5001
```

**Terminal 2 - Backend**:
```bash
cd backend
uvicorn app.main:app --reload --port 8000
# API running on http://localhost:8000
```

**Terminal 3 - Frontend**:
```bash
cd frontend
npm run dev
# Frontend running on http://localhost:3000
```

---

## Verify Setup

### Test MCP Server

```bash
# MCP server health check
curl http://localhost:5001/health
# Expected: {"status": "ok"}
```

### Test Chat API

```bash
# First, login to get JWT token
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "yourpassword"}' \
  -c cookies.txt

# Then test chat endpoint
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"message": "Show my tasks"}'

# Expected: JSON response with AI assistant message
```

### Test via UI

1. Open http://localhost:3000
2. Login with your credentials
3. Click the chat button (bottom right)
4. Type "Show my tasks"
5. Verify assistant responds

---

## Troubleshooting

### MCP Server Won't Start

```bash
# Check port availability
lsof -i :5001

# Check DATABASE_URL is correct
python -c "from config import settings; print(settings.database_url)"
```

### Chat Returns 500 Error

```bash
# Check Gemini API key
curl "https://generativelanguage.googleapis.com/v1beta/models?key=YOUR_API_KEY"

# Check MCP server is running
curl http://localhost:5001/health

# Check backend logs for errors
tail -f backend/logs/app.log
```

### Chat Sidebar Not Showing

```bash
# Clear Next.js cache and rebuild
cd frontend
rm -rf .next
npm run dev
```

### Database Connection Error

```bash
# Verify DATABASE_URL format
# Should be: postgresql+asyncpg://user:pass@host/db

# Test connection
cd backend
python -c "from app.database import engine; print('OK')"
```

---

## Service Ports

| Service | Port | URL |
|---------|------|-----|
| Frontend | 3000 | http://localhost:3000 |
| Backend | 8000 | http://localhost:8000 |
| MCP Server | 5001 | http://localhost:5001 |

---

## Development Tips

### Hot Reload

- Frontend: Automatic via Next.js
- Backend: `--reload` flag with uvicorn
- MCP Server: Restart manually after changes

### Testing Chat

Use these sample messages to test functionality:

```
"Add buy groceries"           → Creates task
"Show my tasks"               → Lists tasks
"Mark task 1 as done"         → Completes task
"Delete task 2"               → Removes task
"Change task 1 to buy milk"   → Updates task
```

### Debugging Agent

Set environment variable for verbose logging:

```bash
export AGENTS_DEBUG=1
python server.py
```

---

## Next Steps

After setup is verified:

1. Run `/sp.tasks` to generate task breakdown
2. Implement tasks in order of priority
3. Test each user story independently
4. Create PHR after significant changes
