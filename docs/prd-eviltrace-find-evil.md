# PRD: EvilTrace for FIND EVIL!

## Metadata
- Planning mode: ralplan-style non-interactive consensus summary
- Source spec: prior deep-interview planning session; runtime `.omx/` state is intentionally gitignored
- Created: 2026-04-26T09:36:41.861Z
- Target hackathon: FIND EVIL! (https://findevil.devpost.com/)
- Backup candidates: Build with MeDo (https://medo.devpost.com/), Splunk Agentic Ops (https://splunk.devpost.com/)

## RALPLAN-DR Summary

### Principles
1. Prize-oriented but honest: optimize judging criteria; never promise winning.
2. Free-first: no paid contest entry and no required paid API path.
3. Evidence integrity: agent actions must be auditable, read-only against evidence, and reproducible.
4. Demo polish matters: judges must quickly see autonomy, accuracy, constraints, and usability.
5. Build for fallback: if full SIFT integration is blocked, the demo still works with safe sample fixtures and clear adapter boundaries.

### Decision drivers
1. User boundary fit: free entry, avoid student-only, user handles legal/account/final submission.
2. Prize probability: meaningful cash prize plus differentiated technical depth.
3. Feasibility: buildable full-stack MVP before the Jun 15, 2026 deadline.

### Viable options considered
- Option A: FIND EVIL! / EvilTrace (chosen)
  - Pros: public online challenge, substantial $22k prize pool, clear forensic-agent judging fit, enough time, non-student preference appears satisfied.
  - Cons: technically harder; SIFT/Protocol SIFT environment may add setup risk.
- Option B: Build with MeDo
  - Pros: easiest, $50k prize pool, many prize slots, beginner/low-code.
  - Cons: high visible participant count, external platform dependency, weaker fit for agent-coded full-stack repository.
- Option C: Splunk Agentic Ops
  - Pros: $20k prize, lower visible competition, excellent agentic-ops fit.
  - Cons: detailed requirements not available until May 13, 2026, so immediate planning has more uncertainty.

### Decision
Choose FIND EVIL! and build EvilTrace: a self-correcting incident-response agent workbench with a full-stack audit dashboard.

## Product overview
EvilTrace is a local-first, full-stack cybersecurity agent workbench for repeatable incident-response triage. It ingests safe sample case artifacts/logs, runs a bounded autonomous investigation workflow, records every tool call and evidence reference, detects contradictions, performs targeted re-checks, and emits a judge-friendly final report plus visual timeline.

## Target users
- Hackathon judges evaluating autonomous defender agents.
- Incident responders who need transparent agent-assisted triage.
- Security learners who need evidence-linked explanations rather than black-box findings.

## Goals
1. Demonstrate an autonomous incident-response agent that can plan, execute, verify, self-correct, and report.
2. Make every claim evidence-linked and auditable.
3. Provide a polished dashboard and submission story that maps directly to FIND EVIL! judging criteria.
4. Keep the default demo free, local, and safe.

## Non-goals
- No paid API requirement.
- No destructive tooling.
- No handling real private evidence in the demo.
- No Devpost/legal/account actions by the agent.
- No guarantee of prize award.

## Proposed tech stack
- Backend: Python 3.12, FastAPI, SQLite, Pydantic, pytest.
- Agent core: deterministic finite-state investigation loop plus optional local-LLM adapter (Ollama-compatible) that is disabled by default.
- Tool adapters: read-only log/file parsers, timeline extractor, IOC matcher, Sigma/YARA-style rule hooks where feasible.
- Frontend: React + TypeScript + Vite, Tailwind or lightweight CSS, Vitest.
- E2E smoke: Playwright only if time permits.
- Packaging: Docker Compose optional; local run must work without paid services.

## Core features

### F1. Evidence workspace
- Upload or load bundled safe sample case fixtures.
- Store artifacts as immutable evidence records with hash, type, source path, and parse status.
- Show evidence inventory in UI.

### F2. Autonomous triage run
- Start a bounded investigation run from the UI/API.
- Agent creates hypotheses, selects read-only tools, runs checks, and records results.
- Hard limits: max steps, max tool runtime, no network by default, no destructive commands.

### F3. Self-correction loop
- Agent checks whether findings have sufficient evidence.
- Contradictory or weak findings trigger targeted re-check steps.
- UI highlights corrections and before/after confidence changes.

### F4. Findings and report
- Produce structured findings: title, severity, confidence, evidence links, reasoning, caveats.
- Export Markdown/JSON report suitable for Devpost and judge review.

### F5. Judge dashboard
- Run timeline: plan -> tool calls -> evidence -> corrections -> final report.
- Evidence graph: findings connected to artifact lines/events.
- Metrics panel: steps, corrections, confirmed/unknown/false-positive counts.

### F6. Submission package
- README, architecture diagram, demo script, Devpost story draft, screenshots, and judging-criteria mapping.

## MVP scope
- One bundled safe case fixture set.
- 5-8 read-only tools/parsers.
- One complete autonomous run from fixture to final report.
- Web dashboard for run timeline, findings, evidence, and corrections.
- Exported report and Devpost-ready documentation.

## Stretch scope
- Optional SIFT/Protocol SIFT adapter instructions.
- Local LLM summarizer adapter.
- More fixtures and benchmark scoring.
- Dockerized one-command demo.
- Video walkthrough automation/script.

## Implementation phases
1. Repository scaffold and domain model.
2. Evidence fixture ingestion and read-only tool adapter layer.
3. Agent loop and self-correction mechanics.
4. API endpoints and persistence.
5. React dashboard.
6. Reports, docs, demo assets, and Devpost story.
7. Hardening, tests, and final submission checklist.

## Acceptance criteria
- Clean checkout can run backend and frontend with documented free commands.
- Bundled fixture produces a complete run without external paid services.
- UI shows evidence records, timeline, findings, and corrections.
- Every final finding has at least one evidence reference.
- At least one weak/contradictory finding is corrected in the demo run.
- Exported Markdown/JSON report exists.
- README contains user/legal boundaries and contest submission checklist.
- PRD and test spec exist under .omx/plans/.

## ADR
Decision: Target FIND EVIL! with EvilTrace, a full-stack auditable IR agent workbench.

Drivers:
- User prefers free entry, non-student where possible, prize orientation, and accepts harder implementation.
- FIND EVIL! has clear requirements and a substantial cash prize pool.
- The project can showcase agentic capability better than a generic no-code app.

Alternatives considered:
- Build with MeDo: rejected as primary due external no-code dependence and high competition despite being easier.
- Splunk Agentic Ops: deferred because requirements are not fully published until May 13, 2026.
- EnviroCast/social-good small-prize tracks: rejected because lower prize and weaker fit with user preference after pressure pass.

Consequences:
- Higher technical risk; mitigated by fixture-first MVP and optional SIFT adapter.
- Stronger differentiation if implemented well.
- Submission must carefully explain evidence integrity and no-paid-service path.

Follow-ups:
- Recheck FIND EVIL! rules before final submission.
- If SIFT environment blocks, document adapter and submit working fixture demo.
- User must personally join/submit on Devpost.
