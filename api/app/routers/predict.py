# ============================================================
# app/routers/predict.py  — THAY THẾ file cũ bằng file này
# ============================================================

import json
import time

from fastapi import APIRouter, HTTPException, status, Depends, Request
from sqlalchemy.orm import Session
from typing import List, Optional

from app.schemas.prediction import (
    HeartDiseaseInput, PredictionResponse,
    PatientCreateRequest, PatientResponse,
    PredictionHistoryItem
)
from app.database.database import get_db
from app.database.models import User, Patient, Prediction, PredictionLog
from app.core.dependencies import get_current_user

# Import singleton predictor
try:
    from app.ml.predictor import predictor
    _PREDICTOR_LOADED = True
except Exception as e:
    print(f"[WARN] Predictor chưa load được: {e}")
    predictor = None
    _PREDICTOR_LOADED = False

router = APIRouter(
    prefix="/predict",
    tags=["Prediction"],
    responses={
        401: {"description": "Chưa đăng nhập"},
        422: {"description": "Dữ liệu đầu vào không hợp lệ"},
        500: {"description": "Lỗi server khi predict"},
    }
)


def _get_or_create_patient(user_id: int, db: Session) -> Patient:
    count = db.query(Patient).filter(Patient.user_id == user_id).count()
    code  = f"BN-{(count + 1):05d}"
    p = Patient(user_id=user_id, patient_code=code, full_name="Bệnh nhân ẩn danh")
    db.add(p)
    db.flush()
    return p


@router.post(
    "/",
    response_model=PredictionResponse,
    status_code=status.HTTP_200_OK,
    summary="Dự đoán nguy cơ bệnh tim (yêu cầu đăng nhập)"
)
async def predict_heart_disease(
    data:         HeartDiseaseInput,
    request:      Request,
    db:           Session = Depends(get_db),
    current_user: User    = Depends(get_current_user),
):
    if not _PREDICTOR_LOADED or predictor is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model chưa được load. Kiểm tra file models/model_package.pkl"
        )

    start_time = time.time()

    try:
        result = predictor.predict(data)

        # Xác định / tạo patient
        if data.patient_id:
            patient = db.query(Patient).filter(
                Patient.id      == data.patient_id,
                Patient.user_id == current_user.id
            ).first()
            if not patient:
                raise HTTPException(status_code=404, detail="Không tìm thấy bệnh nhân")
        else:
            patient = _get_or_create_patient(current_user.id, db)

        age   = data.age
        thalch = data.thalch
        heart_rate_ratio = thalch / age if age > 0 else 0.0
        age_risk_group   = 1 if age >= 55 else 0

        pred_record = Prediction(
            patient_id       = patient.id,
            user_id          = current_user.id,
            age              = data.age,
            sex              = data.sex.value,
            cp               = data.cp.value,
            trestbps         = data.trestbps,
            chol             = data.chol,
            fbs              = data.fbs,
            restecg          = data.restecg.value,
            thalch           = data.thalch,
            exang            = data.exang,
            oldpeak          = data.oldpeak,
            slope            = data.slope.value,
            ca               = data.ca,
            thal             = data.thal.value,
            heart_rate_ratio = heart_rate_ratio,
            age_risk_group   = age_risk_group,
            prediction       = result["prediction"],
            probability      = result["probability"],
            risk_level       = result["risk_level"],
            model_version    = predictor.metadata.get("version", "1.0") if predictor else "1.0",
        )
        db.add(pred_record)
        db.flush()

        processing_ms = (time.time() - start_time) * 1000
        log = PredictionLog(
            prediction_id = pred_record.id,
            user_id       = current_user.id,
            request_body  = json.dumps(data.model_dump(), default=str),
            response_body = json.dumps(result),
            ip_address    = request.client.host if request.client else None,
            user_agent    = request.headers.get("user-agent", "")[:255],
            endpoint      = str(request.url.path),
            http_method   = request.method,
            status_code   = 200,
            processing_ms = processing_ms,
        )
        db.add(log)
        db.commit()

        return {**result, "prediction_id": pred_record.id}

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=422, detail=f"Lỗi xử lý dữ liệu: {str(e)}")
    except Exception as e:
        print(f"[ERROR] Predict failed: {e}")
        raise HTTPException(status_code=500, detail="Lỗi server khi thực hiện dự đoán.")


@router.get("/history", response_model=List[PredictionHistoryItem], summary="Lịch sử dự đoán")
async def get_history(
    limit: int = 20, skip: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(Prediction)
        .filter(Prediction.user_id == current_user.id)
        .order_by(Prediction.created_at.desc())
        .offset(skip).limit(limit).all()
    )


@router.post("/patients", response_model=PatientResponse, status_code=201, summary="Thêm bệnh nhân mới")
async def create_patient(
    data: PatientCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    count = db.query(Patient).filter(Patient.user_id == current_user.id).count()
    patient = Patient(
        user_id       = current_user.id,
        patient_code  = f"BN-{(count + 1):05d}",
        full_name     = data.full_name,
        date_of_birth = data.date_of_birth,
        gender        = data.gender,
        phone         = data.phone,
        address       = data.address,
        notes         = data.notes,
    )
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


@router.get("/patients", response_model=List[PatientResponse], summary="Danh sách bệnh nhân")
async def list_patients(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(Patient).filter(Patient.user_id == current_user.id).order_by(Patient.created_at.desc()).all()


@router.get("/health", summary="Kiểm tra trạng thái model", tags=["Health"])
async def model_health():
    if not _PREDICTOR_LOADED or predictor is None:
        return {"status": "model_not_loaded", "message": "Thiếu file models/model_package.pkl"}
    return {
        "status":        "ok",
        "model_loaded":  True,
        "feature_count": len(predictor.feature_cols),
        "features":      predictor.feature_cols,
    }
