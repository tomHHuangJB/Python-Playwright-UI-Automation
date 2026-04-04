from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

import allure

LAYER_LABELS = ("smoke", "bdd", "ui", "regression", "perf")
SEVERITY_BY_LAYER = {
    "smoke": allure.severity_level.CRITICAL,
    "bdd": allure.severity_level.CRITICAL,
    "ui": allure.severity_level.NORMAL,
    "regression": allure.severity_level.NORMAL,
    "perf": allure.severity_level.MINOR,
}
FEATURE_NAME_OVERRIDES = {
    "a11y": "Accessibility",
    "auth": "Authentication",
    "components": "Components",
    "debug_panel": "Debug Panel",
    "dynamic": "Dynamic Behavior",
    "errors": "Errors",
    "experiments": "Experiments",
    "files": "Files",
    "forms": "Forms",
    "grpc": "gRPC",
    "home": "Home",
    "i18n": "Internationalization",
    "integrations": "Integrations",
    "mobile": "Mobile",
    "navigation": "Navigation",
    "performance": "Performance",
    "selectors": "Selectors",
    "system": "System",
    "tables": "Tables",
    "workflow": "Business Workflows",
}
OWNER_BY_FEATURE = {
    "Accessibility": "quality-engineering",
    "Authentication": "identity-platform",
    "Business Workflows": "quality-engineering",
    "Components": "frontend-platform",
    "Debug Panel": "quality-engineering",
    "Dynamic Behavior": "frontend-platform",
    "Errors": "platform-reliability",
    "Experiments": "growth-platform",
    "Files": "content-platform",
    "Forms": "frontend-platform",
    "gRPC": "backend-platform",
    "Home": "frontend-platform",
    "Internationalization": "frontend-platform",
    "Integrations": "integrations-platform",
    "Mobile": "mobile-experience",
    "Navigation": "frontend-platform",
    "Performance": "platform-reliability",
    "Selectors": "quality-engineering",
    "System": "platform-reliability",
    "Tables": "frontend-platform",
    "General": "quality-engineering",
}
RISK_BY_LAYER = {
    "smoke": "critical-path",
    "bdd": "business-critical",
    "ui": "workflow",
    "regression": "broad-regression",
    "perf": "performance-guardrail",
}
ROUTES_BY_FEATURE = {
    "Accessibility": ("/a11y",),
    "Authentication": ("/auth",),
    "Business Workflows": ("/auth", "/forms", "/tables", "/dynamic", "/files"),
    "Components": ("/components",),
    "Debug Panel": ("/",),
    "Dynamic Behavior": ("/dynamic",),
    "Errors": ("/errors",),
    "Experiments": ("/experiments",),
    "Files": ("/files",),
    "Forms": ("/forms",),
    "gRPC": ("/grpc",),
    "Home": ("/",),
    "Internationalization": ("/i18n",),
    "Integrations": ("/integrations",),
    "Mobile": ("/mobile",),
    "Navigation": ("/", "/auth", "/forms", "/tables", "/dynamic"),
    "Performance": ("/performance",),
    "Selectors": ("/",),
    "System": ("/system",),
    "Tables": ("/tables",),
    "General": ("/",),
}


@dataclass(frozen=True)
class SuiteCatalogEntry:
    layer: str
    feature: str
    owner: str
    risk: str
    path: str
    routes: tuple[str, ...]
    scenario_count: int

    def as_dict(self) -> dict[str, str | int | list[str]]:
        data = asdict(self)
        data["routes"] = list(self.routes)
        return data


def layer_for_path(path: Path) -> str:
    path_parts = path.parts
    for layer in LAYER_LABELS:
        if layer in path_parts:
            return layer
    return "ui"


def feature_for_path(path: Path) -> str:
    normalized_path = str(path).lower()
    for key, label in FEATURE_NAME_OVERRIDES.items():
        if key in normalized_path:
            return label

    stem = path.stem.replace("test_", "").replace("_", " ").title()
    return stem or "General"


def owner_for_feature(feature: str) -> str:
    return OWNER_BY_FEATURE.get(feature, "quality-engineering")


def routes_for_feature(feature: str) -> tuple[str, ...]:
    return ROUTES_BY_FEATURE.get(feature, ("/",))


def scenario_count_for_path(path: Path, root: Path) -> int:
    if "bdd" not in path.parts:
        return 1

    feature_dir = root / "features"
    count = 0
    for feature_file in feature_dir.glob("*_workflow.feature"):
        lines = feature_file.read_text(encoding="utf-8").splitlines()
        count += sum(1 for line in lines if line.lstrip().startswith("Scenario:"))
    return count or 1


def catalog_entry_for_path(path: Path, root: Path) -> SuiteCatalogEntry:
    layer = layer_for_path(path)
    feature = feature_for_path(path)
    return SuiteCatalogEntry(
        layer=layer,
        feature=feature,
        owner=owner_for_feature(feature),
        risk=RISK_BY_LAYER[layer],
        path=str(path.relative_to(root)),
        routes=routes_for_feature(feature),
        scenario_count=scenario_count_for_path(path, root),
    )


def collect_suite_catalog(root: Path) -> list[SuiteCatalogEntry]:
    tests_root = root / "tests"
    entries = [catalog_entry_for_path(path, root) for path in sorted(tests_root.rglob("test_*.py"))]
    return sorted(entries, key=lambda entry: (entry.layer, entry.feature, entry.path))
