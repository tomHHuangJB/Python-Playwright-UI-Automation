#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$ROOT_DIR"

if [ ! -d ".venv" ]; then
  echo ".venv not found. Create it first with: python3 -m venv .venv"
  exit 1
fi

# shellcheck disable=SC1091
source .venv/bin/activate

unset PYTEST_PLUGINS
unset PYTEST_ADDOPTS

export HEADLESS="${HEADLESS:-false}"
export BASE_UI_URL="${BASE_UI_URL:-http://localhost:5173}"
export BASE_API_URL="${BASE_API_URL:-http://localhost:3001}"

bash ./scripts/run_quality_checks.sh
bash ./scripts/run_ci_layer_local.sh full
