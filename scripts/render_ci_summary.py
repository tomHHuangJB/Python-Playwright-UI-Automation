from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _format_counter(counter: dict[str, int]) -> str:
    if not counter:
        return "none"
    return ", ".join(f"{key}={value}" for key, value in sorted(counter.items()))


def build_summary_payload(args: argparse.Namespace) -> dict[str, Any]:
    suite_catalog = _load_json(Path(args.suite_catalog_json))
    quarantine_report = _load_json(Path(args.quarantine_report_json))

    suite_summary = suite_catalog["summary"]
    quarantine_summary = quarantine_report["summary"]

    return {
        "title": args.title,
        "ui_url": args.ui_url,
        "api_url": args.api_url,
        "suite_layers": suite_summary["layers"],
        "route_coverage": suite_summary["routes"],
        "owner_coverage": suite_summary["owners"],
        "quarantined_tests": quarantine_summary["total"],
        "quarantine_owners": quarantine_summary["owners"],
        "artifacts": {
            "allure_report": args.allure_report_artifact,
            "allure_results": args.allure_results_artifact,
            "junit": args.junit_artifact,
            "suite_catalog": args.suite_catalog_artifact,
            "quarantine_report": args.quarantine_report_artifact,
            "playwright": args.playwright_artifact,
        },
    }


def build_markdown(payload: dict[str, Any]) -> str:
    lines = [
        f"## {payload['title']}",
        "",
        f"- UI target: {payload['ui_url']}",
        f"- API target: {payload['api_url']}",
        f"- Suite layers: {_format_counter(payload['suite_layers'])}",
        f"- Route coverage: {_format_counter(payload['route_coverage'])}",
        f"- Owner coverage: {_format_counter(payload['owner_coverage'])}",
        f"- Quarantined tests: {payload['quarantined_tests']}",
        f"- Quarantine owners: {_format_counter(payload['quarantine_owners'])}",
        f"- Allure report artifact: `{payload['artifacts']['allure_report']}`",
        f"- Raw Allure results artifact: `{payload['artifacts']['allure_results']}`",
        f"- JUnit XML artifact: `{payload['artifacts']['junit']}`",
        f"- Suite catalog artifact: `{payload['artifacts']['suite_catalog']}`",
        f"- Quarantine report artifact: `{payload['artifacts']['quarantine_report']}`",
        f"- Playwright artifact bundle: `{payload['artifacts']['playwright']}`",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a GitHub job summary for CI reports.")
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Output format.",
    )
    parser.add_argument("--title", required=True)
    parser.add_argument("--ui-url", required=True)
    parser.add_argument("--api-url", required=True)
    parser.add_argument("--suite-catalog-json", required=True)
    parser.add_argument("--quarantine-report-json", required=True)
    parser.add_argument("--allure-report-artifact", required=True)
    parser.add_argument("--allure-results-artifact", required=True)
    parser.add_argument("--junit-artifact", required=True)
    parser.add_argument("--suite-catalog-artifact", required=True)
    parser.add_argument("--quarantine-report-artifact", required=True)
    parser.add_argument("--playwright-artifact", required=True)
    args = parser.parse_args()

    payload = build_summary_payload(args)

    if args.format == "json":
        print(json.dumps(payload, indent=2))
        return 0

    print(build_markdown(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
