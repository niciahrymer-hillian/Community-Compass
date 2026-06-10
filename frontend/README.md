# Community Compass — Web (React + Vite + Leaflet)

Resident-facing frontend: dev login, guided intake, personalized dashboard
(recommendations), housing map, and resource search.

## Run
```bash
cd frontend
npm install
npm run dev          # http://localhost:5173
```
The Python API must be running on http://localhost:8000 (override with
`VITE_PYTHON_API_URL`). Seed demo data first so there's something to show:
```bash
cd ../backend && .venv/bin/python -m scripts.seed
```

## Pages
- `/login` — dev sign-in (`POST /auth/dev-login`; production uses Supabase).
- `/intake` — guided intake form (CC-04) → `POST /intake`.
- `/dashboard` — recommendations (CC-07) → `GET /recommendations/me`.
- `/housing` — Leaflet map of listings (CC-11) → `GET /housing` (public).
- `/resources` — search/filter resources (CC-14) → `GET /resources` (public).
