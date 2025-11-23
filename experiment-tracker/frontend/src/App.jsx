import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ExperimentList } from './components/ExperimentList';
import { ExperimentDetail } from './components/ExperimentDetail';
import { ExperimentCompare } from './components/ExperimentCompare';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <header className="app-header">
          <h1>📊 Experiment Tracker</h1>
        </header>
        <main className="app-main">
          <Routes>
            <Route path="/" element={<ExperimentList />} />
            <Route path="/experiments/:id" element={<ExperimentDetail />} />
            <Route path="/compare" element={<ExperimentCompare />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
