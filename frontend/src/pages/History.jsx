import React, { useState, useEffect } from 'react';
import { getHistory } from '../services/api';

const History = () => {
    const [historyData, setHistoryData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchHistory = async () => {
        setLoading(true);
        setError(null);
        try {
            const response = await getHistory();

            setHistoryData(response.data);
        } catch (err) {
            console.error("Lỗi khi tải lịch sử:", err);
            setError("Không thể kết nối đến máy chủ. Vui lòng kiểm tra lại Backend API và Database.");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchHistory();
    }, []);

    return (
        <div className="container py-5">
            <div className="d-flex justify-content-between align-items-center mb-4">
                <div>
                    <h3 className="fw-bold mb-1" style={{ color: '#202124' }}>Lịch sử Khám bệnh</h3>
                    <p className="text-muted mb-0">Tra cứu các ca chẩn đoán AI đã lưu trong cơ sở dữ liệu</p>
                </div>
                <button
                    className="btn btn-outline-primary rounded-pill px-4 fw-bold shadow-sm"
                    onClick={fetchHistory}
                    disabled={loading}
                >
                    <i className={`bi bi-arrow-clockwise me-2 ${loading ? 'spinner-border spinner-border-sm' : ''}`}></i>
                    {loading ? 'Đang tải...' : 'Làm mới'}
                </button>
            </div>

            {error && (
                <div className="alert alert-danger rounded-4 border-0 shadow-sm p-4 text-center mb-4">
                    <i className="bi bi-x-circle fs-1 mb-2 text-danger"></i>
                    <h5 className="fw-bold">{error}</h5>
                    <p className="mb-0 text-muted">Hệ thống yêu cầu phải có Database và Backend API đang chạy để hiển thị dữ liệu lịch sử.</p>
                </div>
            )}

            {!error && (
                <div className="card shadow-sm border-0 rounded-4 overflow-hidden">
                    <div className="table-responsive">
                        <table className="table table-hover align-middle mb-0">
                            <thead style={{ backgroundColor: '#f8f9fa', color: '#5f6368' }}>
                                <tr>
                                    <th className="px-4 py-3 border-0">Mã HS</th>
                                    <th className="py-3 border-0">Bệnh nhân</th>
                                    <th className="py-3 border-0">CCCD</th>
                                    <th className="py-3 border-0">Tuổi / Giới tính</th>
                                    <th className="py-3 border-0">Kết quả AI</th>
                                    <th className="py-3 border-0">Thời gian khám</th>
                                </tr>
                            </thead>
                            <tbody>
                                {loading ? (
                                    <tr>
                                        <td colSpan="6" className="text-center py-5">
                                            <div className="spinner-border text-primary" role="status"></div>
                                            <div className="mt-3 text-muted fw-bold">Đang tải dữ liệu từ Database...</div>
                                        </td>
                                    </tr>
                                ) : historyData.length === 0 ? (
                                    <tr>
                                        <td colSpan="6" className="text-center py-5 text-muted">
                                            <i className="bi bi-inbox display-4 d-block mb-3" style={{ opacity: 0.3 }}></i>
                                            Chưa có hồ sơ chẩn đoán nào trong hệ thống.
                                        </td>
                                    </tr>
                                ) : (
                                    historyData.map((record) => (
                                        <tr key={record.id} style={{ cursor: 'pointer' }}>
                                            <td className="px-4 fw-bold" style={{ color: '#4285f4' }}>#{record.id}</td>
                                            <td className="fw-bold" style={{ color: '#202124' }}>{record.patientName || 'N/A'}</td>
                                            <td className="text-muted">{record.cccd || 'N/A'}</td>
                                            <td>
                                                <span className="d-block fw-bold">{record.age} tuổi</span>
                                                <span className="text-muted small">{record.sex === 'M' ? 'Nam' : 'Nữ'}</span>
                                            </td>
                                            <td>
                                                <span className={`badge rounded-pill px-3 py-2 ${record.prediction === 1 ? 'bg-danger' : 'bg-success'}`}>
                                                    {record.risk_level || (record.prediction === 1 ? 'Nguy cơ Cao' : 'An toàn')}
                                                </span>
                                            </td>
                                            <td className="text-muted">
                                                <small><i className="bi bi-calendar-event me-1"></i>{record.timestamp}</small>
                                            </td>
                                        </tr>
                                    ))
                                )}
                            </tbody>
                        </table>
                    </div>
                </div>
            )}
        </div>
    );
};

export default History;