from flask import request, jsonify
from app import create_app, db
from app.models import BenhNhan, ThongSoYTe, KetQuaChuanDoan
from app.ml.model_utils import predict
from app.ml.custom_transformers import OutlierHandler, FeatureEngineer

app = create_app()


@app.route("/")
def home():
    return jsonify({"message": "Heart Disease API Running"})


@app.route("/predict", methods=["POST"])
def du_doan():
    try:
        data = request.json

        print(data)

        bn = BenhNhan(
            ho_ten=data.get("fullName", "Ẩn danh"),
            tuoi=data["age"],
            gioi_tinh=data["sex"]
        )

        print('OK')

        db.session.add(bn)
        db.session.flush()

        print('OK')

        ts = ThongSoYTe(
            benh_nhan_id=bn.id,
            tuoi=data["age"],
            gioi_tinh=data["sex"],
            cp=data["cp"],
            trestbps=data["trestbps"],
            chol=data["chol"],
            fbs=data["fbs"],
            restecg=data["restecg"],
            thalch=data["thalch"],
            exang=data["exang"],
            oldpeak=data["oldpeak"],
            slope=data["slope"],
            ca=data.get("ca"),
            thal=data["thal"]
        )

        db.session.add(ts)
        db.session.flush()

        result = predict(data)

        if result: 
            print(result)
        else:
            print("error")

        kq = KetQuaChuanDoan(
            thong_so_id=ts.id,
            ket_qua=result["prediction"],
            xac_suat=result["probability"],
            muc_do_rui_ro=result["risk_level"]
        )

        db.session.add(kq)
        db.session.commit()

        return jsonify(result)

    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route("/benh-nhan")
def benh_nhan():
    ds = BenhNhan.query.all()

    return jsonify([
        {
            "id": x.id,
            "ho_ten": x.ho_ten,
            "tuoi": x.tuoi,
            "gioi_tinh": x.gioi_tinh
        }
        for x in ds
    ])


@app.route("/lich-su")
def lich_su():
    ds = KetQuaChuanDoan.query.all()

    return jsonify([
        {
            "ket_qua": x.ket_qua,
            "xac_suat": x.xac_suat,
            "muc_do": x.muc_do_rui_ro
        }
        for x in ds
    ])


@app.route("/thong-ke")
def thong_ke():
    tong = BenhNhan.query.count()
    duong = KetQuaChuanDoan.query.filter_by(ket_qua=1).count()
    am = KetQuaChuanDoan.query.filter_by(ket_qua=0).count()

    return jsonify({
        "tong": tong,
        "duong_tinh": duong,
        "am_tinh": am
    })


if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()

    print("🚀 Server chạy tại http://localhost:8000")
    app.run(debug=True, host="0.0.0.0", port=8000)