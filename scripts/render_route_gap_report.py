from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from io import StringIO
from pathlib import Path
from typing import TypedDict

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.suite_catalog import (  # noqa: E402
    collect_suite_catalog,
    registered_app_routes,
)


class RouteGapRow(TypedDict):
    route: str
    covered: bool
    layer_count: int
    layers: list[str]
    features: list[str]
    owners: list[str]
    paths: list[str]


class RouteGapSummary(TypedDict):
    registered_routes: int
    covered_routes: int
    uncovered_routes: int
    layer_coverage: dict[str, int]


def build_rows(root: Path) -> list[RouteGapRow]:
    entries = collect_suite_catalog(root)
    by_route: dict[str, list] = defaultdict(list)
    for entry in entries:
        for route in entry.routes:
            by_route[route].append(entry)

    rows: list[RouteGapRow] = []
    for route in sorted(registered_app_routes()):
        route_entries = by_route.get(route, [])
        rows.append(
            {
                "route": route,
                "covered": bool(route_entries),
                "layer_count": len({entry.layer for entry in route_entries}),
                "layers": sorted({entry.layer for entry in route_entries}),
                "features": sorted({entry.feature for entry in route_entries}),
                "owners": sorted({entry.owner for entry in route_entries}),
                "paths": sorted({entry.path for entry in route_entries}),
            }
        )
    return rows


def build_summary(rows: list[RouteGapRow]) -> RouteGapSummary:
    return {
        "registered_routes": len(rows),
        "covered_routes": sum(1 for row in rows if row["covered"]),
        "uncovered_routes": sum(1 for row in rows if not row["covered"]),
        "layer_coverage": dict(
            sorted(
                Counter(layer for row in rows for layer in row["layers"]).items(),
            )
        ),
    }


def build_markdown(rows: list[RouteGapRow]) -> str:
    summary = build_summary(rows)
    layer_summary = (
        ", ".join(f"{layer}={count}" for layer, count in summary["layer_coverage"].items())
        or "none"
    )
    lines = [
        "# Route Gap Report",
        "",
        f"- Registered routes: {summary['registered_routes']}",
        f"- Covered routes: {summary['covered_routes']}",
        f"- Uncovered routes: {summary['uncovered_routes']}",
        f"- Layer coverage: {layer_summary}",
        "",
        "| Route | Covered | Layers | Features | Owners | Paths |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| `{row['route']}` | {'yes' if row['covered'] else 'no'} | "
            f"{', '.join(row['layers']) or 'none'} | "
            f"{', '.join(row['features']) or 'none'} | "
            f"{', '.join(row['owners']) or 'none'} | "
            f"{', '.join(f'`{path}`' for path in row['paths']) or 'none'} |"
        )
    return "\n".join(lines)


def build_csv(rows: list[RouteGapRow]) -> str:
    fieldnames = ["route", "covered", "layer_count", "layers", "features", "owners", "paths"]
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    for row in rows:
        writer.writerow(
            {
                "route": row["route"],
                "covered": str(row["covered"]).lower(),
                "layer_count": row["layer_count"],
                "layers": ",".join(row["layers"]),
                "features": ",".join(row["features"]),
                "owners": ",".join(row["owners"]),
                "paths": ",".join(row["paths"]),
            }
        )
    return output.getvalue()


def main() -> int:
    parser = argparse.ArgumentParser(description="Render the route coverage gap report.")
    parser.add_argument(
        "--format",
        choices=("markdown", "json", "csv"),
        default="markdown",
        help="Output format.",
    )
    args = parser.parse_args()

    rows = build_rows(ROOT)
    if args.format == "json":
        print(json.dumps({"summary": build_summary(rows), "routes": rows}, indent=2))
        return 0

    if args.format == "csv":
        print(build_csv(rows), end="")
        return 0

    print(build_markdown(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
