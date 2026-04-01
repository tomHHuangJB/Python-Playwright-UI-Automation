#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APP_DIR="${LOCAL_AUTOMATION_APP_DIR:-/Users/tomhuang/prog/LocalAutomationApp}"
BACKEND_LOG="$ROOT_DIR/.local-automation-backend.log"
FRONTEND_LOG="$ROOT_DIR/.local-automation-frontend.log"
PID_FILE="$ROOT_DIR/.local-automation-pids"
BACKEND_PORT=3001
FRONTEND_PORT=5173

if [ ! -d "$APP_DIR" ]; then
  echo "LocalAutomationApp not found at: $APP_DIR"
  echo "Set LOCAL_AUTOMATION_APP_DIR to your LocalAutomationApp checkout."
  exit 1
fi

if ! command -v curl >/dev/null 2>&1; then
  echo "curl is required for health checks."
  exit 1
fi

if ! command -v npm >/dev/null 2>&1; then
  echo "npm is required to build and start LocalAutomationApp."
  exit 1
fi

stop_pid_if_running() {
  local pid="$1"
  if [ -n "$pid" ] && kill -0 "$pid" >/dev/null 2>&1; then
    kill "$pid" >/dev/null 2>&1 || true
    wait "$pid" 2>/dev/null || true
  fi
}

stop_port_if_busy() {
  local port="$1"
  if command -v lsof >/dev/null 2>&1; then
    local pids
    pids="$(lsof -ti :"$port" 2>/dev/null || true)"
    if [ -n "$pids" ]; then
      echo "Stopping process(es) on port $port: $pids"
      kill $pids >/dev/null 2>&1 || true
    fi
  fi
}

if [ -f "$PID_FILE" ]; then
  read -r old_backend_pid old_frontend_pid < "$PID_FILE" || true
  stop_pid_if_running "${old_backend_pid:-}"
  stop_pid_if_running "${old_frontend_pid:-}"
  rm -f "$PID_FILE"
fi

stop_port_if_busy "$BACKEND_PORT"
stop_port_if_busy "$FRONTEND_PORT"

echo "Starting LocalAutomationApp from: $APP_DIR"

pushd "$APP_DIR/backend" >/dev/null
if [ -f package-lock.json ]; then
  npm ci
else
  npm install
fi
npm run build
node dist/index.js > "$BACKEND_LOG" 2>&1 &
BACKEND_PID=$!
popd >/dev/null

pushd "$APP_DIR/frontend" >/dev/null
if [ -f package-lock.json ]; then
  npm ci
else
  npm install
fi
VITE_API_URL="http://localhost:3001" npm run build
npx serve -s dist -l "$FRONTEND_PORT" > "$FRONTEND_LOG" 2>&1 &
FRONTEND_PID=$!
popd >/dev/null

echo "$BACKEND_PID $FRONTEND_PID" > "$PID_FILE"

for _ in {1..30}; do
  if curl -fsS "http://localhost:${BACKEND_PORT}/health" >/dev/null && curl -fsS "http://localhost:${FRONTEND_PORT}" >/dev/null; then
    echo "LocalAutomationApp is up."
    echo "UI: http://localhost:${FRONTEND_PORT}"
    echo "API: http://localhost:${BACKEND_PORT}"
    echo "PIDs saved in $PID_FILE"
    exit 0
  fi
  sleep 2
done

echo "LocalAutomationApp did not start in time."
echo "Check logs:"
echo "  $BACKEND_LOG"
echo "  $FRONTEND_LOG"
exit 1
