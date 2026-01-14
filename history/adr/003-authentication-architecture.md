# ADR-003: Authentication Architecture

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Authentication Strategy" not separate ADRs for JWT, cookies, token expiration).

- **Status:** Accepted
- **Date:** 2026-01-13
- **Feature:** 002-phase-02-web-app (Phase 2 Full-Stack Web Application)
- **Context:** Phase 2 transitions from single-user console app (Phase 1) to multi-user web application. Authentication is required to isolate user data, secure API endpoints, and enable personalized task management. The constitution mandates Better Auth with JWT tokens, but implementation details (storage, expiration, refresh strategy) require architectural decisions with long-term security implications.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? ✓ YES - Authentication affects all protected routes, security posture, scalability, user experience
     2) Alternatives: Multiple viable options considered with tradeoffs? ✓ YES - Session-based auth, local storage JWT, OAuth considered
     3) Scope: Cross-cutting concern (not an isolated detail)? ✓ YES - Affects frontend middleware, backend middleware, API contracts, database schema (users table), testing
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

Adopt an integrated authentication architecture consisting of:

- **Authentication Library:** Better Auth (Python backend + TypeScript client)
- **Token Type:** JWT (JSON Web Tokens) with HS256 algorithm
- **Token Storage:** httpOnly cookies (SameSite=Strict, Secure flag in production)
- **Token Expiration:** 7 days (balances security and user convenience)
- **Token Refresh:** Not implemented in Phase 2 (token expires after 7 days, user must re-login)
- **Password Hashing:** Better Auth built-in (bcrypt/argon2)
- **Frontend Middleware:** Next.js middleware for route protection (server-side check before page render)
- **Backend Middleware:** FastAPI auth middleware validates JWT on all protected endpoints
- **User Isolation:** All database queries filtered by `user_id` extracted from JWT token
- **Session Management:** Stateless (no server-side session storage)
- **Logout:** Clears httpOnly cookie (JWT expires naturally, no server-side revocation)
- **Security:** No OAuth/SSO (deferred per user decision), no email verification, no password reset (Phase 2 scope)

This architecture is **stateless and horizontally scalable** - JWT tokens contain all authentication state, enabling multi-instance deployment without shared session storage.

## Consequences

### Positive

- **Constitution Compliance:** Meets Phase II requirements (Better Auth + JWT tokens per §VI.Phase II:109)
- **XSS Protection:** httpOnly cookies prevent JavaScript access (XSS attacks cannot steal token)
- **CSRF Protection:** SameSite=Strict cookies prevent cross-site request forgery
- **Stateless Architecture:** No server-side session storage enables horizontal scaling (add backend instances without coordination)
- **Fast Authentication:** JWT validation is local (no database lookup per request), < 5ms validation time
- **Frontend Redirect Speed:** Next.js middleware checks auth server-side (fast redirect, no flash of unauthorized content)
- **User Isolation:** `user_id` in JWT token ensures queries filter by current user (prevents User A from seeing User B's tasks)
- **Secure Password Storage:** Better Auth handles hashing (passwords never stored in plain text)
- **Simple Logout:** Clear cookie on frontend (no server-side revocation list needed for Phase 2 scope)
- **Testing Simplicity:** TestClient can set cookies, easy to mock authenticated requests in tests

### Negative

- **Token Revocation Limitation:** Cannot force logout before 7-day expiration (compromised tokens remain valid until expiry)
- **No Token Refresh:** User must re-login after 7 days (poor UX for frequent users)
- **JWT Size Overhead:** JWT tokens ~200-500 bytes (sent in every request), increases bandwidth slightly vs session ID
- **Clock Synchronization:** Servers must have synchronized clocks for expiration validation (NTP required)
- **Secret Key Management:** JWT secret must be securely stored, rotated periodically (compromise = all tokens invalid)
- **User Session Control:** Admin cannot force-logout specific users (no central session management)
- **Payload Size Limit:** Cookie max 4KB (JWT payload must stay small), limits what can be embedded in token
- **No OAuth Integration:** Users cannot login with Google/GitHub (deferred to Phase 3+)
- **Password Reset Absent:** Users cannot reset forgotten passwords (must contact admin - Phase 2 limitation)
- **Email Verification Missing:** Fake emails can register (acceptable risk for Phase 2 hackathon scope)

## Alternatives Considered

### Alternative A: Session-Based Authentication (Server-Side Sessions)

**Components:**
- Session ID stored in httpOnly cookie
- Session data stored in Redis or database
- Backend looks up session on every request

**Why Rejected:**
- **Not Stateless:** Requires centralized session storage (Redis, database), complicates horizontal scaling
- **Database Lookup Overhead:** Every request requires session lookup (adds 10-50ms latency)
- **Scalability Complexity:** Multi-instance deployment requires shared Redis or sticky sessions
- **Constitution Preference:** Constitution specifies JWT tokens (§VI.Phase II:109), not sessions

### Alternative B: JWT Tokens in Local Storage

**Components:**
- JWT stored in browser localStorage
- JavaScript reads token, adds to Authorization header on API requests

**Why Rejected:**
- **XSS Vulnerability:** JavaScript can access localStorage (XSS attacks steal token)
- **Constitution Risk:** Constitution prioritizes security (§Security Principles:208-233), this approach violates XSS prevention
- **Industry Best Practice:** httpOnly cookies recommended by OWASP for token storage

### Alternative C: OAuth 2.0 with Third-Party Providers (Google, GitHub)

**Components:**
- OAuth 2.0 authorization flow
- Users login with Google/GitHub account
- Backend receives OAuth token, exchanges for user info

**Why Rejected:**
- **User Decision:** User explicitly deferred OAuth to Phase 3+ (Phase 2 spec §Assumptions:351)
- **Implementation Complexity:** OAuth adds callback endpoints, token exchange, account linking
- **Scope Creep:** Not required for Phase 2 MVP (email/password sufficient for hackathon)
- **Still Need Password Auth:** Must support email/password as fallback (doubles auth code)

### Alternative D: Magic Link Authentication (Email-Based)

**Components:**
- User enters email, receives login link
- Clicking link authenticates user (no password)

**Why Rejected:**
- **Email Service Required:** Needs email provider (SendGrid, Mailgun), adds cost and complexity
- **User Decision:** No email verification requested (§Assumptions:352), magic links require email
- **Poor UX for Offline:** Cannot login without internet (Phase 2 requires internet anyway, but degrades UX)
- **Constitution Not Mentioned:** Better Auth with passwords mandated (§VI.Phase II:109)

## References

- Feature Spec: `../../specs/002-phase-02-web-app/spec.md` (User Story 1, FR-001 to FR-009, SC-001 to SC-004)
- Implementation Plan: `../../specs/002-phase-02-web-app/plan.md` (Design Decision §2, Authentication Flow Diagram)
- Research: `../../specs/002-phase-02-web-app/research.md` (Section 1: Better Auth Integration, Section 3: Next.js Middleware Auth)
- Constitution: `.specify/memory/constitution.md` (§VI.Phase II:109 - Better Auth JWT tokens, §Security Principles:208-212)
- Related ADRs: ADR-001 (Frontend Stack provides Next.js middleware), ADR-002 (Backend Stack provides FastAPI middleware)
- Evaluator Evidence: `../../history/prompts/002-phase-02-web-app/002-phase-2-planning-complete.plan.prompt.md` (Security Principles PASS)
