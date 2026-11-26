
import os
from uuid import UUID

import jwt
from jwt import PyJWKClient
from jwt.exceptions import InvalidTokenError, PyJWKClientError

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


bearer_scheme = HTTPBearer()

def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> UUID:
    supabase_url = os.environ["SUPABASE_URL"].rstrip("/")
                                                                                                                          
    jwks_url = f"{supabase_url}/auth/v1/.well-known/jwks.json"
    issuer = f"{supabase_url}/auth/v1"

    jwks_client = PyJWKClient(jwks_url)

    try:
        signing_key = jwks_client.get_signing_key_from_jwt(
            credentials.credentials
        )

        payload = jwt.decode(
            credentials.credentials,
            signing_key.key,
            algorithms=["ES256", "RS256"],
            audience="authenticated",
            issuer=issuer,
            options={"require": ["exp", "iat", "sub"]},
        )

        return UUID(payload["sub"])

    except (InvalidTokenError, PyJWKClientError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
