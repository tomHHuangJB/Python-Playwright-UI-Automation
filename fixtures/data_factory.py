from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DemoCredentials:
    username: str
    password: str
    mfa_code: str


@dataclass(frozen=True)
class FormsCase:
    wizard_target_step: int
    array_new_value: str
    rich_text_value: str
    color_value: str
    range_min: str
    range_max: str
    datetime_value: str


@dataclass(frozen=True)
class TestRunContext:
    run_id: str
    worker_id: str
    seed: str


class DataFactory:
    def __init__(self, project_root: Path, run_context: TestRunContext) -> None:
        self.project_root = project_root
        self.run_context = run_context
        self._counter = 0

    def demo_credentials(self) -> DemoCredentials:
        return DemoCredentials(username="principal.engineer", password="demo", mfa_code="123456")

    def forms_case(self) -> FormsCase:
        data_path = self.project_root / "test_data" / "ui" / "forms_cases.json"
        raw_case = json.loads(data_path.read_text())
        return FormsCase(**raw_case)

    def _next_token(self, prefix: str) -> str:
        self._counter += 1
        return (
            f"{prefix}-{self.run_context.run_id}-{self.run_context.worker_id}-"
            f"{self.run_context.seed}-{self._counter:04d}"
        )

    def unique_upload_id(self, prefix: str = "upload") -> str:
        return self._next_token(prefix)

    def unique_order_id(self, prefix: str = "order") -> str:
        return self._next_token(prefix)
