#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LAYER="${1:-smoke}"

cd "$ROOT_DIR"

case "$LAYER" in
  smoke)
    bash ./scripts/run_pytest_layer.sh smoke
    ;;
  full)
    bash ./scripts/run_pytest_layer.sh full
    ;;
  *)
    echo "Unknown layer: $LAYER"
    echo "Usage: bash scripts/run_ci_layer_local.sh [smoke|full]"
    exit 2
    ;;
esac
