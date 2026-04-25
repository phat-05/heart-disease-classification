import React from 'react';

function PredictionResult({ result }) {
  const { prediction, probability, risk_level } = result;

  console.log(result);
  console.log(prediction);
  console.log(probability);
  console.log(risk_level);

  const riskStyles = {
    Low: { color: '#2e7d32', bgColor: '#e8f5e9', label: 'Thấp', icon: '💚' },
    Medium: { color: '#ef6c00', bgColor: '#fff3e0', label: 'Trung bình', icon: '💛' },
    High: { color: '#c62828', bgColor: '#ffebee', label: 'Cao', icon: '💔 ' },
  };

  const currentRisk = riskStyles[risk_level] || riskStyles.Low;

  return (
    <div className="prediction-result-container" style={{
      marginTop: '30px',
      padding: '20px',
      borderRadius: '12px',
      backgroundColor: currentRisk.bgColor,
      border: `2px solid ${currentRisk.color}`,
      textAlign: 'center',
      animation: 'fadeIn 0.5s ease-in-out'
    }}>
      <h2 style={{ color: '#333', marginBottom: '15px' }}>Kết Quả Phân Tích</h2>

      <div style={{ fontSize: '1.2em', marginBottom: '10px' }}>
        <strong>Chẩn đoán:</strong>{' '}
        {prediction === 1
          ? 'Phát hiện dấu hiệu bất thường'
          : 'Chưa phát hiện dấu hiệu bất thường'}
      </div>

      <div style={{ marginBottom: '10px' }}>
        <strong>Xác suất chính xác:</strong>{' '}
        <span style={{ fontSize: '1.4em', fontWeight: 'bold', color: '#0047ab' }}>
          {(probability * 100).toFixed(1)}%
        </span>
      </div>

      <div style={{
        display: 'inline-block',
        padding: '10px 20px',
        borderRadius: '20px',
        backgroundColor: currentRisk.color,
        color: 'white',
        fontWeight: 'bold',
        fontSize: '1.1em'
      }}>
        {currentRisk.icon} Mức độ rủi ro: {currentRisk.label}
      </div>

      <p style={{ fontSize: '0.85em', color: '#666', marginTop: '15px', fontStyle: 'italic' }}>
        * Lưu ý: Đây là kết quả từ mô hình AI, chỉ mang tính chất tham khảo.
      </p>
    </div>
  );
}

export default PredictionResult;