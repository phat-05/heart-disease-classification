# ============================================================
# app/schemas/auth.py
#
# Pydantic schemas cho authentication endpoints.
# ============================================================

from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime


# ------------------------------------------------------------------
# REQUEST SCHEMAS
# ------------------------------------------------------------------
class RegisterRequest(BaseModel):
    username:  str
    email:     EmailStr
    password:  str
    full_name: Optional[str] = None

    @field_validator("username")
    @classmethod
    def username_valid(cls, v):
        if len(v) < 3:
            raise ValueError("Username phải có ít nhất 3 ký tự")
        if not v.isalnum() and "_" not in v:
            raise ValueError("Username chỉ chứa chữ, số và dấu gạch dưới")
        return v

    @field_validator("password")
    @classmethod
    def password_strong(cls, v):
        if len(v) < 6:
            raise ValueError("Password phải có ít nhất 6 ký tự")
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "drsmith",
                "email": "drsmith@hospital.com",
                "password": "secret123",
                "full_name": "Dr. John Smith"
            }
        }
    }


class LoginRequest(BaseModel):
    username: str
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


# ------------------------------------------------------------------
# RESPONSE SCHEMAS
# ------------------------------------------------------------------
class UserResponse(BaseModel):
    id:         int
    username:   str
    email:      str
    full_name:  Optional[str]
    role:       str
    is_active:  bool
    created_at: Optional[datetime]

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token:  str
    refresh_token: str
    token_type:    str = "bearer"
    expires_in:    int = 1800   # 30 phút (seconds)
    user:          UserResponse


class MessageResponse(BaseModel):
    message: str
    success: bool = True
