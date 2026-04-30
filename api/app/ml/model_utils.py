import joblib as jb
from pathlib import Path
import numpy as np
import pandas as pd
from app.ml.custom_transformers import OutlierHandler, FeatureEngineer

BASE_DIR = Path(__file__).resolve().parents[3]
MODEL_PATH = BASE_DIR / "models" / "model_package.pkl"

package = None


def load_model():
    global package
    if package is None:
        try:
            package = jb.load(MODEL_PATH)
            version = package['metadata'].get('version', 'unknown')
            print(f"AI Model Package Loaded Successfully (Version: {version})")
        except FileNotFoundError:
            raise Exception(f"Không tìm thấy file mô hình tại {MODEL_PATH}")
    return package


def preprocess_payload(data: dict, features_in: list) -> pd.DataFrame:
    filtered = {col: data[col] for col in features_in if col in data}
    df = pd.DataFrame([filtered])          # shape (1, n_features)
    df = df[features_in]                   # đảm bảo đúng thứ tự cột
    return df


def predict(data: dict):
    pkg = load_model()
    pipeline = pkg['pipeline']
    metadata = pkg['metadata']

    features_in = metadata['features_in']

    X = preprocess_payload(data, features_in)

    prob = pipeline.predict_proba(X)[0][1]

    threshold = metadata.get("optimal_threshold", 0.4)
    pred = 1 if prob >= threshold else 0

    if prob >= 0.8:
        risk = "Nguy cơ Rất Cao"
    elif prob >= threshold:
        risk = "Nguy cơ Cao"
    elif prob >= 0.2:
        risk = "Nguy cơ Trung Bình"
    else:
        risk = "Thấp"

    return {
        "prediction": pred,
        "probability": round(prob, 4),
        "threshold_used": threshold,
        "risk_level": risk
    }


if __name__ == "__main__":
    test_payload = {
        'fullName': 'Phạm Phát', 'idCard': '087205013175',
        'age': 23, 'sex': 'Male', 'cp': 'typical angina',
        'trestbps': 70, 'chol': 120, 'fbs': True, 'restecg': 'normal',
        'thalch': 98, 'exang': True, 'oldpeak': 0, 'slope': 'flat'
    }

    print("Test Payload Input:", test_payload)
    print("\nExecuting prediction flow...")
    result = predict(test_payload)
    print("\nAPI Response:", result)