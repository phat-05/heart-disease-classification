# ============================================================
# app/database/dao.py
# Tầng truy cập dữ liệu (DAO)
# ============================================================

from sqlalchemy.orm import Session
from app.database.models import User, Patient, Prediction, PredictionLog, RefreshToken


# ============================================================
# USER
# ============================================================

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, user: User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# ============================================================
# REFRESH TOKEN
# ============================================================

def save_refresh_token(db: Session, token_obj):
    db.add(token_obj)
    db.commit()
    db.refresh(token_obj)
    return token_obj


def get_valid_refresh_token(db: Session, token: str):
    return db.query(RefreshToken).filter(
        RefreshToken.token == token,
        RefreshToken.is_revoked == False
    ).first()


def revoke_refresh_token(db: Session, token: str):
    obj = db.query(RefreshToken).filter(
        RefreshToken.token == token
    ).first()

    if obj:
        obj.is_revoked = True
        db.commit()


# ============================================================
# PATIENT
# ============================================================

def count_patients_by_user(db: Session, user_id: int):
    return db.query(Patient).filter(
        Patient.user_id == user_id
    ).count()


def create_patient(db: Session, patient: Patient):
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


def create_temp_patient(db: Session, user_id: int):
    count = count_patients_by_user(db, user_id)

    patient = Patient(
        user_id=user_id,
        patient_code=f"BN-{(count + 1):05d}",
        full_name="Bệnh nhân ẩn danh"
    )

    db.add(patient)
    db.flush()
    return patient


def get_patient_by_id(db: Session, patient_id: int, user_id: int):
    return db.query(Patient).filter(
        Patient.id == patient_id,
        Patient.user_id == user_id
    ).first()


def get_patients_by_user(db: Session, user_id: int):
    return db.query(Patient).filter(
        Patient.user_id == user_id
    ).order_by(Patient.created_at.desc()).all()


# ============================================================
# PREDICTION
# ============================================================

def create_prediction(db: Session, pred):
    db.add(pred)
    db.flush()
    return pred


def get_prediction_history(db: Session, user_id: int, skip=0, limit=20):
    return db.query(Prediction).filter(
        Prediction.user_id == user_id
    ).order_by(
        Prediction.created_at.desc()
    ).offset(skip).limit(limit).all()


def create_prediction_log(db: Session, log):
    db.add(log)
    db.commit()