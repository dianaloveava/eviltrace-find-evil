# Test Spec: EvilTrace for FIND EVIL!

## Metadata
- PRD: docs/prd-eviltrace-find-evil.md
- Source spec: prior deep-interview planning session; runtime `.omx/` state is intentionally gitignored
- Created: 2026-04-26T09:36:41.861Z

## Verification strategy
EvilTrace must be judged as a working, reproducible, free-path full-stack demo. Verification focuses on deterministic behavior, evidence integrity, bounded agent execution, UI visibility, and submission readiness.

## Test layers

### Unit tests
Backend:
- Evidence hashing is stable and recorded for each fixture.
- Artifact parsers return structured events with source references.
- Tool adapters are read-only and reject unsupported/destructive operations.
- Agent step budget and timeout limits stop runaway loops.
- Finding confidence classification is deterministic for fixture cases.
- Self-correction marks weak or contradictory findings and creates follow-up checks.
- Report exporter produces valid Markdown and JSON.

Frontend:
- Timeline component renders ordered agent steps.
- Finding cards render severity, confidence, and evidence links.
- Evidence inventory renders hash/type/source metadata.
- Correction badge/state displays before/after confidence.

### Integration tests
- Start a run from bundled fixture through API; persist run, steps, tools, findings, corrections, and report.
- Confirm every final finding has at least one evidence reference.
- Confirm at least one demo correction event exists.
- Confirm rerunning the same fixture produces stable key results.
- Confirm no external paid API key is required for default run.

### E2E/smoke tests
- Launch backend and frontend.
- Open dashboard.
- Start bundled demo run or load pregenerated run.
- Inspect timeline, evidence, findings, corrections, and report export.
- Export report and verify file content includes findings and caveats.

### Security/safety checks
- No default outbound network access for evidence processing.
- No destructive filesystem operations against evidence fixtures.
- Uploaded/fixture paths are normalized and restricted to workspace data directory.
- UI does not render raw untrusted HTML from evidence.
- README warns users not to upload real sensitive/private evidence to public demos.

### Submission checks
- README includes setup, run, architecture, judging mapping, boundaries, and final submission checklist.
- Devpost story draft exists.
- Demo script and screenshot checklist exist.
- License and attribution for any sample data/rules are included.
- Public demo can run with safe fixtures only.

## Acceptance checklist
- [ ] Backend tests pass.
- [ ] Frontend tests pass.
- [ ] E2E/smoke run completed or documented if skipped.
- [ ] One complete demo run artifact committed/exported.
- [ ] At least one self-correction sequence visible in UI.
- [ ] Final report generated as Markdown and JSON.
- [ ] No required paid API key.
- [ ] No student-only contest dependency.
- [ ] User-only Devpost/legal/final-submit steps documented.

## Known verification risks
- SIFT/Protocol SIFT full environment may not be runnable in this workspace. Mitigation: fixture-first MVP plus optional integration instructions.
- If local LLM is used, output can vary. Mitigation: default deterministic rules; optional LLM only enriches narrative, not core evidence decisions.
- Public deployment may not have safe access to local evidence. Mitigation: bundle a safe demo run and keep upload disabled or fixture-only in public mode.
