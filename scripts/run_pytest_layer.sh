#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LAYER="${1:-full}"
shift || true

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

export HEADLESS="${HEADLESS:-true}"
export BASE_UI_URL="${BASE_UI_URL:-http://localhost:5173}"
export BASE_API_URL="${BASE_API_URL:-http://localhost:3001}"

case "$LAYER" in
  smoke)
    pytest tests/smoke -m smoke "$@"
    ;;
  core)
    pytest tests/smoke tests/regression tests/ui tests/bdd -m "smoke or regression or ui or bdd" "$@"
    ;;
  perf)
    PERF_DOM_CONTENT_LOADED_MAX_MS="${PERF_DOM_CONTENT_LOADED_MAX_MS:-4000}" \
    PERF_NAVIGATION_MAX_MS="${PERF_NAVIGATION_MAX_MS:-6000}" \
      pytest tests/perf -m perf "$@"
    ;;
  full)
    bash "$0" core
    bash "$0" perf
    ;;
  quarantined)
    INCLUDE_QUARANTINED=1 pytest -m "quarantined" "$@"
    ;;
  *)
    echo "Unknown layer: $LAYER"
    echo "Usage: bash scripts/run_pytest_layer.sh [smoke|core|perf|full|quarantined]"
    exit 2
    ;;
esac
