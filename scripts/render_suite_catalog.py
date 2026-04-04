from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.suite_catalog import collect_suite_catalog  # noqa: E402


def build_summary(entries: list) -> dict[str, dict[str, int]]:
    return {
        "layers": dict(sorted(Counter(entry.layer for entry in entries).items())),
        "owners": dict(sorted(Counter(entry.owner for entry in entries).items())),
        "risks": dict(sorted(Counter(entry.risk for entry in entries).items())),
        "routes": dict(
            sorted(Counter(route for entry in entries for route in entry.routes).items())
        ),
    }


def build_markdown(root: Path) -> str:
    entries = collect_suite_catalog(root)
    summary = build_summary(entries)
    layer_summary = ", ".join(f"{layer}={count}" for layer, count in summary["layers"].items())
    owner_summary = ", ".join(f"{owner}={count}" for owner, count in summary["owners"].items())
    risk_summary = ", ".join(f"{risk}={count}" for risk, count in summary["risks"].items())
    route_summary = ", ".join(f"{route}={count}" for route, count in summary["routes"].items())

    lines = [
        "# Suite Catalog",
        "",
        f"- Total test entry files: {len(entries)}",
        f"- Layers: {layer_summary}",
        f"- Owners: {owner_summary}",
        f"- Risks: {risk_summary}",
        f"- Routes: {route_summary}",
        "",
        "| Layer | Feature | Owner | Risk | Routes | Scenarios | Path |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for entry in entries:
        routes = ", ".join(f"`{route}`" for route in entry.routes)
        lines.append(
            f"| {entry.layer} | {entry.feature} | {entry.owner} | {entry.risk} | "
            f"{routes} | {entry.scenario_count} | `{entry.path}` |"
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render the test suite catalog.")
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Output format.",
    )
    args = parser.parse_args()

    entries = collect_suite_catalog(ROOT)
    summary = build_summary(entries)

    if args.format == "json":
        print(
            json.dumps(
                {
                    "summary": summary,
                    "entries": [entry.as_dict() for entry in entries],
                },
                indent=2,
            )
        )
        return 0

    print(build_markdown(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
