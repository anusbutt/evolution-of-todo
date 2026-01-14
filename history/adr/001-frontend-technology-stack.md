# ADR-001: Frontend Technology Stack

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2026-01-13
- **Feature:** 002-phase-02-web-app (Phase 2 Full-Stack Web Application)
- **Context:** Phase 2 requires a modern, responsive web interface with authentication, task management UI, and deployment infrastructure. The constitution mandates specific technologies (Next.js 16+, Tailwind CSS) while allowing flexibility in component architecture and deployment strategy.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? ✓ YES - Frontend architecture affects all user interactions, bundle size, SEO, deployment
     2) Alternatives: Multiple viable options considered with tradeoffs? ✓ YES - Remix, Vite, other frameworks considered
     3) Scope: Cross-cutting concern (not an isolated detail)? ✓ YES - Affects routing, components, styling, deployment, testing
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

Adopt an integrated frontend technology stack consisting of:

- **Framework:** Next.js 16+ (App Router architecture)
- **Language:** TypeScript 5.0+
- **Styling:** Tailwind CSS 4+
- **Routing:** Next.js App Router with file-based routing (`app/` directory)
- **Route Organization:** Route groups `(auth)` and `(dashboard)` for logical separation
- **Component Architecture:** Reusable components organized by domain (ui/, tasks/, auth/, layout/)
- **State Management:** React hooks + Server Components (no global state library initially)
- **Form Handling:** React Hook Form 7+ with Zod 3+ validation
- **Deployment:** Vercel (automatic deployments from Git main branch)
- **Testing:** Vitest 2+ (unit), React Testing Library (components), Playwright 1.48+ (E2E)

This stack is **integrated and cohesive** - components are designed to work together and would likely change together if the framework evolves.

## Consequences

### Positive

- **Constitution Compliance:** Meets Phase II requirements exactly (Next.js 16+, Tailwind CSS per §VI.Phase II:105)
- **Developer Experience:** Excellent TypeScript support, hot reload, fast refresh, integrated dev tools
- **Performance:** Server Components by default reduce client JS bundle size (target < 500KB initial load)
- **File-Based Routing:** Intuitive URL structure (`app/login/page.tsx` → `/login`), route groups for organization
- **Built-In Middleware:** Server-side auth protection before page render (fast redirects, no flash of unauthorized content)
- **SEO-Friendly:** Server-side rendering for landing pages improves search engine indexing
- **Automatic Optimizations:** Image optimization, font loading, code splitting handled by Next.js
- **Deployment Simplicity:** Vercel zero-config deployment, automatic HTTPS, global CDN
- **Type Safety:** End-to-end TypeScript from components to API client reduces runtime errors
- **Modern CSS:** Tailwind utility classes enable rapid UI development, responsive design built-in
- **Form Validation:** Zod schemas provide type-safe validation with clear error messages

### Negative

- **Vercel Vendor Lock-In:** Deployment optimized for Vercel (migration to other platforms requires configuration)
- **Framework Coupling:** Strong dependency on Next.js patterns (App Router, Server Components)
- **Learning Curve:** App Router is newer than Pages Router, fewer Stack Overflow answers for edge cases
- **Build Complexity:** Next.js build process can be opaque when debugging issues
- **Server Components Constraints:** Cannot use browser-only APIs, requires understanding client/server boundary
- **Tailwind Purge Issues:** Unused classes may be purged if dynamically constructed (requires safelist configuration)
- **Bundle Size Risk:** Without careful code splitting, initial bundle can exceed 500KB target
- **Testing Setup:** E2E tests with Playwright add test execution time (slower CI/CD)

## Alternatives Considered

### Alternative Stack A: Remix + styled-components + Cloudflare Pages

**Components:**
- Framework: Remix (React-based, nested routing)
- Styling: styled-components (CSS-in-JS)
- Deployment: Cloudflare Pages

**Why Rejected:**
- **Constitution Violation:** Constitution mandates Next.js 16+ (§VI.Phase II:105), not Remix
- Less mature ecosystem compared to Next.js (fewer third-party integrations)
- styled-components adds runtime overhead for CSS generation

### Alternative Stack B: Vite + React Router + vanilla CSS + AWS Amplify

**Components:**
- Build Tool: Vite (fast dev server, Rollup-based production builds)
- Framework: React with React Router 6
- Styling: Vanilla CSS or CSS Modules
- Deployment: AWS Amplify

**Why Rejected:**
- **Constitution Violation:** Constitution mandates Next.js 16+ and Tailwind CSS (§VI.Phase II:105)
- More manual configuration required (no built-in SSR, middleware, routing)
- AWS Amplify more complex than Vercel for simple web app deployment
- Vanilla CSS lacks utility-first rapid development of Tailwind

### Alternative Stack C: Next.js Pages Router + Material-UI + Netlify

**Components:**
- Framework: Next.js 14 (Pages Router architecture)
- Styling: Material-UI (component library)
- Deployment: Netlify

**Why Rejected:**
- **Outdated Architecture:** Constitution specifies Next.js 16+ with **App Router** (not Pages Router) (§VI.Phase II:105)
- Material-UI adds significant bundle size (>200KB), conflicts with < 500KB target
- **Constitution Violation:** Tailwind CSS mandated (§VI.Phase II:105), not Material-UI
- Netlify deployment similar to Vercel but less Next.js-optimized

## References

- Feature Spec: `../../specs/002-phase-02-web-app/spec.md` (User Stories 1-7, FR-035 to FR-041)
- Implementation Plan: `../../specs/002-phase-02-web-app/plan.md` (Design Decisions §1, §4, §10)
- Research: `../../specs/002-phase-02-web-app/research.md` (Section 3: Next.js App Router Auth Middleware Patterns)
- Constitution: `.specify/memory/constitution.md` (§VI.Phase II:105 - Frontend: Next.js 16+ App Router, Tailwind CSS)
- Related ADRs: None (first ADR)
- Evaluator Evidence: `../../history/prompts/002-phase-02-web-app/002-phase-2-planning-complete.plan.prompt.md` (Constitution Check PASS)
