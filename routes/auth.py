from fastapi import APIRouter, Header, HTTPException, status
from core.security import create_access_token, verify_token
from services.session_store import revoke_session

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


# ---------------- LOGIN ----------------
@auth_router.post("/login")
def login():
    """
    Fake login for learning.
    Replace with real authentication later.
    """
    user_id = "user123"
    token = create_access_token(user_id)
    return {"access_token": token, "token_type": "bearer"}


# ---------------- PROTECTED ----------------
@auth_router.get("/protected")
def protected(authorization: str = Header(...)):
    """
    Access protected resource using JWT.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header"
        )

    token = authorization.split(" ")[1]
    user_id, _ = verify_token(token)

    return {"message": f"Hello {user_id}"}


# ---------------- LOGOUT ----------------
@auth_router.post("/logout")
def logout(authorization: str = Header(...)):
    """
    Revoke JWT token (real logout).
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header"
        )

    token = authorization.split(" ")[1]
    _, token_id = verify_token(token)
    revoke_session(token_id)

    return {"message": "Logged out successfully"}
