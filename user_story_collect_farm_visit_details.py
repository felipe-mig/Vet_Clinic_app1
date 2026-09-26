#!/usr/bin/env python3
"""
User Story: Collect Farm Visit Details
Handles the collection and validation of farm visit booking information.
"""

import json
import os
from datetime import datetime
from typing import Dict, Optional, List


class FarmVisitDetailCollector:
    """Handles collection and validation of farm visit booking details."""

    def __init__(self, data_path: str = "clinic_data.json"):
        """Initialize the farm visit detail collector."""
        self.data_path = data_path
        self.data = self._load_data()
        self.farm_visit_details = {}

    def _load_data(self) -> Dict:
        """Load data from JSON file."""
        if os.path.exists(self.data_path):
            try:
                with open(self.data_path, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {"clients": [], "animals": [], "properties": [], "appointments": []}
        else:
            return {"clients": [], "animals": [], "properties": [], "appointments": []}

    def list_active_clients(self) -> List[Dict]:
        """List all active clients."""
        return [client for client in self.data.get('clients', []) if client.get('active', True)]

    def list_properties_by_client(self, client_id: int) -> List[Dict]:
        """List all active properties for a specific client."""
        return [property for property in self.data.get('properties', [])
                if property.get('active', True) and property.get('client_id') == client_id]

    def select_client(self) -> Optional[Dict]:
        """Interactive client selection."""
        print("\n--- Select Client ---")
        print("1. Search by ID")
        print("2. Search by name")
        print("3. List all clients")
        print("0. Cancel")

        choice = input("Select option (0-3): ").strip()

        if choice == "0":
            return None
        elif choice == "1":
            client_id = input("Enter client ID: ").strip()
            if client_id.isdigit():
                for client in self.data.get('clients', []):
                    if client['id'] == int(client_id) and client.get('active', True):
                        return client
                print("Client not found.")
                return None
            else:
                print("Invalid ID.")
                return None
        elif choice == "2":
            name = input("Enter client name: ").strip()
            matches = [client for client in self.data.get('clients', [])
                       if client.get('active', True) and name.lower() in client['name'].lower()]
            if matches:
                if len(matches) == 1:
                    return matches[0]
                else:
                    print(f"\nFound {len(matches)} matches:")
                    for i, client in enumerate(matches, 1):
                        print(f"{i}. {client['name']} (ID: {client['id']})")
                    selection = input("Select client number: ").strip()
                    if selection.isdigit() and 1 <= int(selection) <= len(matches):
                        return matches[int(selection) - 1]
                    else:
                        print("Invalid selection.")
                        return None
            else:
                print("No clients found.")
                return None
        elif choice == "3":
            clients = self.list_active_clients()
            if clients:
                print(f"\nAll Active Clients ({len(clients)}):")
                for i, client in enumerate(clients, 1):
                    print(f"{i}. {client['name']} (ID: {client['id']}) - Phone: {client.get('phone') or 'N/A'}")
                selection = input("Select client number: ").strip()
                if selection.isdigit() and 1 <= int(selection) <= len(clients):
                    return clients[int(selection) - 1]
                else:
                    print("Invalid selection.")
                    return None
            else:
                print("No active clients found.")
                return None
        else:
            print("Invalid option.")
            return None

    def select_property(self, client_id: int) -> Optional[Dict]:
        """Interactive property selection for a specific client."""
        print("\n--- Select Property ---")
        properties = self.list_properties_by_client(client_id)

        if not properties:
            print("No properties found for this client.")
            return None

        print(f"Properties for this client ({len(properties)}):")
        for i, prop in enumerate(properties, 1):
            prop_type = prop.get('property_type', 'Property')
            print(f"{i}. {prop['address']} - {prop_type} (ID: {prop['id']})")

        selection = input("Select property number: ").strip()
        if selection.isdigit() and 1 <= int(selection) <= len(properties):
            return properties[int(selection) - 1]
        else:
            print("Invalid selection.")
            return None

    def collect_date_time(self) -> Dict:
        """Collect date and time for the farm visit."""
        print("\n--- Select Date and Time ---")

        # Date collection
        date = input("Enter date (YYYY-MM-DD): ").strip()
        while not self.validate_date_format(date):
            print("Invalid date format. Please use YYYY-MM-DD format.")
            date = input("Enter date (YYYY-MM-DD): ").strip()

        # Time collection
        time = input("Enter time (HH:MM, 24-hour format): ").strip()
        while not self.validate_time_format(time):
            print("Invalid time format. Please use HH:MM format (24-hour).")
            time = input("Enter time (HH:MM, 24-hour format): ").strip()

        return {"date": date, "time": time}

    def validate_date_format(self, date_string: str) -> bool:
        """Validate date format (YYYY-MM-DD)."""
        try:
            datetime.strptime(date_string, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def validate_time_format(self, time_string: str) -> bool:
        """Validate time format (HH:MM)."""
        try:
            datetime.strptime(time_string, "%H:%M")
            return True
        except ValueError:
            return False

    def collect_duration(self) -> float:
        """Collect farm visit duration in hours."""
        print("\n--- Select Duration ---")
        print("Standard farm visit durations:")
        print("1. 1 hour")
        print("2. 2 hours")
        print("3. 3 hours")
        print("4. 4 hours")
        print("5. Half day (4 hours)")
        print("6. Full day (8 hours)")
        print("7. Custom duration")

        choice = input("Select option (1-7): ").strip()

        if choice == "1":
            return 1.0
        elif choice == "2":
            return 2.0
        elif choice == "3":
            return 3.0
        elif choice == "4":
            return 4.0
        elif choice == "5":
            return 4.0
        elif choice == "6":
            return 8.0
        elif choice == "7":
            duration = input("Enter custom duration in hours: ").strip()
            while True:
                try:
                    duration_float = float(duration)
                    if duration_float <= 0:
                        print("Duration must be greater than 0.")
                        duration = input("Enter custom duration in hours: ").strip()
                    else:
                        return duration_float
                except ValueError:
                    print("Please enter a valid number.")
                    duration = input("Enter custom duration in hours: ").strip()
        else:
            print("Invalid option. Using default 2 hours.")
            return 2.0

    def collect_notes(self) -> Optional[str]:
        """Collect optional notes for the farm visit."""
        notes = input("Enter any notes for this farm visit (optional): ").strip()
        return notes if notes else None

    def collect_farm_visit_details(self) -> Optional[Dict]:
        """Complete workflow for collecting farm visit details."""
        print("\n--- Collect Farm Visit Details ---")

        # Step 1: Select client
        client = self.select_client()
        if not client:
            print("Client selection failed or cancelled.")
            return None

        # Step 2: Select property
        property = self.select_property(client['id'])
        if not property:
            print("Property selection failed or cancelled.")
            return None

        # Step 3: Collect date and time
        date_time = self.collect_date_time()

        # Step 4: Collect duration
        duration_hours = self.collect_duration()

        # Step 5: Collect notes
        notes = self.collect_notes()

        # Compile all details
        self.farm_visit_details = {
            "client_id": client['id'],
            "client_name": client['name'],
            "property_id": property['id'],
            "property_address": property['address'],
            "property_type": property.get('property_type', 'Property'),
            "date": date_time['date'],
            "time": date_time['time'],
            "duration_hours": duration_hours,
            "notes": notes
        }

        return self.farm_visit_details

    def review_details(self) -> bool:
        """Display collected details for user review."""
        print("\n--- Review Farm Visit Details ---")
        print(f"Client: {self.farm_visit_details['client_name']} (ID: {self.farm_visit_details['client_id']})")
        print(f"Property: {self.farm_visit_details['property_address']} - {self.farm_visit_details['property_type']} (ID: {self.farm_visit_details['property_id']})")
        print(f"Date: {self.farm_visit_details['date']}")
        print(f"Time: {self.farm_visit_details['time']}")
        print(f"Duration: {self.farm_visit_details['duration_hours']} hours")
        print(f"Notes: {self.farm_visit_details['notes'] or 'None'}")

        confirm = input("\nAre these details correct? (y/n): ").strip().lower()
        return confirm == 'y'


def collect_farm_visit_details_workflow(data_path: str = "clinic_data.json"):
    """Complete workflow for collecting farm visit booking details."""
    collector = FarmVisitDetailCollector(data_path)

    # Collect all details
    details = collector.collect_farm_visit_details()
    if not details:
        return None

    # Review and edit cycle
    while True:
        if collector.review_details():
            break
        else:
            edit = input("Would you like to collect the details again? (y/n): ").strip().lower()
            if edit == 'y':
                details = collector.collect_farm_visit_details()
                if not details:
                    return None
            else:
                print("Farm visit detail collection cancelled.")
                return None

    return collector.farm_visit_details


if __name__ == "__main__":
    # Test the farm visit detail collection workflow
    print("Testing Farm Visit Detail Collection")
    details = collect_farm_visit_details_workflow()
    if details:
        print("\nFarm visit details collected successfully:")
        print(details)
    else:
        print("\nNo farm visit details collected.")
