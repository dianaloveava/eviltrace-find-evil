# Dataset Documentation

## Data sources included in this repository

### 1. Default synthetic fixture

Path: `data/fixtures/case_alpha/events.jsonl`

This is a synthetic, safe incident-response fixture created for the EvilTrace demo. It is not private, not regulated, and not copied from a real victim environment.

### 2. SIFT/DFIR export demo bundle

Source path: `data/sift_exports/demo/`

Normalized case path: `data/fixtures/sift_demo/events.jsonl`

This bundle simulates common SIFT/DFIR outputs without shipping large disk or memory images:

- `plaso_timeline.csv`: Plaso/log2timeline-style auth, process, persistence, and network events.
- `volatility_pslist.json`: Volatility-style process listing output.
- `sleuthkit.body`: Sleuth Kit bodyfile-style filesystem metadata.

Normalize it with:

```bash
python -m eviltrace.cli import-sift --source data/sift_exports/demo --case sift_demo
```

Then run:

```bash
python -m eviltrace.cli run --case sift_demo --report docs/sift-demo-report.md
```

## Scenario

The demo cases simulate:

1. Suspicious authentication from known suspicious infrastructure.
2. Same-account logins from multiple countries in the investigation window.
3. Discovery and encoded PowerShell/payload execution.
4. Persistence via cron/service artifacts.
5. Archive creation and outbound transfer signals.

## What EvilTrace found

- Confirmed likely account compromise from suspicious login + impossible-travel evidence.
- Confirmed execution/persistence based on process and persistence artifacts.
- Downgraded exfiltration confidence because upload/archive/DNS signals alone do not prove attacker-controlled receipt.

## Official FIND EVIL! starter data

The FIND EVIL! resources page links official starter case data at:

https://sansorg.egnyte.com/fl/HhH7crTYT4JK

For this workspace, the selected starter case zip has been downloaded locally and integrity-recorded without committing the raw evidence file:

- Local file: `official-data/xp-tdungan-10.3.58.7.zip` (gitignored)
- Size: `12061961109` bytes
- SHA-256: `aec574308482daffaa9c85a585287183bd8605a7d797580bd439cf47ecccaa6f`
- Public manifest committed at: `docs/official-starter-data-manifest.json`

The raw official evidence zip is 11.23GB, so it is intentionally excluded from GitHub. For the strongest final submission, run the full official case inside SIFT Workstation, export Plaso/Volatility/SleuthKit artifacts, import those exports with `python -m eviltrace.cli import-sift`, and attach the resulting report/logs.

## Evidence integrity

Original source exports are read-only. EvilTrace writes a derived `events.jsonl` under `data/fixtures/<case_id>/` and hashes that normalized evidence for reproducibility.
