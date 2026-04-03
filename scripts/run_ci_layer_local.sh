#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LAYER="${1:-smoke}"

cd "$ROOT_DIR"

if [ ! -d ".venv" ]; then
  echo ".venv not found. Create it first with: python3 -m venv .venv"
  exit 1
fi

# shellcheck disable=SC1091
source .venv/bin/activate

unset PYTEST_PLUGINS
unset PYTEST_ADDOPTS

export HEADLESS="${HEADLESS:-true}"
export BASE_UI_URL="${BASE_UI_URL:-http://localhost:5173}"
export BASE_API_URL="${BASE_API_URL:-http://localhost:3001}"

case "$LAYER" in
  smoke)
    pytest tests/smoke -m smoke
    ;;
  full)
    pytest tests/regression tests/ui -m "regression or ui"
    PERF_DOM_CONTENT_LOADED_MAX_MS="${PERF_DOM_CONTENT_LOADED_MAX_MS:-4000}" \
    PERF_NAVIGATION_MAX_MS="${PERF_NAVIGATION_MAX_MS:-6000}" \
      pytest tests/perf -m perf
    ;;
  *)
    echo "Unknown layer: $LAYER"
    echo "Usage: bash scripts/run_ci_layer_local.sh [smoke|full]"
    exit 2
    ;;
esac
