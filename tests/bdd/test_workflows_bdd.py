from pathlib import Path

from pytest_bdd import scenarios

FEATURES_DIR = Path(__file__).resolve().parents[2] / "features"

scenarios(str(FEATURES_DIR / "auth_workflow.feature"))
scenarios(str(FEATURES_DIR / "forms_workflow.feature"))
scenarios(str(FEATURES_DIR / "tables_workflow.feature"))
scenarios(str(FEATURES_DIR / "dynamic_workflow.feature"))
scenarios(str(FEATURES_DIR / "files_workflow.feature"))
