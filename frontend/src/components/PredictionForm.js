
import React, { useState } from 'react';
import { predictHeartDisease } from '../services/api';
import PredictionResult from './PredictionResult';

function PredictionForm() {
  const [formData, setFormData] = useState({
    age: '',
    sex: 'Male',
    cp: 'asymptomatic',
    trestbps: '',
    chol: '',
    fbs: false,
    restecg: 'normal',
    thalch: '',
    exang: false,
    oldpeak: '',
    slope: 'flat',
    ca: '',
    thal: 'normal',
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const payload = {
        ...formData,
        age: parseInt(formData.age),
        trestbps: parseFloat(formData.trestbps),
        chol: parseFloat(formData.chol),
        thalch: parseFloat(formData.thalch),
        oldpeak: parseFloat(formData.oldpeak),
        ca: formData.ca ? parseFloat(formData.ca) : null,
      };

      const data = await predictHeartDisease(payload);
      setResult(data);
    } catch (err) {
      setError('Có lỗi xảy ra. Vui lòng kiểm tra lại!');
    } finally {
      setLoading(false);
    }
  };

  return (

  // Thêm className để nhận CSS từ App.css
  <div className="prediction-form-container">
      <div className="header-container">
        <img src="/icon_heart.png" alt="Heart Icon" className="heart-icon"
             style={{ width: '40px', height: 'auto', marginRight: '8px', verticalAlign: 'middle' }}/>
        <h1>Heart Disease Classification</h1>
      </div>
      <h3>Sức khỏe là vàng! Hãy kiểm tra sức khỏe thường xuyên bạn nhé!</h3>

      <form onSubmit={handleSubmit}>
        {/* Tuổi */}
        <div>
          <label>Tuổi:</label>
          <input
            type="number"
            name="age"
            value={formData.age}
            onChange={handleChange}
            required
          />
        </div>

        {/* Giới tính */}
        <div>
          <label>Giới tính:</label>
          <select name="sex" value={formData.sex} onChange={handleChange}>
            <option value="Male">Nam</option>
            <option value="Female">Nữ</option>
          </select>
        </div>

        {/* Loại đau ngực */}
        <div>
          <label>Loại đau ngực:</label>
          <select name="cp" value={formData.cp} onChange={handleChange}>
            <option value="asymptomatic">Không triệu chứng</option>
            <option value="typical angina">Đau thắt ngực điển hình</option>
            <option value="atypical angina">Đau thắt ngực không điển hình</option>
            <option value="non-anginal">Không phải đau thắt ngực</option>
          </select>
        </div>

        {/* Huyết áp */}
        <div>
          <label>Huyết áp lúc nghỉ (mmHg):</label>
          <input
            type="number"
            name="trestbps"
            value={formData.trestbps}
            onChange={handleChange}
          />
        </div>

        {/* Cholesterol */}
        <div>
          <label>Cholesterol (mg/dl):</label>
          <input
            type="number"
            name="chol"
            value={formData.chol}
            onChange={handleChange}
          />
        </div>

        {/* Nhịp tim tối đa */}
        <div>
          <label>Nhịp tim tối đa:</label>
          <input
            type="number"
            name="thalch"
            value={formData.thalch}
            onChange={handleChange}
          />
        </div>

        {/* ST Depression */}
        <div>
          <label>ST Depression (oldpeak):</label>
          <input
            type="number"
            step="0.1"
            name="oldpeak"
            value={formData.oldpeak}
            onChange={handleChange}
          />
        </div>

        {/* Checkbox Đường huyết - full-width */}
        <div className="full-width checkbox-container">
          <label>
            <input
              type="checkbox"
              name="fbs"
              checked={formData.fbs}
              onChange={handleChange}
            />
            Đường huyết lúc đói &gt; 120 mg/dl
          </label>
        </div>

        {/* Checkbox Đau ngực - full-width */}
        <div className="full-width checkbox-container">
          <label>
            <input
              type="checkbox"
              name="exang"
              checked={formData.exang}
              onChange={handleChange}
            />
            Đau ngực khi vận động
          </label>
        </div>

        <button type="submit" disabled={loading}>
          {loading ? 'Đang dự đoán...' : 'Dự đoán'}
        </button>
      </form>

      {error && <p className="error-message">{error}</p>}

      {/* Kết quả */}
      {result && <PredictionResult result={result} />}
    </div>
  );
}

export default PredictionForm;