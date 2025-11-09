"""
Debug: Check if division is working for multi-ticket days
"""

import requests
from fraud_detector import FraudDetector

data_response = requests.get("https://hackutd2025.eog.systems/api/Data/?start_date=0&end_date=2000000000")
historical_data = data_response.json()

tickets_response = requests.get("https://hackutd2025.eog.systems/api/Tickets")
tickets = tickets_response.json()['transport_tickets']

detector = FraudDetector(historical_data, tickets)

# Check tickets 14 and 15 specifically
target_tickets = ['TT_20251030_014', 'TT_20251030_015']

print("🔍 Checking if division is working for multi-ticket days\n")
print("="*70)

for ticket_id in target_tickets:
    ticket = next(t for t in tickets if t['ticket_id'] == ticket_id)
    validation = detector.validate_ticket(ticket)
    
    print(f"\n{validation['ticket_id']}:")
    print(f"  Cauldron: {validation['cauldron_id']}")
    print(f"  Date: {validation['date']}")
    print(f"  Tickets this day: {validation['tickets_this_day']}")
    print(f"  Total drain expected: {validation['matched_drain']['total_expected']:.2f} units")
    print(f"  Expected per ticket (÷{validation['tickets_this_day']}): {validation['expected_amount']:.2f} units")
    print(f"  Reported: {validation['reported_amount']:.2f} units")
    print(f"  Status: {validation['status']}")

print("\n" + "="*70)
print("Is division happening? Let's check the math:")
print(f"Total expected: {validation['matched_drain']['total_expected']:.2f}")
print(f"Number of tickets: {validation['tickets_this_day']}")
print(f"Expected per ticket: {validation['matched_drain']['total_expected'] / validation['tickets_this_day']:.2f}")
print(f"Actual expected in result: {validation['expected_amount']:.2f}")
print("Match? ", abs(validation['expected_amount'] - validation['matched_drain']['total_expected'] / validation['tickets_this_day']) < 0.01)
