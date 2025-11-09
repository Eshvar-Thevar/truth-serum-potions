"""
Test the NEW drain detection algorithm
"""

import requests
from data_processor import DataProcessor
from datetime import datetime

print("🔍 Testing NEW drain detection algorithm...")

# Get data
data_response = requests.get("https://hackutd2025.eog.systems/api/Data/?start_date=0&end_date=2000000000")
historical_data = data_response.json()

# Get tickets
tickets_response = requests.get("https://hackutd2025.eog.systems/api/Tickets")
tickets = tickets_response.json()['transport_tickets'][:5]

print(f"✅ Got {len(historical_data)} data points")
print(f"✅ Got {len(tickets)} tickets\n")

# Create processor
processor = DataProcessor(historical_data)

# Test on first ticket
ticket = tickets[0]
print("="*60)
print("TESTING FIRST TICKET:")
print("="*60)
print(f"Ticket: {ticket['ticket_id']}")
print(f"Cauldron: {ticket['cauldron_id']}")
print(f"Date: {ticket['date']}")
print(f"Reported: {ticket['amount_collected']} units")

# Detect drains
drains = processor.detect_drain_events(ticket['cauldron_id'], ticket['date'])

print(f"\n🔍 Drains detected: {len(drains)}")

if drains:
    for i, drain in enumerate(drains):
        print(f"\nDrain #{i+1}:")
        print(f"  Start: {drain['start_time'].strftime('%H:%M:%S')} at {drain['start_level']:.2f} units")
        print(f"  End: {drain['end_time'].strftime('%H:%M:%S')} at {drain['end_level']:.2f} units")
        print(f"  Visible drain: {drain['drain_amount']:.2f} units")
        print(f"  Duration: {drain['duration_minutes']:.1f} minutes")
        
        # Calculate expected
        fill_rate = processor.calculate_fill_rate(ticket['cauldron_id'])
        expected = processor.calculate_expected_collection(ticket['cauldron_id'], drain, fill_rate)
        
        print(f"  Fill rate: {fill_rate:.3f} units/min")
        print(f"  Inflow during drain: {fill_rate * drain['duration_minutes']:.2f} units")
        print(f"  Expected collection: {expected:.2f} units")
        print(f"  Reported: {ticket['amount_collected']:.2f} units")
        print(f"  Difference: {ticket['amount_collected'] - expected:.2f} units")
        
        percent_error = abs(ticket['amount_collected'] - expected) / expected * 100
        print(f"  Error: {percent_error:.1f}%")
        
        if percent_error < 7:
            print(f"  ✅ VALID")
        elif percent_error < 15:
            print(f"  🟡 SUSPICIOUS")
        else:
            print(f"  🚨 FRAUDULENT")
else:
    print("  ❌ No drains detected!")

print("\n" + "="*60)
