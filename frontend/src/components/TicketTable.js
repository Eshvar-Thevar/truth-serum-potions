import React, { useState } from 'react';
import './TicketTable.css';

function TicketTable({ tickets, compact = false }) {
  const [filter, setFilter] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');

  // Filter tickets
  let filteredTickets = tickets;
  
  if (filter !== 'all') {
    filteredTickets = tickets.filter(ticket => ticket.status === filter);
  }
  
  if (searchTerm) {
    filteredTickets = filteredTickets.filter(ticket => 
      ticket.ticket_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
      ticket.cauldron_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
      ticket.courier_id.toLowerCase().includes(searchTerm.toLowerCase())
    );
  }

  const displayTickets = compact ? filteredTickets.slice(0, 5) : filteredTickets;

  const getStatusBadge = (status) => {
    const badges = {
      valid: { emoji: '✅', class: 'status-valid', text: 'Valid' },
      suspicious: { emoji: '🟡', class: 'status-suspicious', text: 'Suspicious' },
      fraudulent: { emoji: '🚨', class: 'status-fraudulent', text: 'FRAUD' }
    };
    const badge = badges[status] || badges.valid;
    return (
      <span className={`status-badge ${badge.class}`}>
        {badge.emoji} {badge.text}
      </span>
    );
  };

  return (
    <div className={`ticket-table-container ${compact ? 'compact' : ''}`}>
      {!compact && (
        <div className="table-controls">
          <div className="filter-buttons">
            <button 
              className={filter === 'all' ? 'active' : ''} 
              onClick={() => setFilter('all')}
            >
              All ({tickets.length})
            </button>
            <button 
              className={filter === 'valid' ? 'active' : ''} 
              onClick={() => setFilter('valid')}
            >
              ✅ Valid ({tickets.filter(t => t.status === 'valid').length})
            </button>
            <button 
              className={filter === 'suspicious' ? 'active' : ''} 
              onClick={() => setFilter('suspicious')}
            >
              🟡 Suspicious ({tickets.filter(t => t.status === 'suspicious').length})
            </button>
            <button 
              className={filter === 'fraudulent' ? 'active' : ''} 
              onClick={() => setFilter('fraudulent')}
            >
              🚨 Fraudulent ({tickets.filter(t => t.status === 'fraudulent').length})
            </button>
          </div>
          
          <input
            type="text"
            placeholder="🔍 Search tickets..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
        </div>
      )}

      <div className="table-wrapper">
        <table className="ticket-table">
          <thead>
            <tr>
              <th>Ticket ID</th>
              <th>Cauldron</th>
              <th>Witch</th>
              <th>Date</th>
              <th>Reported</th>
              <th>Expected</th>
              <th>Diff</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {displayTickets.map((ticket) => (
              <tr key={ticket.ticket_id} className={`row-${ticket.status}`}>
                <td className="ticket-id">{ticket.ticket_id}</td>
                <td>{ticket.cauldron_id.replace('cauldron_', 'C')}</td>
                <td>{ticket.courier_id.replace('courier_witch_', 'Witch ')}</td>
                <td>{ticket.date}</td>
                <td className="amount">{ticket.reported_amount.toFixed(2)}</td>
                <td className="amount">{ticket.expected_amount.toFixed(2)}</td>
                <td className={`diff ${ticket.difference > 0 ? 'positive' : 'negative'}`}>
                  {ticket.difference > 0 ? '+' : ''}{ticket.difference.toFixed(2)}
                </td>
                <td>{getStatusBadge(ticket.status)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {!compact && (
        <div className="table-footer">
          <p>Showing {displayTickets.length} of {tickets.length} tickets</p>
        </div>
      )}
    </div>
  );
}

export default TicketTable;
