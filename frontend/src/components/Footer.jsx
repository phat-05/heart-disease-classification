import React from 'react';

const Footer = () => {
    return (
        <footer
            className="bg-medical text-white py-5 mt-auto shadow-lg"
            style={{ borderTopLeftRadius: '24px', borderTopRightRadius: '24px' }}
        >
            <div className="container">
                <div className="row align-items-center">

                    <div className="col-md-5 mb-4 mb-md-0">
                        <div className="d-flex align-items-center mb-3">
                            <img
                                src="/favicon.ico"
                                alt="HeartAI Logo"
                                className="bg-white rounded-circle p-1 me-2 shadow-sm"
                                style={{ width: '45px', height: '45px', objectFit: 'contain' }}
                            />
                            <h4 className="fw-bold mb-0">Heart<span className="text-warning">AI</span></h4>
                        </div>
                        <p className="small mb-0" style={{ color: 'rgba(255, 255, 255, 0.85)', lineHeight: '1.6' }}>
                            Dự án cuối kỳ - Machine Learning End-to-End.<br />
                            Ứng dụng mô hình AI hỗ trợ sàng lọc y tế tuyến cơ sở.
                        </p>
                    </div>

                    <div className="col-md-2 text-center d-none d-md-block">
                        <i className="bi bi-heart-pulse display-1" style={{ color: 'rgba(255, 255, 255, 0.2)' }}></i>
                    </div>

                    <div className="col-md-5 text-md-end">
                        <h6 className="text-uppercase fw-bold mb-3 text-warning">Thông tin thực hiện</h6>
                        <ul className="list-unstyled small mb-0" style={{ color: 'rgba(255, 255, 255, 0.85)', lineHeight: '1.8' }}>
                            <li>
                                <i className="bi bi-journal-medical me-2 text-white"></i>
                                <strong>Đề tài:</strong> Số 2 - Heart Disease Classification
                            </li>
                            <li>
                                <i className="bi bi-people-fill me-2 text-white"></i>
                                <strong>Nhóm:</strong> 14
                            </li>
                            <li>
                                <i className="bi bi-stack me-2 text-white"></i>
                                <strong>Tech Stack:</strong> ReactJS - Flask - Scikit-learn
                            </li>
                        </ul>
                    </div>
                </div>

                {/* Đường kẻ ngang phân cách */}
                <hr className="my-4" style={{ borderColor: 'rgba(255, 255, 255, 0.2)' }} />

                {/* Dòng bản quyền */}
                <div className="text-center small" style={{ color: 'rgba(255, 255, 255, 0.7)' }}>
                    &copy; {new Date().getFullYear()} Bản quyền thuộc về Nhóm 14.
                </div>
            </div>
        </footer>
    );
};

export default Footer;