"""
Debug: Check for tickets over 100 units and fill rates
"""

import requests

print("🔍 Checking for issues with tickets and fill rates...\n")

# Get tickets
tickets_response = requests.get("https://hackutd2025.eog.systems/api/Tickets")
tickets = tickets_response.json()['transport_tickets']

print(f"Total tickets: {len(tickets)}\n")

# Check for tickets over 100
over_100 = [t for t in tickets if t['amount_collected'] > 100]

print("="*60)
print("TICKETS OVER 100 UNITS (IMPOSSIBLE!):")
print("="*60)
if over_100:
    for ticket in over_100[:10]:  # Show first 10
        print(f"{ticket['ticket_id']}: {ticket['amount_collected']:.2f} units - {ticket['cauldron_id']} - {ticket['courier_id']}")
    print(f"\nTotal: {len(over_100)} tickets over 100 units!")
else:
    print("✅ No tickets over 100 units found")

print("\n" + "="*60)
print("CHECKING FILL RATES PER CAULDRON:")
print("="*60)

# Get data and calculate fill rates
from data_processor import DataProcessor

data_response = requests.get("https://hackutd2025.eog.systems/api/Data/?start_date=0&end_date=2000000000")
historical_data = data_response.json()

processor = DataProcessor(historical_data)

for cauldron_id in processor.cauldron_ids:
    fill_rate = processor.calculate_fill_rate(cauldron_id)
    print(f"{cauldron_id}: {fill_rate:.4f} units/min")
