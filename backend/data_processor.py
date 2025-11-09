"""
🔮 DATA PROCESSOR - FIXED FOR GRADUAL DRAINS
This module analyzes historical cauldron data to calculate fill rates and detect drain events.
"""

import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

class DataProcessor:
    """Processes cauldron level data to find patterns and drain events"""
    
    def __init__(self, historical_data: List[Dict]):
        """
        Initialize with historical data from the API
        
        Args:
            historical_data: List of {timestamp, cauldron_levels} dictionaries
        """
        self.data = historical_data
        self.cauldron_ids = list(historical_data[0]['cauldron_levels'].keys()) if historical_data else []
        
    def calculate_fill_rate(self, cauldron_id: str) -> float:
        """
        Calculate the average fill rate (units per minute) for a cauldron.
        """
        levels = []
        timestamps = []
        
        # Extract all level data for this cauldron
        for entry in self.data:
            level = entry['cauldron_levels'].get(cauldron_id, 0)
            timestamp = datetime.fromisoformat(entry['timestamp'].replace('Z', '+00:00'))
            levels.append(level)
            timestamps.append(timestamp)
        
        if len(levels) < 10:
            return 0.1
        
        # Find periods of steady increase (no drains)
        fill_rates = []
        
        for i in range(1, len(levels)):
            time_diff = (timestamps[i] - timestamps[i-1]).total_seconds() / 60
            level_diff = levels[i] - levels[i-1]
            
            # Only consider positive changes (filling, not draining)
            if level_diff > 0 and time_diff > 0:
                rate = level_diff / time_diff
                if 0.01 < rate < 5:
                    fill_rates.append(rate)
        
        return np.median(fill_rates) if fill_rates else 0.1
    
    def detect_drain_events(self, cauldron_id: str, date_str: str) -> List[Dict]:
        """
        Detect drain events - NOW HANDLES BOTH SUDDEN AND GRADUAL DRAINS
        
        Strategy: Look for periods where the level goes DOWN significantly,
        regardless of whether it's sudden or gradual.
        """
        target_date = datetime.fromisoformat(date_str).date()
        
        day_data = []
        for entry in self.data:
            timestamp = datetime.fromisoformat(entry['timestamp'].replace('Z', '+00:00'))
            if timestamp.date() == target_date:
                level = entry['cauldron_levels'].get(cauldron_id, 0)
                day_data.append({
                    'timestamp': timestamp,
                    'level': level
                })
        
        if len(day_data) < 10:
            return []
        
        # Sort by timestamp
        day_data.sort(key=lambda x: x['timestamp'])
        
        # NEW APPROACH: Find the PEAK and the LOW point
        # The drain is from peak to low
        drain_events = []
        
        # Find local maxima (peaks) in the data
        i = 1
        while i < len(day_data) - 1:
            current_level = day_data[i]['level']
            prev_level = day_data[i-1]['level']
            
            # Is this a local peak? (higher than previous)
            if current_level > prev_level:
                # Found a potential peak, now look ahead for the valley
                peak_idx = i
                peak_level = current_level
                
                # Search forward for the lowest point before it starts rising again
                j = i + 1
                min_idx = i
                min_level = current_level
                
                while j < len(day_data):
                    if day_data[j]['level'] < min_level:
                        min_level = day_data[j]['level']
                        min_idx = j
                    elif day_data[j]['level'] > min_level + 5:
                        # Started rising significantly, drain is over
                        break
                    j += 1
                
                # Check if this is a significant drain
                drain_amount = peak_level - min_level
                
                if drain_amount > 20:  # At least 20 units drained
                    duration = (day_data[min_idx]['timestamp'] - day_data[peak_idx]['timestamp']).total_seconds() / 60
                    
                    drain_events.append({
                        'start_time': day_data[peak_idx]['timestamp'],
                        'end_time': day_data[min_idx]['timestamp'],
                        'start_level': peak_level,
                        'end_level': min_level,
                        'drain_amount': drain_amount,
                        'duration_minutes': max(duration, 1)  # At least 1 minute
                    })
                    
                    i = min_idx + 1  # Skip past this drain
                else:
                    i += 1
            else:
                i += 1
        
        return drain_events
    
    def calculate_expected_collection(self, cauldron_id: str, drain_event: Dict, fill_rate: float) -> float:
        """
        Calculate expected collection amount.
        
        For GRADUAL drains, potion keeps flowing in during the entire drain period.
        Expected = Visible Drain + (Fill Rate × Drain Duration)
        """
        visible_drain = drain_event['drain_amount']
        duration = drain_event['duration_minutes']
        
        # Potion that flowed in during the drain
        inflow_during_drain = fill_rate * duration
        
        # Total expected collection
        expected = visible_drain + inflow_during_drain
        
        return expected
    
    def get_cauldron_stats(self, cauldron_id: str) -> Dict:
        """
        Get comprehensive statistics for a cauldron
        """
        levels = [entry['cauldron_levels'].get(cauldron_id, 0) for entry in self.data]
        
        return {
            'cauldron_id': cauldron_id,
            'fill_rate': self.calculate_fill_rate(cauldron_id),
            'avg_level': np.mean(levels),
            'max_level': np.max(levels),
            'min_level': np.min(levels),
            'std_dev': np.std(levels)
        }
