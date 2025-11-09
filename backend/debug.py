"""
Debug script to check what's happening with the fraud detection
"""

import requests
import json
from datetime import datetime

# Fetch some data
print("🔍 Fetching data from API...")

# Get historical data (just first 100 points to see)
data_response = requests.get("https://hackutd2025.eog.systems/api/Data/?start_date=0&end_date=1762629770")
historical_data = data_response.json()[:100]  # Just first 100 for speed

# Get tickets
tickets_response = requests.get("https://hackutd2025.eog.systems/api/Tickets")
tickets_data = tickets_response.json()
tickets = tickets_data['transport_tickets'][:5]  # Just first 5

print(f"\n✅ Got {len(historical_data)} data points")
print(f"✅ Got {len(tickets)} sample tickets\n")

# Check a specific ticket
print("="*60)
print("ANALYZING FIRST TICKET:")
print("="*60)

ticket = tickets[0]
print(f"Ticket ID: {ticket['ticket_id']}")
print(f"Cauldron: {ticket['cauldron_id']}")
print(f"Reported Amount: {ticket['amount_collected']}")
print(f"Date: {ticket['date']}")
print(f"Witch: {ticket['courier_id']}")

# Check cauldron levels on that date
target_date = datetime.fromisoformat(ticket['date']).date()
print(f"\nLooking for data on: {target_date}")

# Filter data for that cauldron and date
cauldron_id = ticket['cauldron_id']
day_levels = []

for entry in historical_data:
    timestamp = datetime.fromisoformat(entry['timestamp'].replace('Z', '+00:00'))
    if timestamp.date() == target_date:
        level = entry['cauldron_levels'].get(cauldron_id, 0)
        day_levels.append({
            'time': timestamp.strftime('%H:%M:%S'),
            'level': level
        })

if day_levels:
    print(f"\n✅ Found {len(day_levels)} data points for this cauldron on this date")
    print("\nFirst 10 levels:")
    for i, d in enumerate(day_levels[:10]):
        print(f"  {d['time']}: {d['level']:.2f} units")
    
    # Check for drops
    print("\nLooking for level drops (drains)...")
    for i in range(len(day_levels) - 1):
        current = day_levels[i]['level']
        next_level = day_levels[i+1]['level']
        drop = current - next_level
        
        if drop > 5:
            print(f"  🔽 DROP FOUND at {day_levels[i]['time']}: {current:.2f} → {next_level:.2f} (dropped {drop:.2f} units)")
else:
    print(f"\n❌ NO DATA FOUND for {cauldron_id} on {target_date}")
    print("This might be why everything shows as valid!")

print("\n" + "="*60)
print("CHECKING ALL TICKETS' DATES:")
print("="*60)

# Check which dates have data
dates_in_data = set()
for entry in historical_data:
    timestamp = datetime.fromisoformat(entry['timestamp'].replace('Z', '+00:00'))
    dates_in_data.add(timestamp.date())

print(f"\nDates with data: {sorted(dates_in_data)}")

ticket_dates = set()
for ticket in tickets:
    ticket_date = datetime.fromisoformat(ticket['date']).date()
    ticket_dates.add(ticket_date)

print(f"Dates in tickets: {sorted(ticket_dates)}")

overlap = dates_in_data.intersection(ticket_dates)
print(f"\nDates that overlap: {sorted(overlap)}")

if not overlap:
    print("\n❌ PROBLEM FOUND: No overlap between ticket dates and data dates!")
    print("This is why everything shows as valid - we have no data to check against!")
