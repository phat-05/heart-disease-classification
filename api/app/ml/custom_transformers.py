import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class OutlierHandler(BaseEstimator, TransformerMixin):
    """Xử lý các giá trị bất hợp lệ về mặt lâm sàng bằng cách thay thế bằng NaN."""
    def fit(self, X, y=None):
        """
        Không học tham số, trả về self để tương thích với Pipeline.

        Args:
            X (pd.DataFrame): Dữ liệu đầu vào.
            y: Bỏ qua, chỉ có mặt để tương thích với scikit-learn API.

        Returns:
            self: Trả về chính transformer.
        """
        # Return self vì bước này không cần học tham số (như mean/std) từ tập train
        return self

    def transform(self, X):
        """Thay thế các giá trị 0 bất khả thi lâm sàng bằng NaN.

        Các cột 'trestbps' (huyết áp) và 'chol' (cholesterol) không thể
        có giá trị 0 trên thực tế, nên 0 được coi là dữ liệu bị thiếu.

        Args:
            X (pd.DataFrame): DataFrame chứa ít nhất hai cột
                'trestbps' và 'chol'.

        Returns:
            pd.DataFrame: Bản sao của X với các giá trị 0 trong
                'trestbps' và 'chol' đã được thay thế bằng NaN.
        """
        X_new = X.copy()

        # 0 là giá trị bất khả thi trên lâm sàng đối với huyết áp và cholesterol
        X_new['trestbps'] = X_new['trestbps'].replace(0, np.nan)
        X_new['chol'] = X_new['chol'].replace(0, np.nan)

        return X_new

class FeatureEngineer(BaseEstimator, TransformerMixin):
    """Tạo các đặc trưng mới (Feature Engineering) dựa trên kiến thức y khoa lâm sàng."""

    def fit(self, X, y=None):
        """
        Không học tham số, trả về self để tương thích với Pipeline.

        Args:
            X (pd.DataFrame): Dữ liệu đầu vào.
            y: Bỏ qua, chỉ có mặt để tương thích với scikit-learn API.

        Returns:
            self: Trả về chính transformer.
        """
        return self

    def transform(self, X):
        """Tạo hai đặc trưng mới: tỷ lệ nhịp tim (heart_rate_ratio) và nhóm rủi ro theo tuổi (age_risk_group).

        - 'heart_rate_ratio': Tỷ lệ giữa nhịp tim thực tế ('thalch') và ngưỡng tối đa lý thuyết (220 - 'age').
        - 'age_risk_group': Phân nhóm độ tuổi thành 4 mức rủi ro (0: 0-40, 1: 40-50, 2: 50-60, 3: 60+)
          dựa trên hiệu ứng ngưỡng nguy hiểm.

        Args:
            X (pd.DataFrame): DataFrame chứa ít nhất hai cột
                'age' và 'thalch'.

        Returns:
            pd.DataFrame: Bản sao của X đã được bổ sung thêm hai cột
                mới là 'heart_rate_ratio' và 'age_risk_group'.
        """
        X_new = X.copy()

        # 1. Feature: heart_rate_ratio
        X_new['heart_rate_ratio'] = X_new['thalch'] / (220 - X_new['age'])

        # 2. Feature: age_risk_group
        # Chia bins: 0–40 (0), 40–50 (1), 50–60 (2), 60+ (3)
        bins = [0, 40, 50, 60, np.inf]
        labels = [0, 1, 2, 3]
        X_new['age_risk_group'] = pd.cut(X_new['age'], bins=bins, labels=labels).astype(int)

        return X_new