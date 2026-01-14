# ADR-005: Testing Architecture

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Testing Strategy" not separate ADRs for unit, integration, E2E).

- **Status:** Accepted
- **Date:** 2026-01-13
- **Feature:** 002-phase-02-web-app (Phase 2 Full-Stack Web Application)
- **Context:** Phase 2 requires comprehensive testing to ensure quality, prevent regressions, and meet constitution requirement of 75% minimum coverage. Testing must span frontend (components, forms, routing), backend (API endpoints, database operations, authentication), and full user workflows (E2E). The constitution mandates specific technologies and coverage targets, but testing strategy (unit vs integration vs E2E balance) requires architectural decisions.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? ✓ YES - Testing architecture affects code quality, deployment confidence, refactoring safety, bug detection
     2) Alternatives: Multiple viable options considered with tradeoffs? ✓ YES - Unit-only, E2E-only, TDD-strict, manual testing considered
     3) Scope: Cross-cutting concern (not an isolated detail)? ✓ YES - Affects all components, API endpoints, database models, CI/CD pipeline, development workflow
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

Adopt a **layered testing architecture** with complementary strategies across the test pyramid:

**Backend Testing (Python):**
- **Framework:** pytest 8+ (test discovery, fixtures, async support)
- **Async Testing:** pytest-asyncio 0.24+ (async test execution)
- **API Testing:** FastAPI TestClient (synchronous) + httpx 0.28+ (async test client)
- **Database Testing:** Test database isolation (separate DB per test suite), transaction rollback between tests
- **Coverage Target:** 75% minimum (constitution requirement), measured with pytest-cov
- **Test Types:**
  - **Unit Tests:** Pure functions, validation schemas, utility functions (fast, isolated)
  - **Integration Tests:** API endpoints with database, authentication middleware, service layer logic
  - **Contract Tests:** Request/response validation against OpenAPI schemas

**Frontend Testing (TypeScript):**
- **Unit/Component Framework:** Vitest 2+ (fast, Vite-native)
- **Component Testing:** React Testing Library (user-centric queries, accessibility)
- **E2E Framework:** Playwright 1.48+ (cross-browser, mobile viewports)
- **Coverage Target:** 75% minimum (measured with Vitest coverage)
- **Test Types:**
  - **Unit Tests:** Utility functions, validation schemas (Zod), pure logic
  - **Component Tests:** Isolated component rendering, user interactions, form validation
  - **E2E Tests:** Complete user workflows (signup → login → add task → edit task → logout)

**Testing Philosophy:**
- **Test Pyramid:** Many unit tests (fast feedback), fewer integration tests (confidence), few E2E tests (critical workflows)
- **User-Centric:** Test behavior, not implementation (avoid brittle tests tied to internal structure)
- **Fast Feedback:** Unit tests < 100ms, integration tests < 500ms, E2E tests < 5s per workflow
- **CI/CD Integration:** All tests run on every push (GitHub Actions), no merge without passing tests
- **Test Isolation:** Each test independent (no shared state), database transactions rolled back, mock external APIs

**Coverage Requirements:**
- 75% minimum across backend and frontend (constitution requirement)
- Critical paths 100% covered (authentication, task CRUD, user isolation)
- Exclude from coverage: Config files, type definitions, migration scripts

## Consequences

### Positive

- **Constitution Compliance:** Meets 75% minimum coverage requirement (§Testing Quality:195)
- **Fast Feedback:** Unit tests provide instant feedback (< 100ms), catch bugs early in development
- **High Confidence:** Integration tests verify API contracts, database operations, authentication work together
- **Real User Validation:** E2E tests validate complete workflows (signup → login → add task → logout)
- **Refactoring Safety:** Comprehensive test suite enables confident refactoring without breaking functionality
- **Regression Prevention:** Tests catch bugs introduced by new changes (continuous integration)
- **Documentation:** Tests serve as living documentation of expected behavior
- **Accessibility:** React Testing Library encourages accessible component design (role-based queries)
- **Cross-Browser Coverage:** Playwright tests in Chrome, Firefox, Safari (catches browser-specific bugs)
- **Developer Experience:** Vitest fast, hot-reload-like test execution; pytest clear output with fixtures
- **CI/CD Ready:** Tests run automatically on push, block merge if failing (quality gate)
- **Database Isolation:** Test database prevents production data corruption, transaction rollback ensures clean state

### Negative

