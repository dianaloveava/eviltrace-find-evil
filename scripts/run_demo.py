from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from eviltrace.agent import InvestigationAgent, render_markdown_report


if __name__ == "__main__":
    run = InvestigationAgent("case_alpha").run()
    print(f"Created {run.id}")
    print(render_markdown_report(run))
