import React, { useState } from 'react';
import Summary from './Summary';
import TicketTable from './TicketTable';
import WitchScores from './WitchScores';
import FactoryMap from './FactoryMap';
import './Dashboard.css';

function Dashboard({ data, onRefresh, autoRefresh, onToggleAutoRefresh }) {
  const [activeTab, setActiveTab] = useState('overview');

  const { summary, tickets, witch_trust_scores, background } = data;

  return (
    <div className="dashboard">
      {/* Header */}
      <header className="dashboard-header">
        <div className="header-content">
          <h1>🔮 Truth Serum</h1>
          <p className="subtitle">Potion Factory Fraud Detection System</p>
        </div>
        <div className="header-controls">
          <button 
            onClick={onToggleAutoRefresh} 
            className={`auto-refresh-button ${autoRefresh ? 'active' : ''}`}
          >
            {autoRefresh ? '⏸️ Auto-Refresh ON' : '▶️ Auto-Refresh OFF'}
          </button>
          <button onClick={onRefresh} className="refresh-button">
            🔄 Refresh Now
          </button>
        </div>
      </header>

      {/* Navigation Tabs */}
      <nav className="tab-nav">
        <button
          className={`tab-button ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          📊 Overview
        </button>
        <button
          className={`tab-button ${activeTab === 'tickets' ? 'active' : ''}`}
          onClick={() => setActiveTab('tickets')}
        >
          🎫 Tickets
        </button>
        <button
          className={`tab-button ${activeTab === 'witches' ? 'active' : ''}`}
          onClick={() => setActiveTab('witches')}
        >
          🧙‍♀️ Witches
        </button>
        <button
          className={`tab-button ${activeTab === 'map' ? 'active' : ''}`}
          onClick={() => setActiveTab('map')}
        >
          🗺️ Factory Map
        </button>
      </nav>

      {/* Content */}
      <main className="dashboard-content">
        {activeTab === 'overview' && (
          <div>
            <Summary summary={summary} />
            <div className="overview-grid">
              <div className="overview-card">
                <h3>🎯 Top Fraudsters</h3>
                <WitchScores witches={witch_trust_scores.slice(0, 3)} compact />
              </div>
              <div className="overview-card">
                <h3>🚨 Recent Suspicious Activity</h3>
                <TicketTable 
                  tickets={tickets.filter(t => t.status !== 'valid').slice(0, 5)} 
                  compact 
                />
              </div>
            </div>
          </div>
        )}

        {activeTab === 'tickets' && (
          <TicketTable tickets={tickets} />
        )}

        {activeTab === 'witches' && (
          <WitchScores witches={witch_trust_scores} />
        )}

        {activeTab === 'map' && (
          <FactoryMap background={background} />
        )}
      </main>

      {/* Footer */}
      <footer className="dashboard-footer">
        
        {autoRefresh && <p className="auto-refresh-indicator">🔄 Auto-refreshing every 30 seconds...</p>}
      </footer>
    </div>
  );
}

export default Dashboard;
