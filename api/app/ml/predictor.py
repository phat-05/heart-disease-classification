# ============================================================
# app/ml/predictor.py
#
# Load model_package.pkl từ models/ và thực hiện predict.
#
# Cấu trúc pkl (đã kiểm tra):
#   {
#     "metadata":    dict  — feature names, metrics, version...
#     "model":       RandomForestClassifier
#     "preprocessor": ColumnTransformer (imputer + scaler/encoder)
#   }
#
# Pipeline predict:
#   FE input (13 fields)
#     → giữ string cho cat / giữ số cho num
#     → tính thêm 2 features (heart_rate_ratio, age_risk_group)
#     → build DataFrame đúng thứ tự features_in (15 cột)
#     → preprocessor.transform()
#     → model.predict_proba()
#     → trả về prediction, probability, risk_level
# ============================================================

import os
import numpy as np
import pandas as pd
import joblib

# ------------------------------------------------------------------
# ĐƯỜNG DẪN ĐẾN MODEL
#
# __file__ = D:/heart-disease-classification/api/app/ml/predictor.py
# Đi lên 4 cấp để về root:
#   predictor.py → ml/ → app/ → api/ → heart-disease-classification/
# ------------------------------------------------------------------
_THIS_FILE = os.path.abspath(__file__)
_ROOT      = os.path.dirname(   # heart-disease-classification/
             os.path.dirname(    # api/
             os.path.dirname(    # app/
             os.path.dirname(    # ml/
             _THIS_FILE))))

MODEL_PATH = os.path.join(_ROOT, "models", "model_package.pkl")


class HeartPredictor:
    """
    Singleton — load model 1 lần khi server start,
    tái sử dụng cho mọi request.
    """

    def __init__(self):
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Không tìm thấy model tại: {MODEL_PATH}\n"
                f"Kiểm tra lại thư mục models/ ở root project."
            )

        package = joblib.load(MODEL_PATH)

        self.model        = package["model"]          # RandomForestClassifier
        self.preprocessor = package["preprocessor"]   # ColumnTransformer
        self.metadata     = package["metadata"]

        # Thứ tự 15 features lấy từ metadata — không hardcode
        self.feature_cols = self.metadata["features_in"]

        print(f"[Predictor] Model loaded: {self.metadata['model_type']} v{self.metadata['version']}")
        print(f"[Predictor] Recall={self.metadata['metrics']['recall']:.3f} | "
              f"F1={self.metadata['metrics']['f1_score']:.3f}")
        print(f"[Predictor] Features ({len(self.feature_cols)}): {self.feature_cols}")

    def _build_dataframe(self, data) -> pd.DataFrame:
        """
        Nhận HeartDiseaseInput → DataFrame 1 hàng, 15 cột đúng thứ tự.

        Tại sao dùng DataFrame?
        - ColumnTransformer được fit với tên cột
        - Nếu dùng numpy array → transformer không biết cột nào num, cột nào cat

        Tại sao tính heart_rate_ratio và age_risk_group ở đây?
        - Đây là engineered features được tạo trong notebook trước khi train
        - Model không tự tính được → ta phải tính trước

        Tại sao fbs/exang dùng str(bool)?
        - FE gửi true/false (bool Python)
        - OneHotEncoder đã được fit trên "True"/"False" (string)
        - Nếu gửi thẳng bool → encoder không nhận ra → lỗi transform

        Tại sao ca=NaN thay vì 0?
        - preprocessor có SimpleImputer(strategy='median') cho numerical
        - NaN → imputer tự điền median của training set → đúng hơn điền 0
        """
        age    = data.age
        thalch = data.thalch

        heart_rate_ratio = thalch / age if age > 0 else 0.0
        age_risk_group   = 1 if age >= 55 else 0

        row = {
            "age":              age,
            "sex":              data.sex.value,
            "cp":               data.cp.value,
            "trestbps":         data.trestbps,
            "chol":             data.chol,
            "fbs":              str(data.fbs),        # bool → "True"/"False"
            "restecg":          data.restecg.value,
            "thalch":           thalch,
            "exang":            str(data.exang),      # bool → "True"/"False"
            "oldpeak":          data.oldpeak,
            "slope":            data.slope.value,
            "ca":               data.ca if data.ca is not None else np.nan,
            "thal":             data.thal.value,
            "heart_rate_ratio": heart_rate_ratio,
            "age_risk_group":   age_risk_group,
        }

        return pd.DataFrame([row], columns=self.feature_cols)

    def predict(self, data) -> dict:
        """
        Full pipeline: FE input → DataFrame → preprocess → predict → result
        """
        df          = self._build_dataframe(data)
        X_processed = self.preprocessor.transform(df)
        proba       = float(self.model.predict_proba(X_processed)[0][1])
        label       = int(self.model.predict(X_processed)[0])

        return {
            "prediction":  label,
            "probability": round(proba, 4),
            "risk_level":  self._get_risk_level(proba),
        }

    @staticmethod
    def _get_risk_level(probability: float) -> str:
        """
        Khớp chính xác với riskStyles keys trong PredictionResult.js:
        "Low" / "Medium" / "High"
        """
        if probability < 0.35:
            return "Low"
        elif probability < 0.65:
            return "Medium"
        else:
            return "High"


# Singleton — khởi tạo 1 lần khi module được import
predictor = HeartPredictor()