#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$ROOT_DIR"

if [ -d ".venv" ]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
elif ! command -v ruff >/dev/null || ! command -v black >/dev/null || ! command -v mypy >/dev/null; then
  echo "Quality tools not found. Create .venv and install requirements, or run in an environment with ruff, black, and mypy available."
  exit 1
fi

unset PYTEST_PLUGINS
unset PYTEST_ADDOPTS

ruff check .
black --check .
mypy --explicit-package-bases config fixtures flows utils
python scripts/validate_suite_catalog.py
