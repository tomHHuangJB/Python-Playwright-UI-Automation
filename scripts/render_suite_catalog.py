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


def build_markdown(root: Path) -> str:
    entries = collect_suite_catalog(root)
    layer_counts = Counter(entry.layer for entry in entries)
    layer_summary = ", ".join(f"{layer}={count}" for layer, count in sorted(layer_counts.items()))

    lines = [
        "# Suite Catalog",
        "",
        f"- Total test entry files: {len(entries)}",
        f"- Layers: {layer_summary}",
        "",
        "| Layer | Feature | Owner | Risk | Path |",
        "| --- | --- | --- | --- | --- |",
    ]
    for entry in entries:
        lines.append(
            f"| {entry.layer} | {entry.feature} | {entry.owner} | {entry.risk} | `{entry.path}` |"
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

    if args.format == "json":
        print(json.dumps([entry.as_dict() for entry in entries], indent=2))
        return 0

    print(build_markdown(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
