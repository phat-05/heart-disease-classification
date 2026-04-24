

import React, { useState } from 'react';
import { predictHeartDisease } from '../services/api';
import PredictionResult from './PredictionResult';

function PredictionForm() {
  const [formData, setFormData] = useState({
    fullName: '',
    idCard: '',
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

    // Chặn lỗi nhập liệu số âm
    if (formData.age < 0 || formData.trestbps < 0 || formData.chol < 0 || formData.thalch < 0) {
      setError("Vui lòng nhập các chỉ số sức khỏe hợp lệ (không được là số âm)!");
      return;
    }

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
      setError('Có lỗi xảy ra. Vui lòng kiểm tra lại kết nối server!');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="prediction-form-container">
      <div className="header-container">
        <img src="/icon_heart.png" alt="Heart Icon" className="heart-icon"
             style={{ width: '40px', height: 'auto', marginRight: '8px', verticalAlign: 'middle' }}/>
        <h1>Heart Disease Classification</h1>
      </div>
      <h3>Sức khỏe là vàng! Hãy kiểm tra sức khỏe thường xuyên bạn nhé!</h3>

      <form onSubmit={handleSubmit}>
        {/* Tên và CCCD */}
        <div className="full-width">
          <label>Họ và Tên:</label>
          <input
            type="text"
            name="fullName"
            placeholder="Nhập đầy đủ họ tên"
            value={formData.fullName}
            onChange={handleChange}
            required
          />
        </div>

        <div className="full-width">
          <label>Số CCCD:</label>
          <input
            type="text"
            name="idCard"
            placeholder="Nhập 12 số CCCD"
            pattern="[0-9]{12}" // Chỉ cho nhập số và đúng 12 số
            maxLength="12"
            title="Vui lòng nhập đúng 12 chữ số CCCD"
            value={formData.idCard}
            onChange={handleChange}
            required
          />
        </div>

        {/*Tuổi và Giới tính */}
        <div>
          <label>Tuổi:</label>
          <input
            type="number"
            name="age"
            min="0" // Tuổi không được âm
            value={formData.age}
            onChange={handleChange}
            required
          />
        </div>

        <div>
          <label>Giới tính:</label>
          <select name="sex" value={formData.sex} onChange={handleChange}>
            <option value="Male">Nam</option>
            <option value="Female">Nữ</option>
          </select>
        </div>

        {/* Loại đau ngực*/}
        <div>
          <label>Loại đau ngực:</label>
          <select name="cp" value={formData.cp} onChange={handleChange}>
            <option value="asymptomatic">Không triệu chứng</option>
            <option value="typical angina">Đau thắt ngực điển hình</option>
            <option value="atypical angina">Đau thắt ngực không điển hình</option>
            <option value="non-anginal">Không phải đau thắt ngực</option>
          </select>
        </div>

        <div>
          <label>Huyết áp lúc nghỉ (mmHg):</label>
          <input
            type="number"
            name="trestbps"
            min="0" // Không âm
            value={formData.trestbps}
            onChange={handleChange}
          />
        </div>

        {/* Hàng 3: Cholesterol và Nhịp tim */}
        <div>
          <label>Cholesterol (mg/dl):</label>
          <input
            type="number"
            name="chol"
            min="0"
            value={formData.chol}
            onChange={handleChange}
          />
        </div>

        <div>
          <label>Nhịp tim tối đa:</label>
          <input
            type="number"
            name="thalch"
            min="0"
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
            min="0"
            name="oldpeak"
            value={formData.oldpeak}
            onChange={handleChange}
          />
        </div>

        {/* Checkbox Đường huyết và Đau ngực */}
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
      {result && <PredictionResult result={result} />}
    </div>
  );
}

export default PredictionForm;