from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class FormsCase:
    wizard_target_step: int
    array_new_value: str
    rich_text_value: str
    color_value: str
    range_min: str
    range_max: str
    datetime_value: str


class ScenarioLoader:
    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root

    def _load_json(self, relative_path: str) -> dict:
        data_path = self.project_root / relative_path
        return json.loads(data_path.read_text())

    def forms_case(self) -> FormsCase:
        return FormsCase(**self._load_json("test_data/ui/forms_cases.json"))
