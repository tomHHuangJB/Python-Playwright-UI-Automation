from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def _load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _format_counter(counter: dict[str, int]) -> str:
    if not counter:
        return "none"
    return ", ".join(f"{key}={value}" for key, value in sorted(counter.items()))


def _suite_summary(payload: dict[str, Any] | None) -> dict[str, dict[str, int]]:
    if not payload:
        return {"layers": {}, "routes": {}, "owners": {}}
    return payload.get("summary", {"layers": {}, "routes": {}, "owners": {}})


def _quarantine_summary(payload: dict[str, Any] | None) -> dict[str, Any]:
    if not payload:
        return {"total": 0, "owners": {}}
    return payload.get("summary", {"total": 0, "owners": {}})


def _route_gap_summary(payload: dict[str, Any] | None) -> dict[str, int]:
    if not payload:
        return {"registered_routes": 0, "uncovered_routes": 0}
    return payload.get("summary", {"registered_routes": 0, "uncovered_routes": 0})


def build_summary_payload(args: argparse.Namespace) -> dict[str, Any]:
    suite_catalog = _load_json(Path(args.suite_catalog_json))
    quarantine_report = _load_json(Path(args.quarantine_report_json))
    route_gap_report = _load_json(Path(args.route_gap_report_json))
    suite_summary = _suite_summary(suite_catalog)
    quarantine_summary = _quarantine_summary(quarantine_report)
    route_gap_summary = _route_gap_summary(route_gap_report)
    missing_inputs = [
        name
        for name, payload in (
            (args.suite_catalog_json, suite_catalog),
            (args.quarantine_report_json, quarantine_report),
            (args.route_gap_report_json, route_gap_report),
        )
        if payload is None
    ]

    return {
        "title": args.title,
        "ui_url": args.ui_url,
        "api_url": args.api_url,
        "suite_layers": suite_summary["layers"],
        "route_coverage": suite_summary["routes"],
        "owner_coverage": suite_summary["owners"],
        "quarantined_tests": quarantine_summary["total"],
        "quarantine_owners": quarantine_summary["owners"],
        "registered_routes": route_gap_summary["registered_routes"],
        "uncovered_routes": route_gap_summary["uncovered_routes"],
        "missing_inputs": missing_inputs,
        "artifacts": {
            "allure_report": args.allure_report_artifact,
            "allure_results": args.allure_results_artifact,
            "junit": args.junit_artifact,
            "suite_catalog": args.suite_catalog_artifact,
            "quarantine_report": args.quarantine_report_artifact,
            "route_gap_report": args.route_gap_report_artifact,
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
        f"- Registered app routes: {payload['registered_routes']}",
        f"- Uncovered app routes: {payload['uncovered_routes']}",
        f"- Owner coverage: {_format_counter(payload['owner_coverage'])}",
        f"- Quarantined tests: {payload['quarantined_tests']}",
        f"- Quarantine owners: {_format_counter(payload['quarantine_owners'])}",
        f"- Allure report artifact: `{payload['artifacts']['allure_report']}`",
        f"- Raw Allure results artifact: `{payload['artifacts']['allure_results']}`",
        f"- JUnit XML artifact: `{payload['artifacts']['junit']}`",
        f"- Suite catalog artifact: `{payload['artifacts']['suite_catalog']}`",
        f"- Quarantine report artifact: `{payload['artifacts']['quarantine_report']}`",
        f"- Route gap report artifact: `{payload['artifacts']['route_gap_report']}`",
        f"- Playwright artifact bundle: `{payload['artifacts']['playwright']}`",
    ]
    if payload["missing_inputs"]:
        missing_inputs = ", ".join(f"`{path}`" for path in payload["missing_inputs"])
        lines.append(f"- Missing report inputs: {missing_inputs}")
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
    parser.add_argument("--route-gap-report-json", required=True)
    parser.add_argument("--allure-report-artifact", required=True)
    parser.add_argument("--allure-results-artifact", required=True)
    parser.add_argument("--junit-artifact", required=True)
    parser.add_argument("--suite-catalog-artifact", required=True)
    parser.add_argument("--quarantine-report-artifact", required=True)
    parser.add_argument("--route-gap-report-artifact", required=True)
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
