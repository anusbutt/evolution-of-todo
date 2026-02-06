---
id: 003
title: Migrate Cloud Provider OCI to DigitalOcean
stage: misc
date: 2026-02-05
surface: agent
model: claude-opus-4-5-20251101
feature: 005-phase-05-cloud-native
branch: 005-phase-05-cloud-native
user: architect
command: direct-prompt
labels: ["cloud-migration", "digitalocean", "oci", "infrastructure", "constitution-amendment"]
links:
  spec: specs/005-phase-05-cloud-native/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - specs/005-phase-05-cloud-native/spec.md
  - specs/005-phase-05-cloud-native/plan.md
  - specs/005-phase-05-cloud-native/tasks.md
tests:
  - none (documentation-only change)
---

## Prompt

User reported OCI node pool stuck in CREATING state for ~1 hour. Investigation revealed "Out of host capacity" error for VM.Standard.A1.Flex (ARM64) in ap-mumbai-1. Multiple NODEPOOL_CREATE and NODEPOOL_RECONCILE work requests all FAILED. Attempted to subscribe tenancy to Frankfurt region but hit "TenantCapacityExceeded" - free tier limited to 1 region. User requested switching to DigitalOcean instead of OKE. User confirmed: will create new DO account ($200 credit), acceptable cost for hackathon (~3 months needed). User explicitly requested: "now first update all sdd artifacts. because we are using pure-sdd not vibe coding."

## Response snapshot

Updated all 4 SDD artifacts following constitution hierarchy (Constitution > Spec > Plan > Tasks):

1. **Constitution v1.5.0 → v1.6.0**: Amended Phase V Technology Stack from OCI/OKE to DigitalOcean/DOKS. Updated Deployment Standards Phase V with DOCR, Frankfurt region, amd64 architecture.

2. **spec.md**: Replaced all OCI/OKE/OCIR references. Updated architecture diagram, component table, technical requirements (DOKS cluster spec, DOCR registry), CI/CD secrets, constraints (budget-based vs free-tier), risks, acceptance scenarios, glossary, references.

3. **plan.md**: Updated summary, technical context, constitution check, architecture diagram, CI/CD pipeline design (doctl-based), complexity tracking, risk mitigations.

4. **tasks.md**: Replaced Phase 3 (US1) tasks entirely (T021-T037 → T021a-T037a) for DigitalOcean workflow. Updated Phase 4/5 OKE references to DOKS. Updated Phase 11 CI/CD tasks for doctl/DOCR. Updated notes, summary table, parallel examples.

Key architectural changes:
- ARM64 (Ampere A1) → amd64 (standard x86_64 droplets)
- OCIR auth tokens → doctl registry login
- VCN/subnets → auto-managed VPC
- oci CLI → doctl CLI
- Free tier (no cost) → $200 credit (~$36/month, ~5 months coverage)

## Outcome

- ✅ Impact: All SDD artifacts aligned for DigitalOcean/DOKS deployment
- 🧪 Tests: None (documentation-only, no code changes)
- 📁 Files: 4 files modified (constitution, spec, plan, tasks)
- 🔁 Next prompts: Create DO account, authenticate doctl, create DOKS cluster (T021a-T024a)
- 🧠 Reflection: Pure SDD approach - updating all artifacts before any implementation ensures consistency and traceability. OCI capacity issues are a known problem with free-tier ARM64 instances.

## Evaluation notes (flywheel)

- Failure modes observed: OCI ARM64 capacity exhaustion is a systemic issue, not transient. Free tier region lock prevents fallback.
- Graders run and results (PASS/FAIL): PASS - all artifacts updated consistently, no placeholder text remaining
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed with DigitalOcean account creation and DOKS cluster provisioning
