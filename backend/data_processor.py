"""
🔮 DATA PROCESSOR - CORRECT APPROACH
Find the ACTUAL daily drain, don't search for one that fits the report
"""

import numpy as np
from datetime import datetime
from typing import Dict, List

class DataProcessor:
    """Processes cauldron level data to find patterns and drain events"""
    
    def __init__(self, historical_data: List[Dict]):
        self.data = historical_data
        self.cauldron_ids = list(historical_data[0]['cauldron_levels'].keys()) if historical_data else []
        
    def calculate_fill_rate(self, cauldron_id: str) -> float:
        """Calculate the average fill rate from REAL data"""
        levels = []
        timestamps = []
        
        for entry in self.data:
            level = entry['cauldron_levels'].get(cauldron_id, 0)
            timestamp = datetime.fromisoformat(entry['timestamp'].replace('Z', '+00:00'))
            levels.append(level)
            timestamps.append(timestamp)
        
        if len(levels) < 10:
            return 0.1
        
        fill_rates = []
        
        for i in range(1, len(levels)):
            time_diff = (timestamps[i] - timestamps[i-1]).total_seconds() / 60
            level_diff = levels[i] - levels[i-1]
            
            if level_diff > 0 and time_diff > 0:
                rate = level_diff / time_diff
                if 0.01 < rate < 5:
                    fill_rates.append(rate)
        
        return np.median(fill_rates) if fill_rates else 0.1
    
    def get_daily_drain(self, cauldron_id: str, date_str: str) -> Dict:
        """
        Get THE daily drain for a cauldron on a specific date.
        
        Returns the primary drain event (peak to valley) for that day.
        """
        target_date = datetime.fromisoformat(date_str).date()
        
        # Get all data for this day
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
            return None
        
        day_data.sort(key=lambda x: x['timestamp'])
        
        # Find the peak and valley (main drain of the day)
        levels = [d['level'] for d in day_data]
        peak_level = max(levels)
        valley_level = min(levels)
        peak_idx = levels.index(peak_level)
        valley_idx = levels.index(valley_level)
        
        # Calculate drain only if valley comes after peak
        if valley_idx <= peak_idx:
            # Valley before peak - maybe no drain, just filling
            return None
        
        drain_amount = peak_level - valley_level
        
        # Only count significant drains
        if drain_amount < 15:
            return None
        
        duration = (day_data[valley_idx]['timestamp'] - day_data[peak_idx]['timestamp']).total_seconds() / 60
        
        return {
            'start_time': day_data[peak_idx]['timestamp'],
            'end_time': day_data[valley_idx]['timestamp'],
            'start_level': peak_level,
            'end_level': valley_level,
            'drain_amount': drain_amount,
            'duration_minutes': duration
        }
    
    def calculate_expected_collection(self, cauldron_id: str, drain_event: Dict, fill_rate: float) -> float:
        """
        Calculate expected collection from a drain event.
        Expected = Visible Drain + (Fill Rate × Duration)
        """
        if drain_event is None:
            return 0
        
        visible_drain = drain_event['drain_amount']
        duration = drain_event['duration_minutes']
        inflow = fill_rate * duration
        
        return visible_drain + inflow
    
    def detect_drain_events(self, cauldron_id: str, date_str: str) -> List[Dict]:
        """Get all drain events (for compatibility) - returns list with main daily drain"""
        drain = self.get_daily_drain(cauldron_id, date_str)
        return [drain] if drain else []
    
    def get_cauldron_stats(self, cauldron_id: str) -> Dict:
        """Get comprehensive statistics for a cauldron"""
        levels = [entry['cauldron_levels'].get(cauldron_id, 0) for entry in self.data]
        
        return {
            'cauldron_id': cauldron_id,
            'fill_rate': self.calculate_fill_rate(cauldron_id),
            'avg_level': np.mean(levels),
            'max_level': np.max(levels),
            'min_level': np.min(levels),
            'std_dev': np.std(levels)
        }
