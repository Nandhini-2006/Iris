from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pwdlib import PasswordHash

from security.authentication.jwt_handler import (
    create_access_token,
    verify_token
)

router = APIRouter()

password_hash = PasswordHash.recommended()

fake_users_db = {
    "admin": {
        "username": "admin",
        "password": password_hash.hash("admin123"),
        "role": "admin"
    }
}

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = fake_users_db.get(form_data.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    if not password_hash.verify(
        form_data.password,
        user["password"]
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    token = create_access_token({
        "sub": user["username"],
        "role": user["role"]
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }


async def get_current_user(
    token: str = Depends(oauth2_scheme)
):
    payload = verify_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    return {
        "username": payload.get("sub"),
        "role": payload.get("role")
    }


@router.get("/me")
async def get_me(
    current_user=Depends(get_current_user)
):
    return current_user