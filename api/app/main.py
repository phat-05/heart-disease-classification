# ============================================================
# app/main.py
# FastAPI chuẩn mới dùng lifespan (thay cho on_event deprecated)
# ============================================================

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import predict
from app.routers import auth as auth_router
from app.database.database import engine, check_db_connection
from app.database import models


# ============================================================
# Tạo bảng DB (idempotent)
# ============================================================
models.Base.metadata.create_all(bind=engine)


# ============================================================
# Lifespan events (startup / shutdown mới)
# ============================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    # ================= STARTUP =================
    print("=" * 55)
    print("[Server] Heart Disease API v2.0 đang khởi động...")

    # Kiểm tra DB
    if check_db_connection():
        print("[DB]     ✔ Kết nối MySQL thành công")
    else:
        print("[DB]     ✘ CẢNH BÁO: Không kết nối được MySQL!")
        print("[DB]       Chạy: python -m app.database.init_db")

    # Kiểm tra model
    try:
        if hasattr(predict, "predictor") and predict.predictor:
            print(f"[Model]  Features: {predict.predictor.feature_cols}")
        else:
            print("[Model]  Predictor chưa load")
    except Exception as e:
        print(f"[Model]  Lỗi load predictor: {e}")

    print("[Server] Swagger : http://localhost:8000/docs")
    print("=" * 55)

    yield

    # ================= SHUTDOWN =================
    print("[Server] Tắt server... Goodbye!")


# ============================================================
# FastAPI App
# ============================================================
app = FastAPI(
    title="Heart Disease Prediction API",
    description="""
## API dự đoán nguy cơ bệnh tim

### Luồng sử dụng:
1. **Đăng ký** `POST /api/auth/register`
2. **Đăng nhập** `POST /api/auth/login`
3. Nhận `access_token`
4. Authorize bằng `Bearer <token>`
5. Gọi `POST /api/predict/`
    """,
    version="2.0.0",
    docs_url="/docs",
    lifespan=lifespan
)


# ============================================================
# Middleware
# ============================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# Routers
# ============================================================
app.include_router(auth_router.router, prefix="/api")
app.include_router(predict.router, prefix="/api")


# ============================================================
# Root endpoint
# ============================================================
@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Heart Disease Prediction API v2.0",
        "status": "running",
        "docs": "http://localhost:8000/docs"
    }