"""FastAPI app entrypoint for the Community Compass Python service.

Foundation scope: Supabase-verified auth + user profiles + health. Map/AI
(HomeMatch) and caseworker/risk (Future-Path) routes are added in later PRs.
"""

from contextlib import asynccontextmanager           # turns a generator into a startup/shutdown manager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError # raised when request bodies fail validation
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes.assistant import router as assistant_router
from app.api.routes.auth import router as auth_router
from app.api.routes.health import router as health_router
from app.api.routes.housing import router as housing_router
from app.api.routes.intake import router as intake_router
from app.api.routes.recommendations import router as recommendations_router
from app.api.routes.resources import router as resources_router
from app.api.routes.risk import router as risk_router
from app.api.routes.users import router as users_router
from app.core.config import settings
from app.core.database import Base, init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs once on startup (before yield) and once on shutdown (after yield).
    import app.models  # noqa: F401 — importing registers every model on Base.metadata

    engine = init_db(settings.DATABASE_URL)           # build the async engine + session factory
    async with engine.begin() as conn:
        # Dev convenience: create any missing tables. Prod will use Alembic migrations.
        await conn.run_sync(Base.metadata.create_all)
    yield                                              # ← app serves requests here
    await engine.dispose()                             # clean up the connection pool on shutdown


# lifespan wires the startup/shutdown above into the app.
app = FastAPI(title="Community Compass API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],            # only the React app's origin may call us
    allow_credentials=True,                            # allow cookies/Authorization on cross-origin calls
    allow_methods=["*"],                               # GET/POST/PATCH/...
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    # Normalize validation failures to a clean 422 with the field-level errors.
    return JSONResponse(status_code=422, content={"detail": exc.errors()})


app.include_router(health_router)   # GET /health
app.include_router(auth_router)     # /auth/dev-login (dev only)
app.include_router(users_router)    # /users/register, /users/me
app.include_router(intake_router)   # /intake (CC-30)
app.include_router(resources_router)  # /resources (CC-31)
app.include_router(housing_router)    # /housing (CC-32 + CC-10 matching)
app.include_router(recommendations_router)  # /recommendations (CC-33 + CC-13)
app.include_router(assistant_router)  # /assistant (CC-05 + CC-06)
app.include_router(risk_router)       # /risk (Future-Path engine)
