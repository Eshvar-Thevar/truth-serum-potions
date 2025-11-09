import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Dashboard from './components/Dashboard';
import './App.css';

const API_URL = 'http://localhost:5000';

function App() {
  const [analysisData, setAnalysisData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [autoRefresh, setAutoRefresh] = useState(false);

  useEffect(() => {
    fetchAnalysis();
  }, []);

  // Auto-refresh every 30 seconds if enabled
  useEffect(() => {
    if (autoRefresh) {
      const interval = setInterval(() => {
        console.log('🔄 Auto-refreshing data...');
        fetchAnalysis();
      }, 30000); // 30 seconds

      return () => clearInterval(interval);
    }
  }, [autoRefresh]);

  const fetchAnalysis = async () => {
    setLoading(true);
    setError(null);
    
    try {
      console.log('🔮 Fetching fraud analysis...');
      const response = await axios.get(`${API_URL}/api/analysis`);
      setAnalysisData(response.data);
      console.log('✅ Analysis loaded successfully!');
    } catch (err) {
      console.error('❌ Error fetching analysis:', err);
      setError('Failed to load analysis. Make sure the backend is running on http://localhost:5000');
    } finally {
      setLoading(false);
    }
  };

  const refreshData = async () => {
    try {
      await axios.post(`${API_URL}/api/refresh`);
      fetchAnalysis();
    } catch (err) {
      console.error('Error refreshing data:', err);
    }
  };

  const toggleAutoRefresh = () => {
    setAutoRefresh(!autoRefresh);
  };

  if (loading) {
    return (
      <div className="app-container loading">
        <div className="loading-content">
          <h1>🔮 Truth Serum</h1>
          <div className="spinner"></div>
          <p>Analyzing potion transport tickets...</p>
          <p className="hint">Detecting dishonest witches... 🧙‍♀️</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="app-container error">
        <div className="error-content">
          <h1>❌ Error</h1>
          <p>{error}</p>
          <div className="instructions">
            <h3>To fix this:</h3>
            <ol>
              <li>Open a terminal in VS Code</li>
              <li>Navigate to the backend folder: <code>cd backend</code></li>
              <li>Install dependencies: <code>pip install -r requirements.txt</code></li>
              <li>Start the server: <code>python api.py</code></li>
            </ol>
          </div>
          <button onClick={fetchAnalysis} className="retry-button">
            🔄 Retry Connection
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="app-container">
      <Dashboard 
        data={analysisData} 
        onRefresh={refreshData}
        autoRefresh={autoRefresh}
        onToggleAutoRefresh={toggleAutoRefresh}
      />
    </div>
  );
}

export default App;
