"""Application settings, loaded from backend/.env via pydantic-settings.

Defaults are dev-safe so the service runs with zero config locally (SQLite, no
Supabase). Supabase/AI keys are only needed once those features are wired.
"""

# BaseSettings = a Pydantic model whose fields auto-populate from env vars / .env.
# SettingsConfigDict = the typed config object that tells it where to read from.
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # env_file=".env" → read backend/.env in dev; extra="ignore" → don't error on
    # env vars we haven't declared here (the root .env has frontend-only VITE_* keys).
    # Precedence: real OS env vars > .env file > the defaults below.
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # ── Database ────────────────────────────────────────────────────────────
    # Default = file-based SQLite (zero setup). In prod this is overridden with a
    # Postgres URL, which database.py rewrites to the async (+asyncpg) driver.
    DATABASE_URL: str = "sqlite+aiosqlite:///./community_compass.db"

    # ── Supabase auth (backend verifies tokens; it does not sign users in) ──
    SUPABASE_URL: str = ""              # project URL; used to build the JWKS endpoint
    SUPABASE_JWT_SECRET: str = ""       # HS256 shared secret (also used by tests)
    SUPABASE_SERVICE_ROLE_KEY: str = "" # privileged key for admin-only server calls

    # ── Encryption (Fernet) for PII columns ─────────────────────────────────
    ENCRYPTION_KEY: str = ""            # 32-byte url-safe base64 key; empty until PII lands

    # ── AI providers (assistant + AI-assisted intake) ───────────────────────
    AI_PROVIDER: str = "groq"          # which provider to call: "groq" | "claude" | "ollama"
    GROQ_API_KEY: str = ""             # secret; empty falls back to rule-based behavior later
    GROQ_BASE_URL: str = "https://api.groq.com/openai/v1"  # OpenAI-compatible endpoint
    GROQ_MODEL: str = "llama-3.3-70b-versatile"            # default Groq model
    ANTHROPIC_API_KEY: str = ""        # only needed when AI_PROVIDER="claude"

    # ── CORS ────────────────────────────────────────────────────────────────
    FRONTEND_URL: str = "http://localhost:5173"  # the only origin allowed to call this API


# Module-level singleton — constructed once at import, imported everywhere.
# Never call Settings() again elsewhere; share this instance so config is uniform.
settings = Settings()
