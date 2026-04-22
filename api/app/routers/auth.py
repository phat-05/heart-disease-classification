# ============================================================
# app/routers/auth.py
# ============================================================

from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import User, RefreshToken
from app.database.dao import (
    get_user_by_username,
    get_user_by_email,
    save_refresh_token,
    get_valid_refresh_token,
    revoke_refresh_token,
    get_user_by_id
)

from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    RefreshTokenRequest,
    TokenResponse,
    UserResponse,
    MessageResponse
)

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
    get_token_expiry_datetime
)

from app.core.dependencies import get_current_user


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# ============================================================
# REGISTER
# ============================================================

@router.post(
    "/register",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED
)
async def register(data: RegisterRequest, db: Session = Depends(get_db)):
    if get_user_by_username(db, data.username):
        raise HTTPException(409, "Username đã tồn tại")

    if get_user_by_email(db, data.email):
        raise HTTPException(409, "Email đã tồn tại")

    user = User(
        username=data.username,
        email=data.email,
        full_name=data.full_name,
        hashed_password=hash_password(data.password),
        is_active=True,
        is_verified=True
    )

    db.add(user)
    db.commit()

    return {
        "message": "Đăng ký thành công",
        "success": True
    }


# ============================================================
# LOGIN
# ============================================================

@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = get_user_by_username(db, data.username)

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(401, "Sai tài khoản hoặc mật khẩu")

    if not user.is_active:
        raise HTTPException(403, "Tài khoản bị khóa")

    token_data = {
        "sub": user.username,
        "user_id": user.id,
        "role": user.role.value
    }

    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    rt = RefreshToken(
        user_id=user.id,
        token=refresh_token,
        expires_at=get_token_expiry_datetime()
    )

    save_refresh_token(db, rt)

    user.last_login = datetime.now(timezone.utc)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": 1800,
        "user": user
    }


# ============================================================
# REFRESH TOKEN
# ============================================================

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(data: RefreshTokenRequest, db: Session = Depends(get_db)):
    payload = decode_token(data.refresh_token)

    if not payload:
        raise HTTPException(401, "Token không hợp lệ")

    db_token = get_valid_refresh_token(db, data.refresh_token)

    if not db_token:
        raise HTTPException(401, "Refresh token đã hết hạn")

    user = get_user_by_id(db, payload["user_id"])

    token_data = {
        "sub": user.username,
        "user_id": user.id,
        "role": user.role.value
    }

    access_token = create_access_token(token_data)
    new_refresh = create_refresh_token(token_data)

    revoke_refresh_token(db, data.refresh_token)

    rt = RefreshToken(
        user_id=user.id,
        token=new_refresh,
        expires_at=get_token_expiry_datetime()
    )

    save_refresh_token(db, rt)

    return {
        "access_token": access_token,
        "refresh_token": new_refresh,
        "token_type": "bearer",
        "expires_in": 1800,
        "user": user
    }


# ============================================================
# LOGOUT
# ============================================================

@router.post("/logout", response_model=MessageResponse)
async def logout(
    data: RefreshTokenRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    revoke_refresh_token(db, data.refresh_token)

    return {
        "message": "Đăng xuất thành công",
        "success": True
    }


# ============================================================
# CURRENT USER
# ============================================================

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user