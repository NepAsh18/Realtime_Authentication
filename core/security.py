from jose import jwt, JWTError
from datetime import datetime, timedelta
import uuid
from fastapi import HTTPException, status

from core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from services.session_store import (
    add_session,
    cleanup_expired_tokens,
    active_sessions
)


def create_access_token(user_id: str):
    token_id = str(uuid.uuid4())
    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": user_id,
        "jti": token_id,
        "exp": expire
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    add_session(token_id, user_id, expire)

    return token


def verify_token(token: str):
    cleanup_expired_tokens()

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_id = payload.get("jti")
        user_id = payload.get("sub")

        if token_id not in active_sessions:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token revoked or expired"
            )

        return user_id

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
