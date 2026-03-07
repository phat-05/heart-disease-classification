# heart-disease-classification – Đề tài số 2 - Heart Disease Classification

## Mô tả
## Mô tả
Bệnh tim mạch là nguyên nhân tử vong hàng đầu trên thế giới. Việc chẩn đoán sớm dựa trên các chỉ số lâm sàng (tuổi, huyết áp, cholesterol, ECG, …) giúp can thiệp kịp thời và giảm nguy cơ tử vong.  
Mục tiêu của dự án là xây dựng mô hình phân loại bệnh tim (có bệnh / không có bệnh) từ dữ liệu lâm sàng. Mô hình ưu tiên Recall cao để hạn chế bỏ sót bệnh nhân, đồng thời duy trì Precision hợp lý nhằm giảm số lượng cảnh báo sai.  
Dataset sử dụng: **UCI Machine Learning Repository – Heart Disease** (hoặc Kaggle "Heart Disease UCI").

## Thành viên nhóm
|    MSSV     |       Họ tên       |   Vai trò   |
|-------------|--------------------|-------------|
| 2351050132  | Phạm Thành Phát    | PM , ML, BE |
| 2351050145  | Ngô Thị Thúy Quyên | FE , ML, QA |
| 2351050209  | Phạm Thị Mỹ Xuyên  | BE, ML, QA  |

## Công nghệ
– ML: Python, sklearn, Jupyter  
– Frontend: ReactJS  
– Backend: Flask   
– Tracking: wandb
– Database: MySQL


## Cài đặt và chạy

### Yêu cầu
– Python 3.10, Node.js (nếu dùng React)

### Chạy Notebook
jupyter notebook notebooks/project_analysis.ipynb

### Chạy Backend
cd api && pip install -r requirements.txt && python app.py

### Chạy Frontend
cd frontend && npm install && npm start

### Truy cập
– Frontend: http://localhost:3000  
– API: http://localhost:5000 (hoặc port tương ứng)

## Demo
– wandb: [link]  
– Screenshot/video: [link hoặc mô tả]

## Nộp bài
– Báo cáo: report/report.pdf  
– wandb link: wandb_link.txt
