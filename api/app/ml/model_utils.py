import joblib as jb
from pathlib import Path
import numpy as np
import pandas as pd
from app.ml.custom_transformers import OutlierHandler, FeatureEngineer

BASE_DIR = Path(__file__).resolve().parents[3]
MODEL_PATH = BASE_DIR / "models" / "model_package.pkl"

# Singleton pattern để lưu package vào bộ nhớ, tránh load lại nhiều lần
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


def preprocess_payload(data: dict, features_in: list):
    """
    Tiền xử lý payload từ Frontend:
    1. Tạo DataFrame.
    2. Kích hoạt Feature Engineering (heart_rate_ratio, age_risk_group).
    3. Lọc bỏ các cột rác (fullName, idCard) để khớp với input của Pipeline.
    """
    df = pd.DataFrame([data])

    # Xử lý các cột missing mặc định (nếu Frontend quên gửi)
    if "ca" not in df.columns or pd.isnull(df.at[0, "ca"]):
        df["ca"] = np.nan
    else:
        df["ca"] = float(df.at[0, "ca"])

    # Tính toán các Feature Engineering mới (Trụ cột Học thuật)
    if "heart_rate_ratio" not in df.columns:
        df["heart_rate_ratio"] = df["thalch"] / (220 - df["age"])

    if "age_risk_group" not in df.columns:
        # np.digitize trả về mảng, lưu ý ép về chuỗi nếu lúc train biến này là dạng Categorical
        df["age_risk_group"] = str(np.digitize(df["age"], bins=[40, 60]))

    # CỰC KỲ QUAN TRỌNG (Trụ cột Thực tế):
    # Lọc DataFrame để CHỈ giữ lại các cột mà mô hình yêu cầu lúc huấn luyện.
    # Thao tác này sẽ tự động vứt bỏ 'fullName', 'idCard' giúp bảo mật dữ liệu.
    try:
        df_filtered = df[features_in]
        return df_filtered
    except KeyError as e:
        missing_cols = set(features_in) - set(df.columns)
        raise ValueError(f"Thiếu các trường dữ liệu quan trọng từ Frontend: {missing_cols}")


def predict(data: dict):
    pkg = load_model()

    # Chỉ giải nén Pipeline nguyên khối và Metadata
    full_pipeline = pkg["pipeline"]
    metadata = pkg["metadata"]

    # 1. Lấy dữ liệu đã lọc và gắn Feature
    X_input = preprocess_payload(data, metadata["features_in"])

    # 2. Đưa qua Full Pipeline (Tự động điền khuyết, chuẩn hóa, mã hóa và dự đoán)
    # Tuyệt đối không gọi .transform()
    prob = float(full_pipeline.predict_proba(X_input)[0][1])

    # 3. Kéo Threshold đã chốt ở Tuần 4-6 ra sử dụng
    threshold = metadata.get("optimal_threshold", 0.4)

    # 4. Quyết định kết quả
    pred = 1 if prob >= threshold else 0

    # Phân loại mức độ rủi ro dựa trên Threshold gốc
    if prob >= 0.8:
        risk = "Nguy cơ Rất Cao (Cần cấp cứu/can thiệp ngay)"
    elif prob >= threshold:
        risk = "Nguy cơ Cao (Cần xét nghiệm chuyên sâu)"
    elif prob >= 0.2:
        risk = "Nguy cơ Trung Bình (Cần theo dõi lối sống)"
    else:
        risk = "Thấp (Khỏe mạnh)"

    return {
        "prediction": pred,
        "probability": round(prob, 4),
        "threshold_used": threshold,
        "risk_level": risk
    }


if __name__ == "__main__":
    # Test thử với payload bạn vừa gửi
    test_payload = {
        'fullName': 'Phạm Phát', 'idCard': '087205013175',
        'age': 23, 'sex': 'Male', 'cp': 'typical angina',
        'trestbps': 70, 'chol': 120, 'fbs': True, 'restecg': 'normal',
        'thalch': 98, 'exang': True, 'oldpeak': 0, 'slope': 'flat',
        'ca': None, 'thal': 'normal'
    }

    # Fake load_model để test nếu bạn chạy file này độc lập mà chưa có mô hình
    # Hãy bỏ comment các dòng này khi chạy thực tế
    print("Test Payload Input:", test_payload)
    print("\nExecuting prediction flow...")
    result = predict(test_payload)
    print("\nAPI Response:", result)