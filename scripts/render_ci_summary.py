from __future__ import annotations

import argparse
import json
from pathlib import Path


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _format_counter(counter: dict[str, int]) -> str:
    if not counter:
        return "none"
    return ", ".join(f"{key}={value}" for key, value in sorted(counter.items()))


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a GitHub job summary for CI reports.")
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

    suite_catalog = _load_json(Path(args.suite_catalog_json))
    quarantine_report = _load_json(Path(args.quarantine_report_json))

    suite_summary = suite_catalog["summary"]
    quarantine_summary = quarantine_report["summary"]

    lines = [
        f"## {args.title}",
        "",
        f"- UI target: {args.ui_url}",
        f"- API target: {args.api_url}",
        f"- Suite layers: {_format_counter(suite_summary['layers'])}",
        f"- Route coverage: {_format_counter(suite_summary['routes'])}",
        f"- Owner coverage: {_format_counter(suite_summary['owners'])}",
        f"- Quarantined tests: {quarantine_summary['total']}",
        f"- Quarantine owners: {_format_counter(quarantine_summary['owners'])}",
        f"- Allure report artifact: `{args.allure_report_artifact}`",
        f"- Raw Allure results artifact: `{args.allure_results_artifact}`",
        f"- JUnit XML artifact: `{args.junit_artifact}`",
        f"- Suite catalog artifact: `{args.suite_catalog_artifact}`",
        f"- Quarantine report artifact: `{args.quarantine_report_artifact}`",
        f"- Playwright artifact bundle: `{args.playwright_artifact}`",
    ]
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
