import joblib as jb
from pathlib import Path
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[3]
MODEL_PATH = BASE_DIR / "models" / "model_package.pkl"

package = None


def load_model():
    global package

    if package is None:
        package = jb.load(MODEL_PATH)

        print("✅ AI Model Loaded")

    return package

SEX_MAP = {"Male": 1, "Female": 0}
CP_MAP = {
    "asymptomatic": 0,
    "atypical angina": 1,
    "non-anginal": 2,
    "typical angina": 3
}
RESTECG_MAP = {"normal": 0, "lv hypertrophy": 1, "st-t abnormality": 2}
SLOPE_MAP = {"flat": 0, "downsloping": 1, "upsloping": 2}
THAL_MAP = {"normal": 1, "fixed defect": 2, "reversable defect": 3}


def preprocess(data):
    df = pd.DataFrame([data])

    if "ca" not in df.columns or pd.isnull(df.at[0, "ca"]):
        df["ca"] = np.nan
    else:
        df["ca"] = float(df.at[0, "ca"])

    numeric_cols = ['age', 'trestbps', 'chol', 'thalch', 'oldpeak']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    if "heart_rate_ratio" not in df.columns:
        df["heart_rate_ratio"] = df["thalch"] / (220 - df["age"])

    if "age_risk_group" not in df.columns:
        df["age_risk_group"] = np.digitize(df["age"], bins=[40, 60])

    expected_columns = [
        'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg',
        'thalch', 'exang', 'oldpeak', 'slope', 'ca', 'thal',
        'heart_rate_ratio', 'age_risk_group'
    ]

    return df[expected_columns]


def predict(data):
    pkg = load_model()

    model = pkg["model"]
    preprocessor = pkg["preprocessor"]

    X = preprocess(data)

    if preprocessor is not None:
        X_transformed = preprocessor.transform(X)
    else:
        X_transformed = X

    pred = int(model.predict(X_transformed)[0])
    prob = float(model.predict_proba(X_transformed)[0][1])

    risk = "Low"

    if prob > 0.65:
        risk = "High"
    elif prob > 0.35:
        risk = "Medium"

    return {
        "prediction": pred,
        "probability": round(prob, 4),
        "risk_level": risk
    }

if __name__ == "__main__":
    package = load_model()
    print(package)