"""
Verify that we're using REAL data, not made-up numbers
"""

import requests
from data_processor import DataProcessor

print("🔍 VERIFICATION: Are we using real data?\n")

# Get data
data_response = requests.get("https://hackutd2025.eog.systems/api/Data/?start_date=0&end_date=2000000000")
historical_data = data_response.json()

print(f"✅ Got {len(historical_data)} data points from API\n")

# Check a specific cauldron
cauldron_id = "cauldron_012"
processor = DataProcessor(historical_data)

print("="*60)
print(f"ANALYSIS OF {cauldron_id}")
print("="*60)

# Show actual data points
print("\nFirst 20 data points (actual levels from API):")
for i, entry in enumerate(historical_data[:20]):
    timestamp = entry['timestamp']
    level = entry['cauldron_levels'][cauldron_id]
    print(f"  {timestamp}: {level:.2f} units")

# Calculate fill rate
fill_rate = processor.calculate_fill_rate(cauldron_id)
print(f"\n✅ Fill rate CALCULATED from real data: {fill_rate:.4f} units/min")

# Show how we calculated it
print("\nShowing fill rate calculation (positive changes only):")
levels = []
for i, entry in enumerate(historical_data[:100]):
    levels.append({
        'time': entry['timestamp'],
        'level': entry['cauldron_levels'][cauldron_id]
    })

positive_changes = []
for i in range(1, len(levels)):
    change = levels[i]['level'] - levels[i-1]['level']
    if change > 0:
        positive_changes.append(change)
        if len(positive_changes) <= 10:
            print(f"  {levels[i-1]['time'][-8:]} → {levels[i]['time'][-8:]}: +{change:.4f} units/min")

import numpy as np
print(f"\n✅ Median of positive changes: {np.median(positive_changes):.4f} units/min")

print("\n" + "="*60)
print("CONCLUSION:")
print("="*60)
print("✅ Fill rates: Calculated from REAL API data (not made up)")
print("✅ Cauldron levels: From API (not made up)")
print("✅ Timestamps: From API (not made up)")
print("\n⚠️ PROBLEM: Our drain matching might be too flexible!")
print("We need to find THE ACTUAL DRAIN, not search for one that fits.")
