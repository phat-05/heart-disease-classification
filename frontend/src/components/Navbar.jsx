import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Navbar = () => {
    const location = useLocation();

    return (
        <nav className="navbar navbar-expand-lg navbar-dark bg-medical shadow-sm py-3 mb-4">
            <div className="container">
                <Link className="navbar-brand d-flex align-items-center fw-bold fs-4" to="/">
                    <img
                        src="/favicon.ico"
                        alt="HeartAI Logo"
                        className="brand-icon"
                        style={{ width: '35px', height: '35px', objectFit: 'contain' }}
                    />
                    Heart<span className="text-warning">AI</span>
                </Link>

                <button
                    className="navbar-toggler border-0"
                    type="button"
                    data-bs-toggle="collapse"
                    data-bs-target="#navbarNav"
                >
                    <span className="navbar-toggler-icon"></span>
                </button>

                <div className="collapse navbar-collapse" id="navbarNav">
                    <ul className="navbar-nav ms-auto align-items-center">

                        <li className="nav-item me-3 mb-2 mb-lg-0">
                            <Link
                                className={`nav-link fw-semibold fs-6 ${location.pathname === '/history' ? 'active text-white fw-bold' : 'text-white'}`}
                                to="/history"
                            >
                                <i className="bi bi-clock-history me-1"></i> Lịch sử Khám
                            </Link>
                        </li>

                        <li className="nav-item">
                            <Link
                                className={`nav-link fw-semibold fs-6 ${location.pathname === '/' ? 'active text-white fw-bold' : 'text-white'}`}                                to="/"
                            >
                                <i className="bi bi-activity me-1"></i> Chẩn đoán Mới
                            </Link>
                        </li>

                    </ul>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;