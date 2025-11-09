"""
🔮 FRAUD DETECTOR
This is the core algorithm that catches dishonest witches!
"""

from typing import Dict, List
from data_processor import DataProcessor
from datetime import datetime

class FraudDetector:
    """Detects fraudulent transport tickets by comparing them with actual drain events"""
    
    def __init__(self, historical_data: List[Dict], tickets: List[Dict]):
        """
        Initialize the fraud detector
        
        Args:
            historical_data: Historical cauldron level data from API
            tickets: Transport tickets from API
        """
        self.processor = DataProcessor(historical_data)
        self.tickets = tickets
        self.cauldron_fill_rates = {}
        
        # Pre-calculate fill rates for all cauldrons
        for cauldron_id in self.processor.cauldron_ids:
            self.cauldron_fill_rates[cauldron_id] = self.processor.calculate_fill_rate(cauldron_id)
    
    def validate_ticket(self, ticket: Dict) -> Dict:
        """
        Validate a single transport ticket
        
        Args:
            ticket: Ticket dictionary with ticket_id, cauldron_id, amount_collected, courier_id, date
            
        Returns:
            Validation result
        """
        cauldron_id = ticket['cauldron_id']
        reported_amount = ticket['amount_collected']
        date = ticket['date']
        
        # Get fill rate for this cauldron
        fill_rate = self.cauldron_fill_rates.get(cauldron_id, 0.1)
        
        # Detect drain events on this date
        drain_events = self.processor.detect_drain_events(cauldron_id, date)
        
        # If no drain detected, check if amount is reasonable
        if not drain_events:
            if reported_amount <= 100:  # Within witch capacity
                # Assume valid - drain detection may have missed small drains
                return {
                    'ticket_id': ticket['ticket_id'],
                    'cauldron_id': cauldron_id,
                    'courier_id': ticket['courier_id'],
                    'date': date,
                    'reported_amount': reported_amount,
                    'expected_amount': reported_amount,
                    'difference': 0,
                    'percent_error': 0,
                    'status': 'valid',
                    'matched_drain': None,
                    'reason': 'Amount within reasonable limits (no drain detected in data)',
                    'fill_rate_used': fill_rate
                }
            else:
                # Exceeds capacity - definitely fraud
                return {
                    'ticket_id': ticket['ticket_id'],
                    'cauldron_id': cauldron_id,
                    'courier_id': ticket['courier_id'],
                    'date': date,
                    'reported_amount': reported_amount,
                    'expected_amount': 100,
                    'difference': reported_amount - 100,
                    'percent_error': (reported_amount - 100) / 100 * 100,
                    'status': 'fraudulent',
                    'matched_drain': None,
                    'reason': f'Exceeds witch capacity! Reported {reported_amount:.1f} units (max is 100)',
                    'fill_rate_used': fill_rate
                }
        
        # Find best matching drain
        best_match = None
        min_error = float('inf')
        
        for drain in drain_events:
            expected = self.processor.calculate_expected_collection(cauldron_id, drain, fill_rate)
            error = abs(expected - reported_amount)
            
            if error < min_error:
                min_error = error
                best_match = drain
        
        # Calculate expected amount
        expected_amount = self.processor.calculate_expected_collection(
            cauldron_id, 
            best_match, 
            fill_rate
        )
        
        difference = reported_amount - expected_amount
        percent_error = abs(difference / expected_amount * 100) if expected_amount > 0 else 100
        
        # BALANCED THRESHOLDS - catch real fraud but allow measurement error
        if percent_error < 7:  # Within 7% - VALID (allows for measurement error)
            status = 'valid'
            reason = f'Reported amount matches expected (±{percent_error:.1f}%)'
        elif percent_error < 15:  # 7-15% difference - SUSPICIOUS
            status = 'suspicious'
            if difference > 0:
                reason = f'Over-reported by {difference:.2f} units (+{percent_error:.1f}%) - suspicious'
            else:
                reason = f'Under-reported by {abs(difference):.2f} units (-{percent_error:.1f}%) - suspicious'
        else:  # > 15% difference - FRAUDULENT
            status = 'fraudulent'
            if difference > 0:
                reason = f'FRAUD: Over-reported by {difference:.2f} units (+{percent_error:.1f}%) - likely stealing!'
            else:
                reason = f'FRAUD: Under-reported by {abs(difference):.2f} units (-{percent_error:.1f}%) - likely hoarding!'
        
        return {
            'ticket_id': ticket['ticket_id'],
            'cauldron_id': cauldron_id,
            'courier_id': ticket['courier_id'],
            'date': date,
            'reported_amount': reported_amount,
            'expected_amount': expected_amount,
            'difference': difference,
            'percent_error': percent_error,
            'status': status,
            'matched_drain': {
                'start_time': best_match['start_time'].isoformat(),
                'end_time': best_match['end_time'].isoformat(),
                'duration_minutes': best_match['duration_minutes'],
                'visible_drain': best_match['drain_amount']
            } if best_match else None,
            'reason': reason,
            'fill_rate_used': fill_rate
        }
    
    def analyze_all_tickets(self) -> Dict:
        """
        Analyze all tickets and generate a comprehensive fraud report
        """
        results = []
        
        for ticket in self.tickets:
            validation = self.validate_ticket(ticket)
            results.append(validation)
        
        # Calculate statistics
        total_tickets = len(results)
        valid_tickets = [r for r in results if r['status'] == 'valid']
        suspicious_tickets = [r for r in results if r['status'] == 'suspicious']
        fraudulent_tickets = [r for r in results if r['status'] == 'fraudulent']
        
        # Calculate witch trust scores
        witch_scores = self.calculate_witch_trust_scores(results)
        
        return {
            'summary': {
                'total_tickets': total_tickets,
                'valid_count': len(valid_tickets),
                'suspicious_count': len(suspicious_tickets),
                'fraudulent_count': len(fraudulent_tickets),
                'fraud_rate': (len(fraudulent_tickets) / total_tickets * 100) if total_tickets > 0 else 0
            },
            'tickets': results,
            'witch_trust_scores': witch_scores,
            'cauldron_fill_rates': self.cauldron_fill_rates,
            'flagged_tickets': suspicious_tickets + fraudulent_tickets
        }
    
    def calculate_witch_trust_scores(self, validated_tickets: List[Dict]) -> Dict:
        """
        Calculate trust scores for each witch
        """
        witch_data = {}
        
        # Initialize all witches with 100 trust
        witch_ids = set(ticket['courier_id'] for ticket in validated_tickets)
        for witch_id in witch_ids:
            witch_data[witch_id] = {
                'courier_id': witch_id,
                'trust_score': 100,
                'total_tickets': 0,
                'valid_tickets': 0,
                'suspicious_tickets': 0,
                'fraudulent_tickets': 0,
                'total_fraud_amount': 0
            }
        
        # Update scores based on ticket validation
        for ticket in validated_tickets:
            witch_id = ticket['courier_id']
            witch_data[witch_id]['total_tickets'] += 1
            
            if ticket['status'] == 'valid':
                witch_data[witch_id]['valid_tickets'] += 1
            elif ticket['status'] == 'suspicious':
                witch_data[witch_id]['suspicious_tickets'] += 1
                witch_data[witch_id]['trust_score'] -= 5
                witch_data[witch_id]['total_fraud_amount'] += abs(ticket['difference'])
            elif ticket['status'] == 'fraudulent':
                witch_data[witch_id]['fraudulent_tickets'] += 1
                witch_data[witch_id]['trust_score'] -= 20
                witch_data[witch_id]['total_fraud_amount'] += abs(ticket['difference'])
        
        # Ensure trust score doesn't go below 0
        for witch_id in witch_data:
            witch_data[witch_id]['trust_score'] = max(0, witch_data[witch_id]['trust_score'])
            
            # Calculate accuracy percentage
            total = witch_data[witch_id]['total_tickets']
            valid = witch_data[witch_id]['valid_tickets']
            witch_data[witch_id]['accuracy_percent'] = (valid / total * 100) if total > 0 else 0
        
        # Convert to list and sort by trust score (worst first)
        witch_list = list(witch_data.values())
        witch_list.sort(key=lambda x: x['trust_score'])
        
        return witch_list
