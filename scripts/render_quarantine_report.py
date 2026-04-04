from __future__ import annotations

import argparse
import ast
import csv
import json
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from io import StringIO
from pathlib import Path
from typing import TypedDict

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.suite_catalog import catalog_entry_for_path, collect_suite_catalog  # noqa: E402


@dataclass(frozen=True)
class QuarantinedTest:
    name: str
    reason: str
    path: str
    layer: str
    feature: str
    owner: str
    risk: str

    def as_dict(self) -> dict[str, str]:
        return asdict(self)


class QuarantineSummary(TypedDict):
    total: int
    owners: dict[str, int]
    layers: dict[str, int]
    risks: dict[str, int]


def _quarantine_reason(decorator: ast.expr) -> str | None:
    if not isinstance(decorator, ast.Call):
        return None
    if not isinstance(decorator.func, ast.Attribute):
        return None
    if decorator.func.attr != "quarantined":
        return None
    if not isinstance(decorator.func.value, ast.Attribute):
        return None
    if decorator.func.value.attr != "mark":
        return None

    if decorator.args and isinstance(decorator.args[0], ast.Constant):
        value = decorator.args[0].value
        if isinstance(value, str):
            return value
    return "No reason recorded"


def collect_quarantined_tests(root: Path) -> list[QuarantinedTest]:
    tests_root = root / "tests"
    entries_by_path = {entry.path: entry for entry in collect_suite_catalog(root)}
    quarantined: list[QuarantinedTest] = []

    for path in sorted(tests_root.rglob("test_*.py")):
        relative_path = str(path.relative_to(root))
        entry = entries_by_path.get(relative_path) or catalog_entry_for_path(path, root)
        module = ast.parse(path.read_text(encoding="utf-8"))
        for node in module.body:
            if not isinstance(node, ast.FunctionDef):
                continue
            for decorator in node.decorator_list:
                reason = _quarantine_reason(decorator)
                if reason is None:
                    continue
                quarantined.append(
                    QuarantinedTest(
                        name=node.name,
                        reason=reason,
                        path=relative_path,
                        layer=entry.layer,
                        feature=entry.feature,
                        owner=entry.owner,
                        risk=entry.risk,
                    )
                )
    return quarantined


def build_summary(tests: list[QuarantinedTest]) -> QuarantineSummary:
    return {
        "total": len(tests),
        "owners": dict(sorted(Counter(test.owner for test in tests).items())),
        "layers": dict(sorted(Counter(test.layer for test in tests).items())),
        "risks": dict(sorted(Counter(test.risk for test in tests).items())),
    }


def build_markdown(tests: list[QuarantinedTest]) -> str:
    summary = build_summary(tests)
    owner_summary = (
        ", ".join(f"{owner}={count}" for owner, count in summary["owners"].items()) or "none"
    )
    layer_summary = (
        ", ".join(f"{layer}={count}" for layer, count in summary["layers"].items()) or "none"
    )
    risk_summary = (
        ", ".join(f"{risk}={count}" for risk, count in summary["risks"].items()) or "none"
    )

    lines = [
        "# Quarantine Report",
        "",
        f"- Total quarantined tests: {summary['total']}",
        f"- Owners: {owner_summary}",
        f"- Layers: {layer_summary}",
        f"- Risks: {risk_summary}",
        "",
        "| Test | Reason | Owner | Layer | Risk | Path |",
        "| --- | --- | --- | --- | --- | --- |",
    ]

    for test in tests:
        lines.append(
            f"| `{test.name}` | {test.reason} | {test.owner} | {test.layer} | "
            f"{test.risk} | `{test.path}` |"
        )
    return "\n".join(lines)


def build_csv(tests: list[QuarantinedTest]) -> str:
    fieldnames = ["name", "reason", "owner", "layer", "risk", "path"]
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    for test in tests:
        writer.writerow(test.as_dict())
    return output.getvalue()


def main() -> int:
    parser = argparse.ArgumentParser(description="Render the quarantine test report.")
    parser.add_argument(
        "--format",
        choices=("markdown", "json", "csv"),
        default="markdown",
        help="Output format.",
    )
    args = parser.parse_args()

    tests = collect_quarantined_tests(ROOT)
    summary = build_summary(tests)
    if args.format == "json":
        print(
            json.dumps(
                {
                    "summary": summary,
                    "tests": [test.as_dict() for test in tests],
                },
                indent=2,
            )
        )
        return 0

    if args.format == "csv":
        print(build_csv(tests), end="")
        return 0

    print(build_markdown(tests))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
