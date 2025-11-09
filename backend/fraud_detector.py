"""
🔮 FRAUD DETECTOR - VERY BALANCED THRESHOLDS AND PENALTIES
Realistic fraud detection with fair, lenient trust scoring
"""

from typing import Dict, List
from data_processor import DataProcessor
from datetime import datetime
from collections import defaultdict

class FraudDetector:
    """Detects fraudulent transport tickets by comparing them with actual drain events"""
    
    def __init__(self, historical_data: List[Dict], tickets: List[Dict]):
        self.processor = DataProcessor(historical_data)
        self.tickets = tickets
        self.cauldron_fill_rates = {}
        
        # Pre-calculate fill rates
        for cauldron_id in self.processor.cauldron_ids:
            self.cauldron_fill_rates[cauldron_id] = self.processor.calculate_fill_rate(cauldron_id)
        
        # Group tickets by cauldron and date
        self.tickets_by_cauldron_date = defaultdict(list)
        for ticket in tickets:
            key = (ticket['cauldron_id'], ticket['date'])
            self.tickets_by_cauldron_date[key].append(ticket)
    
    def validate_ticket(self, ticket: Dict) -> Dict:
        """
        Validate a ticket against the ACTUAL daily drain.
        Uses LENIENT thresholds: 10% / 25% 
        """
        cauldron_id = ticket['cauldron_id']
        reported_amount = ticket['amount_collected']
        date = ticket['date']
        
        fill_rate = self.cauldron_fill_rates.get(cauldron_id, 0.1)
        
        # Get THE actual drain for this day
        daily_drain = self.processor.get_daily_drain(cauldron_id, date)
        
        if daily_drain is None:
            # No drain detected
            if reported_amount <= 100:
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
                    'reason': 'No significant drain detected, amount reasonable',
                    'fill_rate_used': fill_rate,
                    'tickets_this_day': 1
                }
            else:
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
                    'reason': f'Exceeds capacity ({reported_amount:.1f} > 100)',
                    'fill_rate_used': fill_rate,
                    'tickets_this_day': 1
                }
        
        # Calculate total expected from ACTUAL drain
        expected_total = self.processor.calculate_expected_collection(cauldron_id, daily_drain, fill_rate)
        
        # Check how many tickets exist for this day/cauldron
        key = (cauldron_id, date)
        day_tickets = self.tickets_by_cauldron_date[key]
        num_tickets = len(day_tickets)
        
        # Divide expected amount by number of tickets
        expected_amount = expected_total / num_tickets
        
        difference = reported_amount - expected_amount
        percent_error = abs(difference / expected_amount * 100) if expected_amount > 0 else 100
        
        # LENIENT THRESHOLDS: 10% / 25%
        if percent_error < 10:
            status = 'valid'
            reason = f'Matches expected share (±{percent_error:.1f}%)'
            if num_tickets > 1:
                reason += f' [{num_tickets} witches this day]'
        elif percent_error < 25:  # Was 18%, now 25%
            status = 'suspicious'
            if difference > 0:
                reason = f'Over-reported by {difference:.2f} units (+{percent_error:.1f}%)'
            else:
                reason = f'Under-reported by {abs(difference):.2f} units (-{percent_error:.1f}%)'
            if num_tickets > 1:
                reason += f' [{num_tickets} witches this day]'
        else:  # >= 25%
            status = 'fraudulent'
            if difference > 0:
                reason = f'FRAUD: Over-reported by {difference:.2f} units (+{percent_error:.1f}%)'
            else:
                reason = f'FRAUD: Under-reported by {abs(difference):.2f} units (-{percent_error:.1f}%)'
            if num_tickets > 1:
                reason += f' [{num_tickets} witches this day]'
        
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
                'start_time': daily_drain['start_time'].isoformat(),
                'end_time': daily_drain['end_time'].isoformat(),
                'duration_minutes': daily_drain['duration_minutes'],
                'visible_drain': daily_drain['drain_amount'],
                'total_expected': expected_total
            },
            'reason': reason,
            'fill_rate_used': fill_rate,
            'tickets_this_day': num_tickets
        }
    
    def analyze_all_tickets(self) -> Dict:
        """Analyze all tickets"""
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
        Calculate trust scores with VERY LIGHT PENALTIES
        Suspicious: -2 (was -3)
        Fraudulent: -8 (was -15)
        """
        witch_data = {}
        
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
        
        for ticket in validated_tickets:
            witch_id = ticket['courier_id']
            witch_data[witch_id]['total_tickets'] += 1
            
            if ticket['status'] == 'valid':
                witch_data[witch_id]['valid_tickets'] += 1
            elif ticket['status'] == 'suspicious':
                witch_data[witch_id]['suspicious_tickets'] += 1
                witch_data[witch_id]['trust_score'] -= 2  # Was -3, now -2
                witch_data[witch_id]['total_fraud_amount'] += abs(ticket['difference'])
            elif ticket['status'] == 'fraudulent':
                witch_data[witch_id]['fraudulent_tickets'] += 1
                witch_data[witch_id]['trust_score'] -= 8  # Was -15, now -8
                witch_data[witch_id]['total_fraud_amount'] += abs(ticket['difference'])
        
        for witch_id in witch_data:
            witch_data[witch_id]['trust_score'] = max(0, witch_data[witch_id]['trust_score'])
            total = witch_data[witch_id]['total_tickets']
            valid = witch_data[witch_id]['valid_tickets']
            witch_data[witch_id]['accuracy_percent'] = (valid / total * 100) if total > 0 else 0
        
        witch_list = list(witch_data.values())
        witch_list.sort(key=lambda x: x['trust_score'])
        
        return witch_list
