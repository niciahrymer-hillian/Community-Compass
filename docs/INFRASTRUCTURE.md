# Infrastructure & Secrets Setup

How to wire up the API keys, Supabase, the database, and Render deployment for
Community Compass. **Never commit real keys** — the `.env` files are git-ignored,
so real values stay local; in production they go in the Render dashboard. The
full key schema is documented here and in [`render.yaml`](../render.yaml).

## Architecture (target)

Community Compass is polyglot (see the user stories' "Team Fit"):

| Tier | Tech | Source repo | Responsibility |
|------|------|-------------|----------------|
| Frontend | React + Vite + Tailwind + Leaflet | — | intake form, dashboards, map view |
| Java service | Spring Boot | kindConnect | user dashboard, newsfeed |
| Python service | FastAPI + SQLAlchemy | HomeMatch, Future-Path | map/housing matching, caseworker risk-scoring, AI-assisted intake |
| Data + auth | Supabase (Postgres + Auth) / Render Postgres | — | users, intake, resources, risk scores, RBAC |

All backends verify the **same Supabase JWT**, so a user signs in once and both
services trust the token.

## 1. Supabase (auth + Postgres)

1. Create a project at <https://supabase.com>.
2. **Project Settings → API**, copy:
   - `Project URL` → `SUPABASE_URL` (and `VITE_SUPABASE_URL`)
   - `anon public` key → `SUPABASE_ANON_KEY` (and `VITE_SUPABASE_ANON_KEY`)
   - `service_role` key → `SUPABASE_SERVICE_ROLE_KEY` (backend only — **secret**)
3. **Project Settings → API → JWT Settings**, copy `JWT Secret` → `SUPABASE_JWT_SECRET`.
4. **Project Settings → Database**, copy the connection string → `DATABASE_URL`
   (Python rewrites `postgresql://` → `postgresql+asyncpg://` automatically).

## 2. AI keys

- **Groq** (default, free): create a key at <https://console.groq.com> → `GROQ_API_KEY`.
- **Anthropic** (optional, if `AI_PROVIDER=claude`): <https://console.anthropic.com> → `ANTHROPIC_API_KEY`.
- **ElevenLabs** (optional voice): <https://elevenlabs.io> → `ELEVENLABS_API_KEY`.

## 3. Encryption key (PII at rest)

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```
Put the output in `ENCRYPTION_KEY`. **Do not rotate in production** without
re-encrypting existing rows first.

## 4. Local development

The git-ignored `.env` (root) and `backend/.env` already exist with placeholders
— just fill in real values, then run the python service:
```bash
cd backend && .venv/bin/uvicorn app.main:app --reload
```
With the SQLite default `DATABASE_URL`, the Python service runs with **zero
external setup** — Supabase is only required once you wire real auth.

## 5. Render deployment

The repo ships a [`render.yaml`](../render.yaml) blueprint.

1. In Render, **New → Blueprint**, point it at this repo.
2. Render reads `render.yaml` and provisions: the Postgres DB, the shared Env
   Group, and the Python service.
3. For every `sync: false` var, Render prompts you for the value (paste the keys
   from steps 1–3). Set them once in the **community-compass-shared** Env Group.
4. The Java service and React frontend are commented out in `render.yaml` — they
   get enabled in their own PRs once `java-service/` and `frontend/` exist.

### Secret → where it lives

| Secret | Local | Render |
|--------|-------|--------|
| `SUPABASE_*`, `ENCRYPTION_KEY`, `*_API_KEY` | `backend/.env` | `community-compass-shared` Env Group (`sync: false`) |
| `DATABASE_URL` | `backend/.env` (SQLite) | auto-injected from the `community-compass-db` Postgres |
| `VITE_*` (public) | `frontend/.env` | the static-site service env (added later) |
