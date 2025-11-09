"""
🔮 NEW APPROACH: Daily Drain Analysis
Instead of matching individual tickets to drain events,
analyze the entire day's drainage and compare to total tickets for that day.
"""

import requests
from datetime import datetime
from collections import defaultdict

print("🔍 NEW APPROACH: Daily Drain Analysis\n")

# Get data
data_response = requests.get("https://hackutd2025.eog.systems/api/Data/?start_date=0&end_date=2000000000")
historical_data = data_response.json()

tickets_response = requests.get("https://hackutd2025.eog.systems/api/Tickets")
tickets = tickets_response.json()['transport_tickets']

print(f"✅ Got {len(historical_data)} data points")
print(f"✅ Got {len(tickets)} tickets\n")

# Group tickets by cauldron and date
tickets_by_cauldron_date = defaultdict(list)
for ticket in tickets:
    key = (ticket['cauldron_id'], ticket['date'])
    tickets_by_cauldron_date[key].append(ticket)

print("="*70)
print("ANALYZING FIRST DAY FOR CAULDRON_012:")
print("="*70)

cauldron_id = "cauldron_012"
date_str = "2025-10-30"
target_date = datetime.fromisoformat(date_str).date()

# Get all levels for this day
day_data = []
for entry in historical_data:
    timestamp = datetime.fromisoformat(entry['timestamp'].replace('Z', '+00:00'))
    if timestamp.date() == target_date:
        level = entry['cauldron_levels'][cauldron_id]
        day_data.append({
            'time': timestamp.strftime('%H:%M'),
            'level': level
        })

# Find peak and valley
levels = [d['level'] for d in day_data]
peak_level = max(levels)
valley_level = min(levels)
peak_idx = levels.index(peak_level)
valley_idx = levels.index(valley_level)

print(f"\nPeak: {peak_level:.2f} units at {day_data[peak_idx]['time']}")
print(f"Valley: {valley_level:.2f} units at {day_data[valley_idx]['time']}")
print(f"Total visible drain: {peak_level - valley_level:.2f} units")

# Calculate drain duration
if valley_idx > peak_idx:
    drain_duration = valley_idx - peak_idx  # minutes
    print(f"Drain duration: {drain_duration} minutes")
    
    # Calculate fill rate (estimate: 0.1 units/min for cauldron_012)
    fill_rate = 0.10
    inflow_during_drain = fill_rate * drain_duration
    
    print(f"Fill rate: {fill_rate:.2f} units/min")
    print(f"Inflow during drain: {inflow_during_drain:.2f} units")
    print(f"\n💡 TOTAL COLLECTED (expected): {(peak_level - valley_level) + inflow_during_drain:.2f} units")

# Check tickets for this day
key = (cauldron_id, date_str)
day_tickets = tickets_by_cauldron_date[key]

print(f"\n📋 Tickets for this cauldron on this day:")
total_reported = sum(t['amount_collected'] for t in day_tickets)
for ticket in day_tickets:
    print(f"  {ticket['ticket_id']}: {ticket['amount_collected']:.2f} units ({ticket['courier_id']})")

print(f"\n📊 TOTAL REPORTED: {total_reported:.2f} units")
print(f"📊 TOTAL EXPECTED: {(peak_level - valley_level) + inflow_during_drain:.2f} units")
print(f"📊 DIFFERENCE: {total_reported - ((peak_level - valley_level) + inflow_during_drain):.2f} units")

print("\n" + "="*70)
print("💡 INSIGHT:")
print("="*70)
print("Maybe we should compare DAILY TOTALS instead of individual tickets?")
print("Sum all tickets per day/cauldron and compare to total drainage.")
