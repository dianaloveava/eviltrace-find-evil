from __future__ import annotations

import argparse
import json
from pathlib import Path

from .agent import InvestigationAgent, render_markdown_report
from .importers import normalize_sift_exports
from .server import run as run_server


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="eviltrace", description="EvilTrace incident-response agent workbench")
    sub = parser.add_subparsers(dest="command", required=True)

    p_import = sub.add_parser("import-sift", help="Normalize SIFT/DFIR exports into an EvilTrace case")
    p_import.add_argument("--source", required=True, help="Directory containing Plaso/Volatility/SleuthKit exports")
    p_import.add_argument("--case", default="sift_demo", help="Destination case id under data/fixtures")

    p_run = sub.add_parser("run", help="Run the bounded investigation agent")
    p_run.add_argument("--case", default="case_alpha", help="Case id under data/fixtures")
    p_run.add_argument("--report", default="docs/sample-report.md", help="Markdown report output path")

    p_serve = sub.add_parser("serve", help="Start the local web server")
    p_serve.add_argument("--host", default="127.0.0.1")
    p_serve.add_argument("--port", default=8765, type=int)

    args = parser.parse_args(argv)
    if args.command == "import-sift":
        dest = normalize_sift_exports(args.source, args.case)
        print(f"Imported SIFT/DFIR exports into {dest}")
        return 0
    if args.command == "run":
        agent_run = InvestigationAgent(args.case).run()
        report = render_markdown_report(agent_run)
        out = Path(args.report)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(report, encoding="utf-8")
        print(json.dumps({"run_id": agent_run.id, "case_id": agent_run.case_id, "report": out.as_posix()}, indent=2))
        return 0
    if args.command == "serve":
        run(args.host, args.port)
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
