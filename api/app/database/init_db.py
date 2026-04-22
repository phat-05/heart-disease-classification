# ============================================================
# app/database/init_db.py
#
# Script tạo database + tất cả bảng trong MySQL.
#
# Chạy 1 lần trước khi start server:
#   cd heart-disease-classification/api
#   python -m app.database.init_db
#
# Hoặc chạy trực tiếp:
#   python app/database/init_db.py
# ============================================================

import sys
import os

# Đảm bảo import đúng khi chạy trực tiếp
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pymysql
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker

# ── Cấu hình kết nối ──────────────────────────────────────────
MYSQL_USER     = "root"
MYSQL_PASSWORD = "123456"
MYSQL_HOST     = "localhost"
MYSQL_PORT     = 3306
MYSQL_DATABASE = "heart_disease_db"


# ==============================================================
# BƯỚC 1: Tạo database nếu chưa có
# Kết nối không có database trước, rồi CREATE DATABASE
# ==============================================================
def create_database_if_not_exists():
    print("\n[1/3] Kiểm tra / tạo database...")

    conn = pymysql.connect(
        host     = MYSQL_HOST,
        port     = MYSQL_PORT,
        user     = MYSQL_USER,
        password = MYSQL_PASSWORD,
        charset  = "utf8mb4",
    )
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS `{MYSQL_DATABASE}` "
                f"CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
            )
            conn.commit()
        print(f"    ✔ Database '{MYSQL_DATABASE}' đã sẵn sàng.")
    finally:
        conn.close()


# ==============================================================
# BƯỚC 2: Kết nối SQLAlchemy và tạo bảng qua ORM
# ==============================================================
def create_tables():
    print("\n[2/3] Tạo bảng qua SQLAlchemy ORM...")

    DATABASE_URL = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}"
        f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
        f"?charset=utf8mb4"
    )

    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping = True,
        echo          = False,   # Bật True để xem SQL được sinh ra
    )

    # Import Base + tất cả Models (phải import để Base.metadata biết về chúng)
    from app.database.database import Base
    import app.database.models  # noqa: F401 — chỉ cần import để register models

    # create_all: tạo bảng chưa có, BỎ QUA bảng đã tồn tại (an toàn)
    Base.metadata.create_all(bind=engine)

    # Liệt kê bảng đã tạo
    inspector = inspect(engine)
    tables    = inspector.get_table_names()
    print(f"    ✔ Tạo xong. Các bảng trong '{MYSQL_DATABASE}':")
    for t in sorted(tables):
        cols = [c["name"] for c in inspector.get_columns(t)]
        print(f"       • {t:<25} ({len(cols)} cột)")

    return engine


# ==============================================================
# BƯỚC 3: Seed dữ liệu mặc định (admin account)
# ==============================================================
def seed_admin(engine):
    print("\n[3/3] Kiểm tra / tạo tài khoản admin mặc định...")

    from sqlalchemy.orm import sessionmaker
    from app.database.models import User, UserRole
    from app.core.security import hash_password

    Session = sessionmaker(bind=engine)
    db      = Session()

    try:
        existing = db.query(User).filter(User.username == "admin").first()
        if existing:
            print("    ✔ Tài khoản admin đã tồn tại — bỏ qua.")
        else:
            admin = User(
                username        = "admin",
                email           = "admin@heartdisease.local",
                full_name       = "System Administrator",
                hashed_password = hash_password("admin123"),
                role            = UserRole.admin,
                is_active       = True,
                is_verified     = True,
            )
            db.add(admin)
            db.commit()
            print("    ✔ Tạo admin: username=admin | password=admin123")
            print("    ⚠  Đổi password admin sau khi deploy production!")
    finally:
        db.close()


# ==============================================================
# KIỂM TRA KẾT NỐI (hàm riêng — dùng để test)
# ==============================================================
def test_connection():
    """Kiểm tra kết nối MySQL thuần — không cần ORM."""
    print("\n── Kiểm tra kết nối MySQL ──────────────────────────")
    try:
        conn = pymysql.connect(
            host     = MYSQL_HOST,
            port     = MYSQL_PORT,
            user     = MYSQL_USER,
            password = MYSQL_PASSWORD,
            database = MYSQL_DATABASE,
            charset  = "utf8mb4",
        )
        with conn.cursor() as cur:
            cur.execute("SELECT VERSION()")
            version = cur.fetchone()[0]
            cur.execute("SELECT DATABASE()")
            db_name = cur.fetchone()[0]
        conn.close()
        print(f"    ✔ Kết nối thành công!")
        print(f"    • MySQL version : {version}")
        print(f"    • Database      : {db_name}")
        print(f"    • Host          : {MYSQL_HOST}:{MYSQL_PORT}")
        print(f"    • User          : {MYSQL_USER}")
        return True
    except pymysql.err.OperationalError as e:
        print(f"    ✘ Kết nối thất bại: {e}")
        print(f"\n    Kiểm tra lại:")
        print(f"    - MySQL đang chạy chưa?  (services.msc → MySQL)")
        print(f"    - User/password đúng chưa? ({MYSQL_USER} / {MYSQL_PASSWORD})")
        print(f"    - Port {MYSQL_PORT} có bị block không?")
        return False


# ==============================================================
# MAIN
# ==============================================================
if __name__ == "__main__":
    print("=" * 55)
    print("  Heart Disease DB — Khởi tạo Database")
    print("=" * 55)

    # Bước 0: kiểm tra kết nối cơ bản
    if not test_connection():
        # Nếu chưa có database thì kết nối sẽ fail — thử tạo
        try:
            create_database_if_not_exists()
        except Exception as e:
            print(f"\n✘ Không thể kết nối MySQL: {e}")
            print("Đảm bảo MySQL đang chạy và thông tin đăng nhập đúng.")
            sys.exit(1)

    try:
        create_database_if_not_exists()
        engine = create_tables()
        seed_admin(engine)
        test_connection()   # Test lại sau khi setup xong

        print("\n" + "=" * 55)
        print("  ✔ Hoàn tất! Database sẵn sàng sử dụng.")
        print("  Chạy server: python run.py")
        print("=" * 55)

    except Exception as e:
        print(f"\n✘ Lỗi khi khởi tạo database: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
