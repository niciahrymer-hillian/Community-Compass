#!/usr/bin/env bash
# Start everything for Community Compass: Python API (:8000), Java service (:8080),
# and the React/Vite app (:5173). Ctrl-C stops them all.
#
#   ./start.sh
#
# Then open http://localhost:5173 (VS Code: "Simple Browser: Show", or run the
# "🚀 Start Community Compass" task which opens it for you).

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

# Stop anything we previously started so ports 8000/8080/5173 are free.
pkill -f "uvicorn app.main:app" 2>/dev/null
pkill -f "spring-boot:run" 2>/dev/null
pkill -f "node.*vite" 2>/dev/null
sleep 1

# Kill our child servers when this script exits (Ctrl-C included).
cleanup() {
  echo ""
  echo "Stopping Community Compass…"
  pkill -f "uvicorn app.main:app" 2>/dev/null
  pkill -f "spring-boot:run" 2>/dev/null
  pkill -f "node.*vite" 2>/dev/null
}
trap cleanup EXIT INT TERM

echo "→ Seeding demo data (idempotent)…"
( cd backend && ./.venv/bin/python -m scripts.seed ) || echo "  (seed skipped)"

echo "→ Python API   → http://localhost:8000"
( cd backend && ./.venv/bin/uvicorn app.main:app --reload --port 8000 ) 2>&1 | sed 's/^/[api]  /' &

echo "→ Java service → http://localhost:8080"
( cd java-service && JAVA_HOME="$(/usr/libexec/java_home -v 17)" mvn -q spring-boot:run ) 2>&1 | sed 's/^/[java] /' &

echo "→ Web (Vite)   → http://localhost:5173"
( cd frontend && npm run dev ) 2>&1 | sed 's/^/[web]  /' &

echo ""
echo "Community Compass is starting. Open http://localhost:5173 — Ctrl-C to stop."
wait
