// ============================================================
// frontend/src/services/api.js
//
// File này FE đang import nhưng CHƯA CÓ trong project:
//   import { predictHeartDisease } from '../services/api';
//
// Đây là nơi tập trung mọi HTTP call → dễ đổi base URL,
// thêm auth header, handle lỗi chung một chỗ.
// ============================================================

// Base URL của BE FastAPI
// Development: chạy local
// Production: đổi thành domain thật
const BASE_URL = "http://localhost:8000/api";


/**
 * Gọi POST /api/predict với 13 chỉ số y tế
 *
 * @param {Object} formData - Dữ liệu từ PredictionForm.js
 * @returns {Promise<{prediction: number, probability: number, risk_level: string}>}
 * @throws {Error} nếu server trả lỗi hoặc network fail
 */
export async function predictHeartDisease(formData) {
  // fetch() là Web API built-in — không cần install thêm gì
  const response = await fetch(`${BASE_URL}/predict/`, {
    method: "POST",

    headers: {
      // Content-Type: application/json BẮT BUỘC phải có
      // Thiếu header này → FastAPI không biết body là JSON → lỗi 422
      "Content-Type": "application/json",
    },

    // JSON.stringify: chuyển JS object → chuỗi JSON để gửi qua HTTP
    body: JSON.stringify(formData),
  });

  // Kiểm tra HTTP status code
  // response.ok = true nếu status 200-299
  if (!response.ok) {
    // Cố đọc error message từ BE nếu có
    const errorData = await response.json().catch(() => null);
    const detail = errorData?.detail || `HTTP ${response.status}`;
    throw new Error(detail);
  }

  // response.json(): parse chuỗi JSON response → JS object
  // Kết quả: { prediction: 1, probability: 0.7823, risk_level: "High" }
  return response.json();
}