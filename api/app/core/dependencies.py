# ============================================================
# app/core/dependencies.py
#
# FastAPI dependencies dùng trong các router cần authentication.
# ============================================================

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import User
from app.core.security import decode_token

# OAuth2PasswordBearer tự động đọc header "Authorization: Bearer <token>"
# tokenUrl: URL để lấy token (dùng trong Swagger UI)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency: xác thực JWT và trả về user hiện tại.
    Dùng: @router.get("/protected", dependencies=[Depends(get_current_user)])
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token không hợp lệ hoặc đã hết hạn",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_token(token)
    if payload is None:
        raise credentials_exception

    # Kiểm tra đúng loại token
    if payload.get("type") != "access":
        raise credentials_exception

    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tài khoản đã bị vô hiệu hóa"
        )

    return user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Dependency: chỉ cho phép user đang active."""
    return current_user


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """Dependency: chỉ cho phép admin."""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ admin mới có quyền thực hiện hành động này"
        )
    return current_user
