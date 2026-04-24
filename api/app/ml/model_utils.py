import pickle
import os
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_PATH = os.path.join(BASE_DIR, "models", "model_package.pkl")

package = None


def load_model():
    global package

    if package is None:
        with open(MODEL_PATH, "rb") as f:
            package = pickle.load(f)

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
    x = [[
        int(data["age"]),
        SEX_MAP[data["sex"]],
        CP_MAP[data["cp"]],
        float(data["trestbps"]),
        float(data["chol"]),
        int(data["fbs"]),
        RESTECG_MAP[data["restecg"]],
        float(data["thalch"]),
        int(data["exang"]),
        float(data["oldpeak"]),
        SLOPE_MAP[data["slope"]],
        float(data["ca"]),
        THAL_MAP[data["thal"]],
    ]]

    return np.array(x)


def predict(data):
    pkg = load_model()

    model = pkg["model"]
    scaler = pkg["scaler"]

    X = preprocess(data)

    if scaler:
        X = scaler.transform(X)

    pred = int(model.predict(X)[0])
    prob = float(model.predict_proba(X)[0][1])

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