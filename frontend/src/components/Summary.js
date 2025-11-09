import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';
import './Summary.css';

function Summary({ summary }) {
  const { total_tickets, valid_count, suspicious_count, fraudulent_count, fraud_rate } = summary;

  const chartData = [
    { name: 'Valid', value: valid_count, color: '#10b981' },
    { name: 'Suspicious', value: suspicious_count, color: '#f59e0b' },
    { name: 'Fraudulent', value: fraudulent_count, color: '#ef4444' }
  ];

  return (
    <div className="summary-container">
      <div className="summary-grid">
        {/* Stat Cards */}
        <div className="stat-card total">
          <div className="stat-icon">🎫</div>
          <div className="stat-content">
            <h3>Total Tickets</h3>
            <p className="stat-value">{total_tickets}</p>
          </div>
        </div>

        <div className="stat-card valid">
          <div className="stat-icon">✅</div>
          <div className="stat-content">
            <h3>Valid</h3>
            <p className="stat-value">{valid_count}</p>
            <p className="stat-percent">{((valid_count / total_tickets) * 100).toFixed(1)}%</p>
          </div>
        </div>

        <div className="stat-card suspicious">
          <div className="stat-icon">🟡</div>
          <div className="stat-content">
            <h3>Suspicious</h3>
            <p className="stat-value">{suspicious_count}</p>
            <p className="stat-percent">{((suspicious_count / total_tickets) * 100).toFixed(1)}%</p>
          </div>
        </div>

        <div className="stat-card fraudulent">
          <div className="stat-icon">🚨</div>
          <div className="stat-content">
            <h3>Fraudulent</h3>
            <p className="stat-value">{fraudulent_count}</p>
            <p className="stat-percent">{fraud_rate.toFixed(1)}%</p>
          </div>
        </div>
      </div>

      {/* Chart */}
      <div className="chart-container">
        <h3>📊 Ticket Validation Breakdown</h3>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={chartData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
              outerRadius={100}
              fill="#8884d8"
              dataKey="value"
            >
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default Summary;
