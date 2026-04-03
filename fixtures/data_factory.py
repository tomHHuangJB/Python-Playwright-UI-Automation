from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4


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


class DataFactory:
    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root

    def demo_credentials(self) -> DemoCredentials:
        return DemoCredentials(username="principal.engineer", password="demo", mfa_code="123456")

    def forms_case(self) -> FormsCase:
        data_path = self.project_root / "test_data" / "ui" / "forms_cases.json"
        raw_case = json.loads(data_path.read_text())
        return FormsCase(**raw_case)

    def unique_upload_id(self, prefix: str = "upload") -> str:
        return f"{prefix}-{uuid4().hex[:12]}"

    def unique_order_id(self, prefix: str = "order") -> str:
        return f"{prefix}-{uuid4().hex[:12]}"
