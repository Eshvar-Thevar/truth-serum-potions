"""
Debug script - GET MORE DATA
"""

import requests
import json
from datetime import datetime

print("🔍 Fetching MORE data from API...")

# Get MUCH more historical data - full week
data_response = requests.get("https://hackutd2025.eog.systems/api/Data/?start_date=0&end_date=2000000000")
historical_data = data_response.json()

print(f"✅ Got {len(historical_data)} total data points")

# Get tickets
tickets_response = requests.get("https://hackutd2025.eog.systems/api/Tickets")
tickets_data = tickets_response.json()
tickets = tickets_data['transport_tickets'][:5]

print(f"✅ Got {len(tickets)} sample tickets\n")

# Check first ticket with FULL day data
ticket = tickets[0]
print("="*60)
print("ANALYZING FIRST TICKET (WITH FULL DAY DATA):")
print("="*60)
print(f"Ticket ID: {ticket['ticket_id']}")
print(f"Cauldron: {ticket['cauldron_id']}")
print(f"Reported Amount: {ticket['amount_collected']}")
print(f"Date: {ticket['date']}")

# Get ALL data for this cauldron on this date
target_date = datetime.fromisoformat(ticket['date']).date()
cauldron_id = ticket['cauldron_id']

day_data = []
for entry in historical_data:
    timestamp = datetime.fromisoformat(entry['timestamp'].replace('Z', '+00:00'))
    if timestamp.date() == target_date:
        level = entry['cauldron_levels'].get(cauldron_id, 0)
        day_data.append({
            'time': timestamp.strftime('%H:%M:%S'),
            'timestamp': timestamp,
            'level': level
        })

print(f"\n✅ Found {len(day_data)} data points for ENTIRE day")

# Look for BIGGEST drops
print("\n🔍 Looking for drain events (level drops > 5 units)...")
drains_found = []

for i in range(len(day_data) - 1):
    current = day_data[i]['level']
    next_level = day_data[i+1]['level']
    drop = current - next_level
    
    if drop > 5:
        drains_found.append({
            'time': day_data[i]['time'],
            'before': current,
            'after': next_level,
            'drop': drop
        })
        print(f"  🔽 DRAIN at {day_data[i]['time']}: {current:.2f} → {next_level:.2f} (dropped {drop:.2f} units)")

if not drains_found:
    print("  ❌ NO DRAINS DETECTED with threshold > 5 units")
    print("\n  Let's check smaller drops (> 1 unit):")
    
    for i in range(len(day_data) - 1):
        current = day_data[i]['level']
        next_level = day_data[i+1]['level']
        drop = current - next_level
        
        if drop > 1:
            print(f"    Small drop at {day_data[i]['time']}: {current:.2f} → {next_level:.2f} (dropped {drop:.2f})")
            if len([d for d in day_data if d['time'] <= day_data[i+1]['time'] and current - d['level'] > 1]) > 5:
                break  # Only show first few

print("\n" + "="*60)
print(f"Expected collection: ~{ticket['amount_collected']} units")
print(f"Biggest drop found: {max([d['drop'] for d in drains_found]) if drains_found else 0:.2f} units")
print("="*60)

# Show level range
levels = [d['level'] for d in day_data]
print(f"\nLevel range for day: {min(levels):.2f} to {max(levels):.2f} units")
print(f"Total change: {max(levels) - min(levels):.2f} units")
