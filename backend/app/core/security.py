"""Supabase JWT verification and the get_current_user dependency.

Adapted from HomeMatch. Supabase signs user JWTs; this service only *verifies*
them. Two algorithms are accepted:
  - HS256  → Supabase's legacy shared secret (also how tests mint tokens).
  - ES256/RS256 → Supabase's current asymmetric keys, verified via the project's
    JWKS endpoint (public keys fetched + cached once).
"""

from uuid import UUID

import jwt                                            # PyJWT — decode/verify tokens
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer     # pulls the "Authorization: Bearer <t>" token
from jwt import PyJWKClient                           # fetches Supabase's public keys (JWKS)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User

# tokenUrl is only metadata for the docs "Authorize" button; we don't issue tokens
# here (Supabase does). Its real job: extract the bearer token and 401 if missing.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Cache the JWKS client across requests — it memoizes the fetched public keys so
# we don't hit Supabase's endpoint on every verify.
_jwks_client: PyJWKClient | None = None


def _jwks() -> PyJWKClient:
    global _jwks_client
    if _jwks_client is None:                          # lazy init on first asymmetric token
        url = settings.SUPABASE_URL.rstrip("/") + "/auth/v1/.well-known/jwks.json"
        _jwks_client = PyJWKClient(url)
    return _jwks_client


def _decode_token(token: str) -> dict:
    # Read the header WITHOUT verifying, just to learn which algorithm signed it.
    alg = jwt.get_unverified_header(token).get("alg", "")
    if alg == "HS256":                                # shared-secret path (tests + legacy + dev-login)
        return jwt.decode(
            token,
            settings.hs256_secret,                    # symmetric secret (dev fallback if unset)
            algorithms=["HS256"],                     # pin the algorithm (never trust the header's)
            options={"verify_aud": False},            # Supabase sets aud="authenticated"; we don't check it
        )
    # Asymmetric path: look up the matching public key by the token's `kid`.
    signing_key = _jwks().get_signing_key_from_jwt(token)
    return jwt.decode(
        token,
        signing_key.key,
        algorithms=["ES256", "RS256"],                # the algorithms Supabase rotates between
        options={"verify_aud": False},
    )


async def get_current_user(
    token: str = Depends(oauth2_scheme),              # 401s automatically if no bearer token
    db: AsyncSession = Depends(get_db),
) -> User:
    try:
        payload = _decode_token(token)                # verifies signature + expiry, or raises
        user_id = payload.get("sub")                  # Supabase puts the user id in `sub`
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        user_uuid = UUID(user_id)                      # also rejects a malformed sub
    except HTTPException:
        raise                                          # keep our own 401s as-is
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except Exception:
        # Bad signature, unknown key, JWKS failure, malformed sub, etc. → always 401,
        # never a 500, so auth failures are uniform and don't leak internals.
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await db.get(User, user_uuid)               # token is valid, but is it a known account?
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user                                        # injected into any route that Depends on it


async def get_current_admin(user: User = Depends(get_current_user)) -> User:
    """Role guard for admin-only routes (e.g. managing resources). 403 if not admin."""
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin role required")
    return user


async def get_current_caseworker(user: User = Depends(get_current_user)) -> User:
    """Role guard for the caseworker/navigator dashboard. 403 for residents."""
    if user.role not in ("caseworker", "navigator", "admin"):
        raise HTTPException(status_code=403, detail="Caseworker or navigator role required")
    return user
