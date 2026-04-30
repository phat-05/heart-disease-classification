import React, { useState } from 'react';
import { predictHeartDisease } from '../services/api';

const Prediction = () => {
    const [formData, setFormData] = useState({
        patientName: '', cccd: '',
        age: '', trestbps: '', chol: '', thalch: '', oldpeak: '',
        sex: 'M', cp: 'ASY', fbs: '0', restecg: 'Normal', exang: 'N', slope: 'Flat'
    });

    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const isFormValid = Object.values(formData).every(value => value !== '');

    const handleChange = (e) => {
        const { name, value, type } = e.target;

        if (type === 'number' && Number(value) < 0) {
            return;
        }

        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!isFormValid) return;

        setLoading(true);
        setError(null);
        setResult(null);

        try {
            const payload = {
                ...formData,
                age: Number(formData.age),
                trestbps: Number(formData.trestbps),
                chol: Number(formData.chol),
                thalch: Number(formData.thalch),
                oldpeak: Number(formData.oldpeak)
            };

            const response = await predictHeartDisease(payload);
            setResult(response.data);

            window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
        } catch (err) {
            setError("Có lỗi xảy ra khi kết nối hệ thống chẩn đoán.");
        } finally {
            setLoading(false);
        }
    };

    const getRiskStatus = (probability) => {
        if (probability >= 0.70) return { color: 'danger', icon: 'bi-exclamation-octagon-fill', label: 'Nguy Cơ Rất Cao' };
        if (probability >= 0.40) return { color: 'warning', icon: 'bi-exclamation-triangle-fill', label: 'Có Nguy Cơ (Cần theo dõi)' };
        return { color: 'success', icon: 'bi-shield-check-fill', label: 'Tạm Thời An Toàn' };
    };

    return (
        <div className="container py-5">
            <div className="row justify-content-center">
                <div className="col-lg-8 col-md-10">

                    <div className="card shadow-sm border-0 rounded-4 p-4 p-md-5 mb-4">
                        <div className="text-center mb-5">
                            <h3 className="fw-bold" style={{ color: '#202124' }}>Hồ sơ Lâm sàng Bệnh nhân</h3>
                            <p className="text-muted">Vui lòng điền đầy đủ các chỉ số dưới đây để hệ thống AI phân tích</p>
                        </div>

                        <form onSubmit={handleSubmit}>
                            <h6 className="fw-bold mt-2 mb-3" style={{ color: '#4285f4' }}><i className="bi bi-person-vcard me-2"></i>1. Định danh</h6>
                            <div className="row g-3 mb-4">
                                <div className="col-md-6">
                                    <label className="form-label text-muted small fw-bold mb-1">Họ và Tên Bệnh nhân <span className="text-danger">*</span></label>
                                    <input type="text" className="form-control" name="patientName" value={formData.patientName} onChange={handleChange} required />
                                </div>
                                <div className="col-md-6">
                                    <label className="form-label text-muted small fw-bold mb-1">CCCD <span className="text-danger">*</span></label>
                                    <input type="number" className="form-control" name="cccd" value={formData.cccd} onChange={handleChange} min="0" required />
                                </div>
                            </div>

                            <h6 className="fw-bold mt-4 mb-3" style={{ color: '#4285f4' }}><i className="bi bi-heart-pulse me-2"></i>2. Chỉ số Sinh tồn</h6>
                            <div className="row g-3 mb-4">
                                <div className="col-md-4">
                                    {/* Thêm thuộc tính min="0" để chặn nhập số âm trên giao diện HTML5 */}
                                    <label className="form-label text-muted small fw-bold mb-1">Tuổi (Age) <span className="text-danger">*</span></label>
                                    <input type="number" className="form-control" name="age" value={formData.age} onChange={handleChange} min="0" required />
                                </div>
                                <div className="col-md-4">
                                    <label className="form-label text-muted small fw-bold mb-1">Giới tính (Sex) <span className="text-danger">*</span></label>
                                    <select className="form-select" name="sex" value={formData.sex} onChange={handleChange}>
                                        <option value="M">Nam</option>
                                        <option value="F">Nữ</option>
                                    </select>
                                </div>
                                <div className="col-md-4">
                                    <label className="form-label text-muted small fw-bold mb-1">Huyết áp lúc nghỉ <span className="text-danger">*</span></label>
                                    <input type="number" className="form-control" name="trestbps" value={formData.trestbps} onChange={handleChange} min="0" placeholder="mmHg" required />
                                </div>
                            </div>

                            <h6 className="fw-bold mt-4 mb-3" style={{ color: '#4285f4' }}><i className="bi bi-droplet me-2"></i>3. Cận lâm sàng</h6>
                            <div className="row g-3 mb-4">
                                <div className="col-md-4">
                                    <label className="form-label text-muted small fw-bold mb-1">Cholesterol <span className="text-danger">*</span></label>
                                    <input type="number" className="form-control" name="chol" value={formData.chol} onChange={handleChange} min="0" placeholder="mg/dl" required />
                                </div>
                                <div className="col-md-4">
                                    <label className="form-label text-muted small fw-bold mb-1">Đường huyết đói &gt; 120</label>
                                    <select className="form-select" name="fbs" value={formData.fbs} onChange={handleChange}>
                                        <option value="0">Không (0)</option>
                                        <option value="1">Có (1)</option>
                                    </select>
                                </div>
                                <div className="col-md-4">
                                    <label className="form-label text-muted small fw-bold mb-1">Điện tâm đồ (Restecg)</label>
                                    <select className="form-select" name="restecg" value={formData.restecg} onChange={handleChange}>
                                        <option value="Normal">Bình thường</option>
                                        <option value="ST-T">Bất thường ST-T</option>
                                        <option value="LVH">Phì đại thất trái</option>
                                    </select>
                                </div>
                            </div>

                            <h6 className="fw-bold mt-4 mb-3" style={{ color: '#4285f4' }}><i className="bi bi-activity me-2"></i>4. Bài test gắng sức</h6>
                            <div className="row g-3 mb-5">
                                <div className="col-md-4">
                                    <label className="form-label text-muted small fw-bold mb-1">Loại đau ngực (Cp)</label>
                                    <select className="form-select" name="cp" value={formData.cp} onChange={handleChange}>
                                        <option value="ASY">Không triệu chứng</option>
                                        <option value="NAP">Đau không điển hình</option>
                                        <option value="ATA">Đau điển hình</option>
                                        <option value="TA">Đau thắt ngực</option>
                                    </select>
                                </div>
                                <div className="col-md-4">
                                    <label className="form-label text-muted small fw-bold mb-1">Nhịp tim tối đa <span className="text-danger">*</span></label>
                                    <input type="number" className="form-control" name="thalch" value={formData.thalch} onChange={handleChange} min="0" required />
                                </div>
                                <div className="col-md-4">
                                    <label className="form-label text-muted small fw-bold mb-1">Đau ngực khi gắng sức</label>
                                    <select className="form-select" name="exang" value={formData.exang} onChange={handleChange}>
                                        <option value="N">Không (N)</option>
                                        <option value="Y">Có (Y)</option>
                                    </select>
                                </div>
                                <div className="col-md-6">
                                    <label className="form-label text-muted small fw-bold mb-1">ST chênh xuống (Oldpeak) <span className="text-danger">*</span></label>
                                    <input type="number" step="0.1" className="form-control" name="oldpeak" value={formData.oldpeak} onChange={handleChange} min="0" required />
                                </div>
                                <div className="col-md-6">
                                    <label className="form-label text-muted small fw-bold mb-1">Độ dốc đoạn ST (Slope)</label>
                                    <select className="form-select" name="slope" value={formData.slope} onChange={handleChange}>
                                        <option value="Up">Đi lên (Up)</option>
                                        <option value="Flat">Ngang (Flat)</option>
                                        <option value="Down">Đi xuống (Down)</option>
                                    </select>
                                </div>
                            </div>

                            <button
                                type="submit"
                                className={`btn w-100 fw-bold fs-5 p-3 rounded-pill shadow-sm transition-all ${isFormValid ? 'btn-primary' : 'btn-secondary opacity-50'}`}
                                disabled={!isFormValid || loading}
                                style={{
                                    background: isFormValid ? 'linear-gradient(135deg, #0052D4 0%, #4364F7 100%)' : '#e0e0e0',
                                    border: 'none',
                                    transform: isFormValid && !loading ? 'translateY(-2px)' : 'none',
                                    cursor: isFormValid ? 'pointer' : 'not-allowed'
                                }}
                            >
                                {loading ? (
                                    <><span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span> Đang xử lý AI...</>
                                ) : (
                                    <><i className="bi bi-robot me-2"></i> Phân tích Dữ liệu</>
                                )}
                            </button>
                            {!isFormValid && (
                                <p className="text-danger text-center mt-2 small mb-0">
                                    <i className="bi bi-info-circle me-1"></i>Vui lòng nhập đầy đủ các trường có dấu (*) để tiếp tục.
                                </p>
                            )}
                        </form>
                    </div>

                    {error && (
                        <div className="alert alert-danger rounded-4 border-0 shadow-sm p-4 text-center">
                            <i className="bi bi-x-circle fs-1 mb-2"></i>
                            <h5 className="fw-bold">{error}</h5>
                        </div>
                    )}

                    {result && !loading && (() => {
                        const status = getRiskStatus(result.probability);

                        return (
                            <div className={`card shadow border-0 rounded-4 overflow-hidden mt-4 border-top border-4 border-${status.color}`}>
                                <div className={`p-2 text-center text-white fw-bold bg-${status.color}`}>
                                    BÁO CÁO SÀNG LỌC BỆNH TIM MẠCH
                                </div>
                                <div className="card-body p-4 p-md-5 text-center">
                                    <div className={`display-1 mb-3 text-${status.color}`}>
                                        <i className={`bi ${status.icon}`}></i>
                                    </div>
                                    <h2 className={`fw-bold mb-4 text-${status.color}`}>
                                        {status.label}
                                    </h2>

                                    <div className="bg-light rounded-4 p-4 mb-4 text-start">
                                        <div className="d-flex justify-content-between mb-3 border-bottom pb-2">
                                            <span className="text-muted fw-bold">Bệnh nhân:</span>
                                            <span className="fw-bold fs-5" style={{ color: '#202124' }}>{formData.patientName || 'N/A'}</span>
                                        </div>
                                        <div className="d-flex justify-content-between mb-3 border-bottom pb-2">
                                            <span className="text-muted fw-bold">CCCD/CMND:</span>
                                            <span className="fw-bold">{formData.cccd || 'N/A'}</span>
                                        </div>
                                        <div className="d-flex justify-content-between mb-2">
                                            <span className="text-muted fw-bold">Xác suất AI dự đoán:</span>
                                            <span className={`fw-bold fs-4 text-${status.color}`}>
                                                {(result.probability * 100).toFixed(2)}%
                                            </span>
                                        </div>
                                    </div>

                                    <p className="text-muted small text-start mb-0">
                                        <i className="bi bi-info-circle-fill me-1"></i>
                                        <strong>Lưu ý y khoa:</strong> Hệ thống AI phân loại dựa trên tập dữ liệu lâm sàng. Kết quả này chỉ mang tính chất tham khảo sàng lọc sớm (screening) và tuyệt đối không thay thế kết luận chẩn đoán của bác sĩ chuyên khoa.
                                    </p>
                                </div>
                            </div>
                        );
                    })()}

                </div>
            </div>
        </div>
    );
};

export default Prediction;