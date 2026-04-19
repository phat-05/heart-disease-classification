import axios from 'axios';

// Tạo instance axios với base URL
// Mọi request đều tự động gọi đến địa chỉ này
const API = axios.create({
  baseURL: 'http://localhost:8000',
});

// Hàm gọi endpoint /predict
export const predictHeartDisease = async (patientData) => {
  const response = await API.post('/predict', patientData);
  return response.data; // trả về { prediction, probability, risk_level }
};