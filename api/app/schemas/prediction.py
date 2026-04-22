# ============================================================
# app/schemas/prediction.py
#
# Pydantic schemas cho prediction endpoints.
# ============================================================

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime


# ------------------------------------------------------------------
# ENUMS — khớp chính xác với giá trị OneHotEncoder đã fit
# ------------------------------------------------------------------
class SexEnum(str, Enum):
    Male   = "Male"
    Female = "Female"


class ChestPainEnum(str, Enum):
    typical_angina    = "typical angina"
    atypical_angina   = "atypical angina"
    non_anginal_pain  = "non-anginal pain"
    asymptomatic      = "asymptomatic"


class RestECGEnum(str, Enum):
    normal              = "normal"
    st_t_abnormality    = "ST-T wave abnormality"
    left_ventricular    = "left ventricular hypertrophy"


class SlopeEnum(str, Enum):
    upsloping   = "upsloping"
    flat        = "flat"
    downsloping = "downsloping"


class ThalEnum(str, Enum):
    normal         = "normal"
    fixed_defect   = "fixed defect"
    reversable_defect = "reversable defect"


# ------------------------------------------------------------------
# INPUT SCHEMA
# ------------------------------------------------------------------
class HeartDiseaseInput(BaseModel):
    # Thông tin bệnh nhân (optional - nếu có thì lưu vào DB)
    patient_id: Optional[int] = None       # ID bệnh nhân đã có trong DB

    # 13 chỉ số y tế
    age:      int   = Field(..., ge=1, le=120, description="Tuổi bệnh nhân")
    sex:      SexEnum
    cp:       ChestPainEnum
    trestbps: float = Field(..., ge=80,  le=250, description="Huyết áp lúc nghỉ (mmHg)")
    chol:     float = Field(..., ge=100, le=600, description="Cholesterol (mg/dl)")
    fbs:      bool  = Field(..., description="Đường huyết lúc đói > 120 mg/dl")
    restecg:  RestECGEnum
    thalch:   float = Field(..., ge=60,  le=250, description="Nhịp tim tối đa")
    exang:    bool  = Field(..., description="Đau thắt ngực khi gắng sức")
    oldpeak:  float = Field(..., ge=0.0, le=10.0)
    slope:    SlopeEnum
    ca:       Optional[int] = Field(None, ge=0, le=4)
    thal:     ThalEnum

    model_config = {
        "json_schema_extra": {
            "example": {
                "age": 63, "sex": "Male", "cp": "typical angina",
                "trestbps": 145, "chol": 233, "fbs": True,
                "restecg": "normal", "thalch": 150, "exang": False,
                "oldpeak": 2.3, "slope": "downsloping", "ca": 0, "thal": "fixed defect"
            }
        }
    }


# ------------------------------------------------------------------
# OUTPUT SCHEMAS
# ------------------------------------------------------------------
class PredictionResponse(BaseModel):
    prediction:   int
    probability:  float
    risk_level:   str
    prediction_id: Optional[int] = None   # ID lưu trong DB


class PredictionHistoryItem(BaseModel):
    id:          int
    prediction:  int
    probability: float
    risk_level:  str
    age:         int
    sex:         str
    created_at:  Optional[datetime]

    model_config = {"from_attributes": True}


class PatientCreateRequest(BaseModel):
    full_name:     Optional[str] = None
    date_of_birth: Optional[datetime] = None
    gender:        Optional[str] = None
    phone:         Optional[str] = None
    address:       Optional[str] = None
    notes:         Optional[str] = None


class PatientResponse(BaseModel):
    id:           int
    patient_code: Optional[str]
    full_name:    Optional[str]
    gender:       Optional[str]
    phone:        Optional[str]
    created_at:   Optional[datetime]

    model_config = {"from_attributes": True}
