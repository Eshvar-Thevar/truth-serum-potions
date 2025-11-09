import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import './WitchScores.css';

function WitchScores({ witches, compact = false }) {
  const getTrustLevel = (score) => {
    if (score >= 80) return { level: 'Trustworthy', emoji: '✨', class: 'trust-high' };
    if (score >= 50) return { level: 'Questionable', emoji: '🤔', class: 'trust-medium' };
    return { level: 'DISHONEST', emoji: '🚨', class: 'trust-low' };
  };

  const chartData = witches.map(witch => ({
    name: witch.courier_id.replace('courier_witch_', 'Witch '),
    trust: witch.trust_score,
    accuracy: witch.accuracy_percent
  }));

  return (
    <div className={`witch-scores-container ${compact ? 'compact' : ''}`}>
      {!compact && (
        <>
          <h2>🧙‍♀️ Witch Trust Leaderboard</h2>
          <p className="subtitle">Ranked by honesty (worst first)</p>
        </>
      )}

      <div className="witch-cards">
        {witches.map((witch, index) => {
          const trust = getTrustLevel(witch.trust_score);
          return (
            <div key={witch.courier_id} className={`witch-card ${trust.class}`}>
              <div className="witch-header">
                <div className="witch-rank">#{index + 1}</div>
                <div className="witch-name">
                  {witch.courier_id.replace('courier_witch_', 'Witch ')}
                </div>
                <div className="witch-emoji">{trust.emoji}</div>
              </div>

              <div className="witch-stats">
                <div className="stat-row">
                  <span className="stat-label">Trust Score:</span>
                  <div className="trust-bar-container">
                    <div 
                      className="trust-bar" 
                      style={{ width: `${witch.trust_score}%` }}
                    />
                    <span className="trust-value">{witch.trust_score}/100</span>
                  </div>
                </div>

                <div className="stat-row">
                  <span className="stat-label">Accuracy:</span>
                  <span className="stat-value">{witch.accuracy_percent.toFixed(1)}%</span>
                </div>

                <div className="stat-row">
                  <span className="stat-label">Total Tickets:</span>
                  <span className="stat-value">{witch.total_tickets}</span>
                </div>

                <div className="stat-grid">
                  <div className="mini-stat valid">
                    <div>✅ {witch.valid_tickets}</div>
                    <small>Valid</small>
                  </div>
                  <div className="mini-stat suspicious">
                    <div>🟡 {witch.suspicious_tickets}</div>
                    <small>Suspicious</small>
                  </div>
                  <div className="mini-stat fraudulent">
                    <div>🚨 {witch.fraudulent_tickets}</div>
                    <small>Fraud</small>
                  </div>
                </div>

                {witch.total_fraud_amount > 0 && (
                  <div className="fraud-amount">
                    💰 Total fraud: {witch.total_fraud_amount.toFixed(2)} units
                  </div>
                )}
              </div>

              <div className="trust-badge">
                {trust.level}
              </div>
            </div>
          );
        })}
      </div>

      {!compact && witches.length > 3 && (
        <div className="chart-section">
          <h3>📊 Trust Score Comparison</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
              <XAxis dataKey="name" stroke="white" />
              <YAxis stroke="white" />
              <Tooltip 
                contentStyle={{ 
                  background: 'rgba(0,0,0,0.8)', 
                  border: 'none',
                  borderRadius: '10px'
                }}
              />
              <Legend />
              <Bar dataKey="trust" fill="#8b5cf6" name="Trust Score" />
              <Bar dataKey="accuracy" fill="#ec4899" name="Accuracy %" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
}

export default WitchScores;
