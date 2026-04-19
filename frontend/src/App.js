import React from 'react';
import PredictionForm from './components/PredictionForm';
// import PredictionResult from './components/PredictionResult';
import './App.css';
function App() {

//   // Tạo một biến chứa dữ liệu giả để test fe result
// const testData = {
// prediction: 0,
// probability: 0.11,
// risk_level: 'Low'
//
// };
  return (
    <div>
      <PredictionForm />
      {/*<PredictionResult result={testData} />*/}
    </div>
  );
}

export default App;