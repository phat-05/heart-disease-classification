import os
import pandas as pd
from flask import request, jsonify
from flask_cors import CORS
from app import create_app, db
from app.models import BenhNhan, ThongSoYTe, KetQuaChuanDoan
from app.ml.model_utils import predict
from app.ml.custom_transformers import OutlierHandler, FeatureEngineer

app = create_app()

CORS(app, origins=["http://localhost:3000"])


@app.route("/")
def home():
    return jsonify({"message": "Heart Disease AI API is Running", "status": "Online"})


@app.route("/predict", methods=["POST"])
def du_doan():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Dữ liệu trống"}), 400

        cccd_val = data.get("cccd")
        bn = None
        if cccd_val:
            bn = BenhNhan.query.filter_by(cccd=cccd_val).first()

        if not bn:
            bn = BenhNhan(
                ho_ten=data.get("patientName", "Ẩn danh"),
                tuoi=int(data["age"]),
                gioi_tinh=data["sex"],
                cccd=cccd_val
            )
            db.session.add(bn)
            db.session.flush()

        ts = ThongSoYTe(
            benh_nhan_id=bn.id,
            tuoi=int(data["age"]),
            gioi_tinh=data["sex"],
            cp=data["cp"],
            trestbps=float(data["trestbps"]),
            chol=float(data["chol"]),
            fbs=True if data["fbs"] == "1" else False,
            restecg=data["restecg"],
            thalch=float(data["thalch"]),
            exang=True if data["exang"] == "Y" else False,
            oldpeak=float(data["oldpeak"]),
            slope=data["slope"],
            ca=float(data.get("ca", 0)),
            thal=data.get("thal", "Normal")
        )
        db.session.add(ts)
        db.session.flush()

        result = predict(data)

        if not result:
            return jsonify({"error": "Lỗi trong quá trình AI xử lý"}), 500

        kq = KetQuaChuanDoan(
            thong_so_id=ts.id,
            ket_qua=int(result["prediction"]),
            xac_suat=float(result["probability"]),
            muc_do_rui_ro=result["risk_level"]
        )
        db.session.add(kq)

        db.session.commit()

        return jsonify(result)

    except Exception as e:
        print(f"Lỗi: {str(e)}")
        db.session.rollback()
        return jsonify({"error": "Đã xảy ra lỗi hệ thống", "detail": str(e)}), 500


@app.route("/history", methods=["GET"])
def lay_lich_su():
    try:
        records = db.session.query(KetQuaChuanDoan, ThongSoYTe, BenhNhan) \
            .join(ThongSoYTe, KetQuaChuanDoan.thong_so_id == ThongSoYTe.id) \
            .join(BenhNhan, ThongSoYTe.benh_nhan_id == BenhNhan.id) \
            .order_by(ThongSoYTe.ngay_tao.desc()).all()

        history_data = []
        for kq, ts, bn in records:
            history_data.append({
                "id": kq.id,
                "patientName": bn.ho_ten,
                "cccd": bn.cccd,
                "age": ts.tuoi,
                "sex": ts.gioi_tinh,
                "prediction": kq.ket_qua,
                "risk_level": kq.muc_do_rui_ro,
                "timestamp": ts.ngay_tao.strftime("%d/%m/%Y %H:%M:%S")
            })
        return jsonify(history_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Database & Tables created successfully.")

    print("🚀 Server Heart AI đang chạy tại http://localhost:8000")
    app.run(debug=True, host="0.0.0.0", port=8000)