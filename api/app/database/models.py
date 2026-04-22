# ============================================================
# app/database/models.py
#
# Định nghĩa tất cả bảng trong heart_disease_db.
#
# Schema:
#   users          — tài khoản đăng nhập
#   patients       — thông tin bệnh nhân (1 user có nhiều bệnh nhân)
#   predictions    — kết quả dự đoán (1 bệnh nhân nhiều lần dự đoán)
#   prediction_logs — log chi tiết mỗi lần gọi API (audit trail)
#   refresh_tokens — quản lý JWT refresh token
#
# Quan hệ:
#   users 1—N patients
#   patients 1—N predictions
#   predictions 1—1 prediction_logs
# ============================================================

from sqlalchemy import (
    Column, Integer, String, Float, Boolean,
    DateTime, Text, ForeignKey, Enum, Index
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.database.database import Base


# ------------------------------------------------------------------
# ENUM TYPES
# ------------------------------------------------------------------
class RiskLevel(str, enum.Enum):
    Low    = "Low"
    Medium = "Medium"
    High   = "High"


class UserRole(str, enum.Enum):
    admin  = "admin"
    doctor = "doctor"
    user   = "user"


# ------------------------------------------------------------------
# TABLE: users
# Lưu tài khoản đăng nhập của hệ thống
# ------------------------------------------------------------------
class User(Base):
    __tablename__ = "users"

    id           = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username     = Column(String(50),  unique=True, nullable=False, index=True)
    email        = Column(String(100), unique=True, nullable=False, index=True)
    full_name    = Column(String(100), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    role         = Column(Enum(UserRole), default=UserRole.user, nullable=False)
    is_active    = Column(Boolean, default=True, nullable=False)
    is_verified  = Column(Boolean, default=False, nullable=False)
    created_at   = Column(DateTime(timezone=True), server_default=func.now())
    updated_at   = Column(DateTime(timezone=True), onupdate=func.now())
    last_login   = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    patients       = relationship("Patient",      back_populates="user", cascade="all, delete-orphan")
    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User id={self.id} username={self.username}>"


# ------------------------------------------------------------------
# TABLE: patients
# Thông tin cá nhân của bệnh nhân được nhập vào form
# Một user (bác sĩ) có thể quản lý nhiều bệnh nhân
# ------------------------------------------------------------------
class Patient(Base):
    __tablename__ = "patients"

    id          = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id     = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Thông tin định danh bệnh nhân
    patient_code = Column(String(20),  unique=True, nullable=True)   # Mã BN: BN-00001
    full_name    = Column(String(100), nullable=True)
    date_of_birth = Column(DateTime,  nullable=True)
    gender       = Column(String(10),  nullable=True)                 # male/female/other
    phone        = Column(String(20),  nullable=True)
    address      = Column(Text,        nullable=True)
    notes        = Column(Text,        nullable=True)

    created_at  = Column(DateTime(timezone=True), server_default=func.now())
    updated_at  = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user        = relationship("User",       back_populates="patients")
    predictions = relationship("Prediction", back_populates="patient", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_patient_user_id", "user_id"),
    )

    def __repr__(self):
        return f"<Patient id={self.id} code={self.patient_code}>"


# ------------------------------------------------------------------
# TABLE: predictions
# Kết quả mỗi lần chạy dự đoán cho bệnh nhân
# Lưu đủ 15 features đầu vào + kết quả đầu ra
# ------------------------------------------------------------------
class Prediction(Base):
    __tablename__ = "predictions"

    id          = Column(Integer, primary_key=True, index=True, autoincrement=True)
    patient_id  = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id     = Column(Integer, ForeignKey("users.id",    ondelete="SET NULL"), nullable=True,  index=True)

    # ---- 13 features gốc từ form ----
    age         = Column(Integer,  nullable=False)
    sex         = Column(String(10), nullable=False)      # Male/Female
    cp          = Column(String(30), nullable=False)      # chest pain type
    trestbps    = Column(Float,    nullable=True)         # resting blood pressure
    chol        = Column(Float,    nullable=True)         # serum cholesterol
    fbs         = Column(Boolean,  nullable=True)         # fasting blood sugar > 120
    restecg     = Column(String(30), nullable=True)       # resting ECG results
    thalch      = Column(Float,    nullable=False)        # max heart rate
    exang       = Column(Boolean,  nullable=True)         # exercise induced angina
    oldpeak     = Column(Float,    nullable=True)
    slope       = Column(String(20), nullable=True)
    ca          = Column(Integer,  nullable=True)         # vessels colored by fluoroscopy
    thal        = Column(String(20), nullable=True)

    # ---- 2 engineered features ----
    heart_rate_ratio = Column(Float, nullable=True)
    age_risk_group   = Column(Integer, nullable=True)

    # ---- Kết quả dự đoán ----
    prediction   = Column(Integer,  nullable=False)       # 0 hoặc 1
    probability  = Column(Float,    nullable=False)       # 0.0 - 1.0
    risk_level   = Column(Enum(RiskLevel), nullable=False)

    # ---- Metadata ----
    model_version = Column(String(20), nullable=True)
    created_at    = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    patient = relationship("Patient", back_populates="predictions")
    user    = relationship("User")
    log     = relationship("PredictionLog", back_populates="prediction", uselist=False)

    __table_args__ = (
        Index("idx_pred_patient_id", "patient_id"),
        Index("idx_pred_created_at", "created_at"),
        Index("idx_pred_risk_level", "risk_level"),
    )

    def __repr__(self):
        return f"<Prediction id={self.id} risk={self.risk_level} prob={self.probability}>"


# ------------------------------------------------------------------
# TABLE: prediction_logs
# Audit trail — log đầy đủ mỗi request/response API
# Dùng cho: debugging, monitoring, analytics
# ------------------------------------------------------------------
class PredictionLog(Base):
    __tablename__ = "prediction_logs"

    id             = Column(Integer, primary_key=True, index=True, autoincrement=True)
    prediction_id  = Column(Integer, ForeignKey("predictions.id", ondelete="CASCADE"), nullable=True, index=True)
    user_id        = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    # Request/Response raw data
    request_body   = Column(Text,    nullable=True)   # JSON string của input
    response_body  = Column(Text,    nullable=True)   # JSON string của output

    # Thông tin request
    ip_address     = Column(String(45),  nullable=True)   # IPv4 hoặc IPv6
    user_agent     = Column(String(255), nullable=True)
    endpoint       = Column(String(100), nullable=True)
    http_method    = Column(String(10),  nullable=True)

    # Trạng thái
    status_code    = Column(Integer, nullable=True)
    error_message  = Column(Text,    nullable=True)
    processing_ms  = Column(Float,   nullable=True)   # Thời gian xử lý (milliseconds)

    created_at     = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    prediction = relationship("Prediction", back_populates="log")

    __table_args__ = (
        Index("idx_log_created_at", "created_at"),
        Index("idx_log_user_id",    "user_id"),
    )


# ------------------------------------------------------------------
# TABLE: refresh_tokens
# Quản lý JWT refresh tokens (blacklist khi logout)
# ------------------------------------------------------------------
class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id         = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id    = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    token      = Column(String(512), unique=True, nullable=False)
    is_revoked = Column(Boolean, default=False, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="refresh_tokens")

    __table_args__ = (
        Index("idx_rt_token",   "token"),
        Index("idx_rt_user_id", "user_id"),
    )
