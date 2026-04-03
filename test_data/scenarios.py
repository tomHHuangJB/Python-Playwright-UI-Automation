from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, TypeVar


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
class ScenarioSpec:
    name: str
    relative_path: str
    model_type: type[object]


ScenarioModel = TypeVar("ScenarioModel")


class ScenarioLoader:
    FORMS_CASE = ScenarioSpec(
        name="forms_case",
        relative_path="test_data/ui/forms_cases.json",
        model_type=FormsCase,
    )

    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root

    @classmethod
    def registry(cls) -> tuple[ScenarioSpec, ...]:
        return (cls.FORMS_CASE,)

    def available_scenarios(self) -> tuple[str, ...]:
        return tuple(spec.name for spec in self.registry())

    def _load_json(self, relative_path: str) -> dict[str, Any]:
        data_path = self.project_root / relative_path
        return json.loads(data_path.read_text())

    def load(self, spec: ScenarioSpec, model_type: type[ScenarioModel]) -> ScenarioModel:
        payload = self._load_json(spec.relative_path)
        return model_type(**payload)

    def forms_case(self) -> FormsCase:
        return self.load(self.FORMS_CASE, FormsCase)
