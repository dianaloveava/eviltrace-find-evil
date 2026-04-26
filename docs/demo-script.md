# EvilTrace Demo Script

Target length: 4-5 minutes.

## Shot 1: Problem framing (20s)
Explain that autonomous IR agents are only useful if analysts and judges can inspect the evidence behind each claim.

## Shot 2: Start the app (30s)
Run:

```bash
python -m eviltrace.server
```

Open the dashboard and point out that the demo uses synthetic fixtures and no paid APIs.

## Shot 3: Run investigation (60s)
Click **Run demo investigation**. Show metrics: findings, corrections, evidence refs, no paid API.

## Shot 4: Timeline (60s)
Walk through plan, baseline, auth checks, suspicious commands, persistence, exfiltration checks, and final report step.

## Shot 5: Findings (60s)
Show initial access and execution/persistence findings. Emphasize that every claim links to evidence references.

## Shot 6: Self-correction (45s)
Show the exfiltration finding downgrade from high to medium confidence because the fixture lacks destination ownership proof.

## Shot 7: Export report (30s)
Open `/api/runs/latest/report.md` and show the Markdown report.

## Closing (20s)
Summarize: EvilTrace is a transparent, bounded, free-to-run defender agent workbench designed for trustworthy autonomous incident response.
