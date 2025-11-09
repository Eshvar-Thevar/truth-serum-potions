"""
Check how we're handling multiple tickets per day
"""

import requests
from collections import defaultdict

tickets_response = requests.get("https://hackutd2025.eog.systems/api/Tickets")
tickets = tickets_response.json()['transport_tickets']

# Group by cauldron and date
grouped = defaultdict(list)
for ticket in tickets:
    key = (ticket['cauldron_id'], ticket['date'])
    grouped[key].append(ticket)

print("🔍 Checking for multiple tickets per cauldron per day:\n")
print("="*70)

# Find days with multiple tickets
multi_ticket_days = {k: v for k, v in grouped.items() if len(v) > 1}

for (cauldron, date), day_tickets in sorted(multi_ticket_days.items())[:10]:
    print(f"\n{cauldron} on {date}: {len(day_tickets)} tickets")
    total_reported = 0
    for ticket in day_tickets:
        print(f"  {ticket['ticket_id']}: {ticket['amount_collected']:.2f} units ({ticket['courier_id']})")
        total_reported += ticket['amount_collected']
    print(f"  📊 TOTAL REPORTED: {total_reported:.2f} units")

print("\n" + "="*70)
print(f"Found {len(multi_ticket_days)} days with multiple tickets")
print(f"Total tickets: {len(tickets)}")
print(f"Days with single ticket: {len(grouped) - len(multi_ticket_days)}")