- **Test Maintenance Burden:** 75% coverage requires writing ~500-1000 lines of test code (roughly 1:1 ratio with production code)
- **Slower Development Initially:** Writing tests upfront adds time to feature development (pay-off comes later)
- **E2E Test Flakiness:** Playwright tests can be flaky (timing issues, network delays), require retry logic
- **CI/CD Time:** Running full test suite on every push adds 2-5 minutes to CI/CD pipeline
- **Test Database Setup:** Requires separate test database, schema migrations, seed data management
- **False Sense of Security:** 75% coverage doesn't guarantee bug-free code (coverage measures lines run, not correctness)
- **Brittle E2E Tests:** E2E tests break when UI changes (e.g., button class names, element IDs)
- **Async Complexity:** Testing async code (SQLModel queries, FastAPI endpoints) requires understanding pytest-asyncio, proper awaiting
- **Mocking Complexity:** Integration tests require mocking external services (email, payment), can hide integration bugs
- **Test Data Management:** Requires maintaining test fixtures, factories, seed data (additional code to maintain)
- **Coverage Pressure:** Developers may write low-value tests to hit coverage target (testing getters/setters)

## Alternatives Considered

### Alternative A: Unit Tests Only (No Integration or E2E)

**Components:**
- pytest for backend unit tests (pure functions, validation schemas)
- Vitest for frontend unit tests (utilities, components with mocks)
- No integration tests (API endpoints, database, auth tested in isolation with mocks)
- No E2E tests (user workflows not validated)

**Why Rejected:**
- **Low Confidence:** Unit tests with mocks don't catch integration bugs (e.g., wrong SQL query, auth middleware misconfiguration)
- **Missed Real-World Issues:** Cannot detect bugs in API contracts, database constraints, authentication flow
- **Poor Coverage of Critical Paths:** User workflows (signup → login → add task) never validated end-to-end
- **Mock Overload:** Heavy mocking makes tests brittle (tests pass but production fails)
- **No Cross-Layer Validation:** Frontend and backend integration not tested (API contract mismatches)

### Alternative B: E2E Tests Only (No Unit or Integration)

**Components:**
- Playwright E2E tests for all user workflows
- Test entire application through browser (login, add task, edit task, delete task)
- No unit tests, no integration tests

**Why Rejected:**
- **Slow Feedback:** E2E tests take 5-30 seconds per workflow (too slow for TDD-style development)
- **Flaky Tests:** E2E tests prone to timing issues, network delays, browser quirks (false negatives)
- **Hard to Debug:** E2E test failures don't pinpoint root cause (could be frontend, backend, database, auth)
- **Low Coverage:** E2E tests expensive to write, cannot achieve 75% coverage target with reasonable test count
- **No Isolation:** E2E tests require full stack running (database, backend, frontend), slower CI/CD
- **Poor Developer Experience:** Waiting 5+ seconds per test iteration kills productivity

### Alternative C: TDD-Strict (Write Tests Before Any Code)

**Components:**
- Strict Test-Driven Development: write failing test → write minimal code to pass → refactor
- 100% coverage target (every line tested before written)
- Red-Green-Refactor cycle enforced

**Why Rejected:**
- **Slower Initial Development:** Writing tests first for every function adds significant upfront time
- **Over-Engineering Risk:** TDD can lead to over-testing trivial code (getters, setters, simple utilities)
- **Learning Curve:** Team may not be experienced with TDD, slows development during Phase 2 hackathon timeline
- **Constitution Not Required:** Constitution mandates 75% coverage, not 100% or TDD workflow
- **Flexibility Loss:** TDD rigid, doesn't allow exploratory coding or prototyping (useful for hackathons)
- **Diminishing Returns:** 100% coverage has low ROI (last 25% often trivial code not worth testing)

### Alternative D: Manual Testing Only (No Automated Tests)

**Components:**
- Manual testing of all features by developers
- QA checklist for critical workflows
- No automated test suite

**Why Rejected:**
- **Constitution Violation:** Constitution mandates 75% coverage (§Testing Quality:195), impossible without automated tests
- **No Regression Prevention:** Manual tests don't catch regressions introduced by new changes
- **Slow Feedback:** Manual testing takes hours/days, not minutes (blocks development)
- **Human Error:** Manual testing prone to mistakes (forgot to test edge case, didn't test on mobile)
- **No CI/CD:** Cannot integrate into automated deployment pipeline (quality gate impossible)
- **Poor Documentation:** Manual checklists don't document expected behavior as clearly as code tests

## References

- Feature Spec: `../../specs/002-phase-02-web-app/spec.md` (User Stories 1-7, Success Criteria SC-005 to SC-008)
- Implementation Plan: `../../specs/002-phase-02-web-app/plan.md` (Design Decision §9, Technical Context §Testing)
- Research: `../../specs/002-phase-02-web-app/research.md` (Section 8: Testing Strategy)
- Constitution: `.specify/memory/constitution.md` (§Testing Quality:195 - 75% minimum coverage, §Testing Quality:183-207)
- Related ADRs: ADR-001 (Frontend Stack includes Vitest, React Testing Library, Playwright), ADR-002 (Backend Stack includes pytest, pytest-asyncio, httpx)
- Evaluator Evidence: `../../history/prompts/002-phase-02-web-app/002-phase-2-planning-complete.plan.prompt.md` (Testing requirements PASS)
