#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$ROOT_DIR"

if [ -d ".venv" ]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
elif ! command -v pytest >/dev/null; then
  echo "pytest not found. Create .venv and install requirements, or run in an environment with pytest available."
  exit 1
fi

unset PYTEST_PLUGINS
unset PYTEST_ADDOPTS

BASE_UI_URL="${BASE_UI_URL:-http://localhost:5173}"
BASE_API_URL="${BASE_API_URL:-http://localhost:3001}"

require_cmd() {
  local cmd="$1"
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "Missing required command: $cmd"
    exit 1
  fi
}

require_cmd curl
require_cmd python
require_cmd pytest

python - <<'PY'
from importlib.util import find_spec
modules = {
    "playwright": "Playwright Python package",
    "allure_pytest": "allure-pytest package",
}
missing = [label for module, label in modules.items() if find_spec(module) is None]
if missing:
    raise SystemExit("Missing Python packages: " + ", ".join(missing))
PY

if ! python -m playwright install --dry-run chromium >/dev/null 2>&1; then
  echo "Playwright Chromium browser is not available. Run: python -m playwright install chromium"
  exit 1
fi

if ! curl -fsS "$BASE_API_URL/health" >/dev/null; then
  echo "API health check failed at $BASE_API_URL/health"
  exit 1
fi

if ! curl -fsS "$BASE_UI_URL" >/dev/null; then
  echo "UI health check failed at $BASE_UI_URL"
  exit 1
fi

echo "Local environment validation passed."
echo "UI: $BASE_UI_URL"
echo "API: $BASE_API_URL"
