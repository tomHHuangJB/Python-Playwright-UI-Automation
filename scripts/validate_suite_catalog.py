from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.suite_catalog import (  # noqa: E402
    LAYER_LABELS,
    OWNER_BY_FEATURE,
    RISK_BY_LAYER,
    collect_suite_catalog,
)


def main() -> int:
    entries = collect_suite_catalog(ROOT)
    failures: list[str] = []

    if not entries:
        failures.append("No test entry files were found under tests/.")

    seen_paths: set[str] = set()
    layer_counts = Counter(entry.layer for entry in entries)

    for entry in entries:
        if entry.path in seen_paths:
            failures.append(f"Duplicate catalog path detected: {entry.path}")
        seen_paths.add(entry.path)

        if entry.layer not in LAYER_LABELS:
            failures.append(f"Unknown layer for {entry.path}: {entry.layer}")

        expected_risk = RISK_BY_LAYER.get(entry.layer)
        if entry.risk != expected_risk:
            failures.append(
                f"Risk mismatch for {entry.path}: expected {expected_risk}, got {entry.risk}"
            )

        expected_owner = OWNER_BY_FEATURE.get(entry.feature, "quality-engineering")
        if entry.owner != expected_owner:
            failures.append(
                f"Owner mismatch for {entry.path}: expected {expected_owner}, got {entry.owner}"
            )

        if not entry.routes:
            failures.append(f"No routes recorded for {entry.path}")
        elif any(not route.startswith("/") for route in entry.routes):
            failures.append(f"Invalid route mapping for {entry.path}: {entry.routes}")

        if entry.scenario_count < 1:
            failures.append(
                f"Scenario count must be positive for {entry.path}: got {entry.scenario_count}"
            )

    missing_layers = [layer for layer in LAYER_LABELS if layer_counts[layer] == 0]
    if missing_layers:
        failures.append(f"Missing suite coverage for layer(s): {', '.join(missing_layers)}")

    if failures:
        print("Suite catalog validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(
        "Suite catalog validation passed: "
        + ", ".join(f"{layer}={layer_counts[layer]}" for layer in LAYER_LABELS)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
