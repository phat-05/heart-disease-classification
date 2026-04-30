import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Prediction from './pages/Prediction';
import History from './pages/History';

function App() {
  return (
    <Router>
      <div className="d-flex flex-column min-vh-100 bg-light">

        <Navbar />

        <main className="flex-grow-1">
          <Routes>
            <Route path="/" element={<Prediction />} />

            <Route path="/history" element={<History />} />
          </Routes>
        </main>

        <Footer />

      </div>
    </Router>
  );
}

export default App;