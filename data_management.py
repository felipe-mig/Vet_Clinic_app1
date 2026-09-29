#!/usr/bin/env python3
"""
Data Management Module
Handles data loading, saving, and utility functions for the clinic management system.
"""

import json
import os
from typing import List, Dict


class DataManager:
    """Handles data persistence and utility operations."""

    def __init__(self, data_path: str = "clinic_data.json"):
        """Initialize the data manager with JSON data file."""
        self.data_path = data_path
        self.data = self._load_data()

    def _load_data(self) -> Dict:
        """Load data from JSON file or create default structure."""
        if os.path.exists(self.data_path):
            try:
                with open(self.data_path, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                # If file is corrupted, start fresh
                return self._create_default_data()
        else:
            return self._create_default_data()

    def _create_default_data(self) -> Dict:
        """Create default data structure."""
        return {
            "clients": [],
            "animals": [],
            "properties": [],
            "appointments": [],
            "clinic_hours": [
                {"day_of_week": 0, "start_time": "09:00", "end_time": "17:00"},  # Monday
                {"day_of_week": 1, "start_time": "09:00", "end_time": "17:00"},  # Tuesday
                {"day_of_week": 2, "start_time": "09:00", "end_time": "17:00"},  # Wednesday
                {"day_of_week": 3, "start_time": "09:00", "end_time": "17:00"},  # Thursday
                {"day_of_week": 4, "start_time": "09:00", "end_time": "17:00"},  # Friday
            ]
        }

    def _save_data(self):
        """Save data to JSON file."""
        with open(self.data_path, 'w') as f:
            json.dump(self.data, f, indent=2)

    def _get_next_id(self, items: List[Dict]) -> int:
        """Get the next available ID for a list of items."""
        if not items:
            return 1
        return max(item['id'] for item in items) + 1

    def close(self):
        """Save data and close."""
        self._save_data()
