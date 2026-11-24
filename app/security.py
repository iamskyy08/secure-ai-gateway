from dataclasses import dataclass
from functools import lru_cache
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
from jwt import PyJWKClient
from app.config import settings

bearer = HTTPBearer(auto_error=False)

@dataclass(frozen=True)
class Principal:
    subject: str
    scopes: frozenset[str]
    issuer: str
    audience: str

@lru_cache(maxsize=1)
def _jwks_client() -> PyJWKClient:
    if not settings.oidc_jwks_url:
        raise RuntimeError("OIDC_JWKS_URL is not configured")
    return PyJWKClient(settings.oidc_jwks_url, cache_keys=True)

async def current_principal(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
) -> Principal:
    if not credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Bearer token required")
    if not settings.oidc_issuer or not settings.oidc_jwks_url:
        raise HTTPException(status_code=503, detail="Identity provider is not configured")
    try:
        key = _jwks_client().get_signing_key_from_jwt(credentials.credentials).key
        claims = jwt.decode(
            credentials.credentials, key, algorithms=["RS256", "ES256"],
            issuer=settings.oidc_issuer, audience=settings.oidc_audience,
            options={"require": ["exp", "iat", "iss", "sub", "aud"]},
        )
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired access token") from None
    raw_scopes = claims.get("scope", "")
    scopes = frozenset(raw_scopes.split()) if isinstance(raw_scopes, str) else frozenset()
    return Principal(str(claims["sub"]), scopes, str(claims["iss"]), str(claims["aud"]))

def require_scope(required: str):
    async def checker(principal: Principal = Depends(current_principal)) -> Principal:
        if required not in principal.scopes:
            raise HTTPException(status_code=403, detail="Insufficient permission")
        return principal
    return checker
