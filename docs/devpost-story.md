# Devpost Story Draft: EvilTrace

## Inspiration

Security teams increasingly want autonomous investigation helpers, but black-box agents are hard to trust. A useful defender agent should not just produce a confident answer; it should show the evidence trail, expose uncertainty, and correct itself when a claim is weak.

## What it does

EvilTrace runs a safe, synthetic incident-response case through a bounded autonomous workflow. It inventories evidence, runs read-only checks, correlates suspicious login, execution, persistence, and exfiltration signals, then exports a transparent report. The dashboard lets judges inspect every agent step, every evidence reference, and the self-correction that downgrades an overconfident exfiltration claim.

## How we built it

- Python 3.12 backend using only the standard library.
- Deterministic read-only analysis tools over JSONL fixture evidence.
- Bounded investigation loop with structured logs and finding confidence.
- Static HTML/CSS/JS dashboard with API-driven run views.
- Markdown/JSON report export for judge review.

## Challenges

The biggest challenge was balancing autonomy with trust. EvilTrace intentionally refuses to treat suspicious upload signals as confirmed theft without destination corroboration. That self-correction makes the demo more credible than a system that simply maximizes confidence.

## Accomplishments

- Full-stack app with no required paid services.
- Complete autonomous investigation run.
- Evidence-linked findings and correction trail.
- Reproducible synthetic fixture and test suite.
- Submission-ready architecture and demo materials.

## What we learned

Autonomous security agents need auditability as a first-class feature. The best demo is not a perfect oracle; it is an agent that shows how it knows, when it is unsure, and how it revises weak claims.

## What's next

- Add optional SIFT / Protocol SIFT adapters.
- Add more benchmark fixtures.
- Add local LLM summarization that never overrides deterministic evidence decisions.
- Add richer evidence graph visualization.

## Built with

Python, HTML, CSS, JavaScript, SQLite-ready JSON data model, synthetic incident-response fixtures.
