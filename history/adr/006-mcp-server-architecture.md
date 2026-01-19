# ADR-006: MCP Server Architecture

> **Scope**: MCP (Model Context Protocol) server deployment architecture for AI chatbot integration.

- **Status:** Accepted
- **Date:** 2026-01-16
- **Feature:** 003-phase-03-ai-chatbot
- **Context:** Phase 3 introduces an AI chatbot that manages tasks via natural language. The AI agent needs to execute task operations (add, list, complete, delete, update) through MCP tools. A key architectural decision is whether to embed MCP functionality within the existing backend or deploy it as a separate service.

## Decision

**Deploy MCP Server as a separate independent service** with the following configuration:

- **Service**: Standalone Python service on port 5001
- **Transport**: HTTP with SSE (Server-Sent Events)
- **Database**: Shared PostgreSQL (same as backend)
- **Communication**: Backend → MCP Server via HTTP/SSE protocol
- **Tools**: 5 atomic tools (add_task, list_tasks, complete_task, delete_task, update_task)

**Architecture**:
```
Frontend (3000) → Backend (8000) → MCP Server (5001) → PostgreSQL
                       ↓
                  Gemini API
```

## Consequences

### Positive

1. **Constitution Compliance**: Meets Phase III mandate for "MCP Server: Separate service (port 5001)"
2. **Independent Scaling**: MCP server can scale independently based on AI workload
3. **Isolation**: Tool execution isolated from main API; failures don't cascade
4. **Phase 4 Ready**: Clean separation enables containerization (Docker Compose)
5. **Technology Flexibility**: MCP server can evolve independently (different Python version, dependencies)
6. **Debugging**: Clear boundary makes it easier to trace tool execution issues
7. **Reusability**: MCP server can serve multiple clients in future phases

### Negative

1. **Operational Complexity**: 3 services to manage instead of 2
2. **Network Latency**: Additional HTTP hop for tool calls (~10-50ms overhead)
3. **Deployment Coordination**: Must deploy MCP server alongside backend
4. **Shared Database Coupling**: Both services depend on same PostgreSQL schema
5. **Configuration Overhead**: Additional environment variables and port management

## Alternatives Considered

### Alternative A: Embedded MCP in Backend

Embed MCP tool handlers directly in the FastAPI backend as internal functions.

```
Frontend (3000) → Backend (8000) → PostgreSQL
                      ↓
                 Gemini API
```

**Pros**:
- Simpler deployment (2 services)
- No network overhead for tool calls
- Single codebase to maintain

**Cons**:
- Violates constitution mandate
- Tight coupling between API and AI logic
- Harder to scale AI workload independently
- Not containerization-ready for Phase 4

**Why Rejected**: Constitution explicitly requires separate MCP server. This alternative would require justification and approval to override.

### Alternative B: MCP with stdio Transport

Run MCP server as subprocess spawned by backend, communicating via stdio.

**Pros**:
- No HTTP overhead
- Simpler protocol

**Cons**:
- Not a separate service (subprocess)
- Subprocess management complexity
- Can't scale independently
- Harder to monitor and debug

**Why Rejected**: stdio transport is designed for local tool execution, not service architecture. Doesn't meet "separate service" requirement.

### Alternative C: Separate Database per Service

Give MCP server its own database, sync via events.

**Pros**:
- True service isolation
- Independent schema evolution

**Cons**:
- Data synchronization complexity
- Eventual consistency issues
- Overkill for current scale

**Why Rejected**: Constitution allows "shared DB with clear boundaries". Separate databases add complexity without proportional benefit at this scale.

## References

- Feature Spec: [specs/003-phase-03-ai-chatbot/spec.md](../../specs/003-phase-03-ai-chatbot/spec.md)
- Implementation Plan: [specs/003-phase-03-ai-chatbot/plan.md](../../specs/003-phase-03-ai-chatbot/plan.md)
- Research: [specs/003-phase-03-ai-chatbot/research.md](../../specs/003-phase-03-ai-chatbot/research.md)
- Related ADRs: ADR-002 (Backend Technology Stack)
- Constitution: Phase III Technology Stack requirements
