# ============================================================
# app/core/security.py
#
# Xử lý mã hóa password và JWT token.
# ============================================================

from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

# ------------------------------------------------------------------
# CẤU HÌNH JWT
#
# SECRET_KEY: dùng để ký token — PHẢI đổi khi deploy production
# ALGORITHM: HS256 = HMAC + SHA-256 (phổ biến nhất)
# ACCESS_TOKEN_EXPIRE_MINUTES: access token hết hạn sau 30 phút
# REFRESH_TOKEN_EXPIRE_DAYS: refresh token hết hạn sau 7 ngày
# ------------------------------------------------------------------
SECRET_KEY                    = "heart-disease-secret-key-change-in-production-2024"
ALGORITHM                     = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES   = 30
REFRESH_TOKEN_EXPIRE_DAYS     = 7

# passlib context — dùng bcrypt để hash password
# bcrypt tự động thêm salt và tốn thời gian để chống brute-force
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ------------------------------------------------------------------
# PASSWORD UTILITIES
# ------------------------------------------------------------------
def hash_password(password: str) -> str:
    """Hash password bằng bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """So sánh plain password với hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


# ------------------------------------------------------------------
# JWT UTILITIES
# ------------------------------------------------------------------
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Tạo JWT access token.
    data nên chứa: {"sub": username, "user_id": id, "role": role}
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict) -> str:
    """
    Tạo JWT refresh token — thời hạn dài hơn access token.
    Dùng để cấp access token mới mà không cần login lại.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> Optional[dict]:
    """
    Decode và verify JWT token.
    Trả về payload dict nếu hợp lệ, None nếu lỗi.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def get_token_expiry_datetime(days: int = REFRESH_TOKEN_EXPIRE_DAYS):
    """Trả về datetime hết hạn cho refresh token."""
    return datetime.now(timezone.utc) + timedelta(days=days)
