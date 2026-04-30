from datetime import datetime
from app import db

class BenhNhan(db.Model):
    __tablename__ = "benh_nhan"

    id = db.Column(db.Integer, primary_key=True)
    ho_ten = db.Column(db.String(100))
    tuoi = db.Column(db.Integer)
    gioi_tinh = db.Column(db.String(20))
    cccd = db.Column(db.String(12))

    lich_su_kham = db.relationship("ThongSoYTe", backref="benh_nhan", lazy=True)

class ThongSoYTe(db.Model):
    __tablename__ = "thong_so_y_te"

    id = db.Column(db.Integer, primary_key=True)
    benh_nhan_id = db.Column(db.Integer, db.ForeignKey("benh_nhan.id"))

    tuoi = db.Column(db.Integer)
    gioi_tinh = db.Column(db.String(20))
    cp = db.Column(db.String(50))
    trestbps = db.Column(db.Float)
    chol = db.Column(db.Float)
    fbs = db.Column(db.Boolean)
    restecg = db.Column(db.String(30))
    thalch = db.Column(db.Float)
    exang = db.Column(db.Boolean)
    oldpeak = db.Column(db.Float)
    slope = db.Column(db.String(30))
    ca = db.Column(db.Float)
    thal = db.Column(db.String(30))
    ngay_tao = db.Column(db.DateTime, default=datetime.utcnow)

    ket_qua_chuan_doan = db.relationship("KetQuaChuanDoan", backref="thong_so", uselist=False)

class KetQuaChuanDoan(db.Model):
    __tablename__ = "ket_qua_chuan_doan"

    id = db.Column(db.Integer, primary_key=True)
    thong_so_id = db.Column(db.Integer, db.ForeignKey("thong_so_y_te.id"), unique=True)

    ket_qua = db.Column(db.Integer)
    xac_suat = db.Column(db.Float)
    muc_do_rui_ro = db.Column(db.String(100))