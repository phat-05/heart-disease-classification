# ============================================================
# run.py — đặt ở: heart-disease-classification/api/run.py
#
# Script khởi động server.
# Đảm bảo Python path đúng dù chạy từ thư mục nào.
# ============================================================

import sys
import os

# Thêm thư mục hiện tại (api/) vào Python path
# → "from app.xxx import ..." sẽ luôn hoạt động
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host   = "0.0.0.0",
        port   = 8000,
        reload = True,    # Tắt reload=False khi deploy production
    )