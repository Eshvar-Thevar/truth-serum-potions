"""
Debug: Check the actual fraud distribution and witch scores
"""

import requests
from fraud_detector import FraudDetector

data_response = requests.get("https://hackutd2025.eog.systems/api/Data/?start_date=0&end_date=2000000000")
historical_data = data_response.json()

tickets_response = requests.get("https://hackutd2025.eog.systems/api/Tickets")
tickets = tickets_response.json()['transport_tickets']

detector = FraudDetector(historical_data, tickets)
analysis = detector.analyze_all_tickets()

print("🔍 FRAUD DETECTION ANALYSIS\n")
print("="*70)
print(f"Total tickets: {analysis['summary']['total_tickets']}")
print(f"Valid: {analysis['summary']['valid_count']} ({analysis['summary']['valid_count']/analysis['summary']['total_tickets']*100:.1f}%)")
print(f"Suspicious: {analysis['summary']['suspicious_count']} ({analysis['summary']['suspicious_count']/analysis['summary']['total_tickets']*100:.1f}%)")
print(f"Fraudulent: {analysis['summary']['fraudulent_count']} ({analysis['summary']['fraudulent_count']/analysis['summary']['total_tickets']*100:.1f}%)")

print("\n" + "="*70)
print("WITCH TRUST SCORES:")
print("="*70)
for witch in analysis['witch_trust_scores']:
    print(f"\n{witch['courier_id']}:")
    print(f"  Trust: {witch['trust_score']}/100")
    print(f"  Tickets: {witch['total_tickets']}")
    print(f"  Valid: {witch['valid_tickets']}")
    print(f"  Suspicious: {witch['suspicious_tickets']}")
    print(f"  Fraudulent: {witch['fraudulent_tickets']}")
    print(f"  Accuracy: {witch['accuracy_percent']:.1f}%")

print("\n" + "="*70)
print("SAMPLE TICKETS BY STATUS:")
print("="*70)

# Show examples of each status
valid_samples = [t for t in analysis['tickets'] if t['status'] == 'valid'][:3]
suspicious_samples = [t for t in analysis['tickets'] if t['status'] == 'suspicious'][:3]
fraudulent_samples = [t for t in analysis['tickets'] if t['status'] == 'fraudulent'][:3]

print("\n✅ VALID SAMPLES:")
for t in valid_samples:
    print(f"  {t['ticket_id']}: Reported {t['reported_amount']:.2f} | Expected {t['expected_amount']:.2f} | Error: {t['percent_error']:.1f}%")

print("\n🟡 SUSPICIOUS SAMPLES:")
for t in suspicious_samples:
    print(f"  {t['ticket_id']}: Reported {t['reported_amount']:.2f} | Expected {t['expected_amount']:.2f} | Error: {t['percent_error']:.1f}%")

print("\n🚨 FRAUDULENT SAMPLES:")
for t in fraudulent_samples:
    print(f"  {t['ticket_id']}: Reported {t['reported_amount']:.2f} | Expected {t['expected_amount']:.2f} | Error: {t['percent_error']:.1f}%")

print("\n" + "="*70)
print("ERROR DISTRIBUTION:")
print("="*70)
errors = [t['percent_error'] for t in analysis['tickets']]
import numpy as np
print(f"Min error: {min(errors):.1f}%")
print(f"Max error: {max(errors):.1f}%")
print(f"Average error: {np.mean(errors):.1f}%")
print(f"Median error: {np.median(errors):.1f}%")

# Count by error ranges
under_7 = sum(1 for e in errors if e < 7)
between_7_15 = sum(1 for e in errors if 7 <= e < 15)
over_15 = sum(1 for e in errors if e >= 15)

print(f"\nError < 7% (valid): {under_7}")
print(f"Error 7-15% (suspicious): {between_7_15}")
print(f"Error > 15% (fraudulent): {over_15}")
