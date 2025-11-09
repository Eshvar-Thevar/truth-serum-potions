"""
Check if any EXPECTED amounts are unrealistically high
"""

import requests
from fraud_detector import FraudDetector

print("🔍 Checking for unrealistic expected amounts...\n")

# Get data
data_response = requests.get("https://hackutd2025.eog.systems/api/Data/?start_date=0&end_date=2000000000")
historical_data = data_response.json()

tickets_response = requests.get("https://hackutd2025.eog.systems/api/Tickets")
tickets = tickets_response.json()['transport_tickets']

# Run fraud detection
detector = FraudDetector(historical_data, tickets)
analysis = detector.analyze_all_tickets()

print(f"Total tickets analyzed: {len(analysis['tickets'])}\n")

# Find tickets where expected > 100
high_expected = [t for t in analysis['tickets'] if t['expected_amount'] > 100]

print("="*60)
print("TICKETS WITH EXPECTED AMOUNT > 100:")
print("="*60)

if high_expected:
    for ticket in high_expected[:10]:
        print(f"\n{ticket['ticket_id']}:")
        print(f"  Cauldron: {ticket['cauldron_id']}")
        print(f"  Reported: {ticket['reported_amount']:.2f} units")
        print(f"  Expected: {ticket['expected_amount']:.2f} units ⚠️")
        print(f"  Status: {ticket['status']}")
        if ticket['matched_drain']:
            print(f"  Drain duration: {ticket['matched_drain']['duration_minutes']:.1f} minutes")
            print(f"  Visible drain: {ticket['matched_drain']['visible_drain']:.2f} units")
            print(f"  Fill rate: {ticket['fill_rate_used']:.4f} units/min")
    
    print(f"\n⚠️ Found {len(high_expected)} tickets with expected > 100!")
    print("This suggests our drain detection is catching too long of a period.")
else:
    print("✅ All expected amounts are under 100 units - calculations look good!")

# Show some normal tickets for comparison
print("\n" + "="*60)
print("SAMPLE OF NORMAL TICKETS:")
print("="*60)

normal = [t for t in analysis['tickets'] if t['expected_amount'] <= 100][:5]
for ticket in normal:
    print(f"\n{ticket['ticket_id']}:")
    print(f"  Reported: {ticket['reported_amount']:.2f} | Expected: {ticket['expected_amount']:.2f}")
    print(f"  Status: {ticket['status']}")
