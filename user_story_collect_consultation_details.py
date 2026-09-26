#!/usr/bin/env python3
"""
User Story: Collect Consultation Details
Handles the collection and validation of consultation booking information.
"""

import json
import os
from datetime import datetime
from typing import Dict, Optional, List


class ConsultationDetailCollector:
    """Handles collection and validation of consultation booking details."""

    def __init__(self, data_path: str = "clinic_data.json"):
        """Initialize the consultation detail collector."""
        self.data_path = data_path
        self.data = self._load_data()
        self.consultation_details = {}

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

    def list_animals_by_client(self, client_id: int) -> List[Dict]:
        """List all active animals for a specific client."""
        return [animal for animal in self.data.get('animals', [])
                if animal.get('active', True) and animal.get('client_id') == client_id]

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

    def select_animal(self, client_id: int) -> Optional[Dict]:
        """Interactive animal selection for a specific client."""
        print("\n--- Select Animal ---")
        animals = self.list_animals_by_client(client_id)

        if not animals:
            print("No animals found for this client.")
            return None

        print(f"Animals for this client ({len(animals)}):")
        for i, animal in enumerate(animals, 1):
            print(f"{i}. {animal['name']} - {animal['species']} (ID: {animal['id']})")

        selection = input("Select animal number: ").strip()
        if selection.isdigit() and 1 <= int(selection) <= len(animals):
            return animals[int(selection) - 1]
        else:
            print("Invalid selection.")
            return None

    def collect_date_time(self) -> Dict:
        """Collect date and time for the consultation."""
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

    def collect_duration(self) -> int:
        """Collect consultation duration in minutes."""
        print("\n--- Select Duration ---")
        print("Standard consultation durations:")
        print("1. 15 minutes")
        print("2. 30 minutes")
        print("3. 45 minutes")
        print("4. 60 minutes")
        print("5. Custom duration")

        choice = input("Select option (1-5): ").strip()

        if choice == "1":
            return 15
        elif choice == "2":
            return 30
        elif choice == "3":
            return 45
        elif choice == "4":
            return 60
        elif choice == "5":
            duration = input("Enter custom duration in minutes: ").strip()
            while not duration.isdigit() or int(duration) <= 0:
                print("Please enter a positive number.")
                duration = input("Enter custom duration in minutes: ").strip()
            return int(duration)
        else:
            print("Invalid option. Using default 15 minutes.")
            return 15

    def collect_notes(self) -> Optional[str]:
        """Collect optional notes for the consultation."""
        notes = input("Enter any notes for this consultation (optional): ").strip()
        return notes if notes else None

    def collect_consultation_details(self) -> Optional[Dict]:
        """Complete workflow for collecting consultation details."""
        print("\n--- Collect Consultation Details ---")

        # Step 1: Select client
        client = self.select_client()
        if not client:
            print("Client selection failed or cancelled.")
            return None

        # Step 2: Select animal
        animal = self.select_animal(client['id'])
        if not animal:
            print("Animal selection failed or cancelled.")
            return None

        # Step 3: Collect date and time
        date_time = self.collect_date_time()

        # Step 4: Collect duration
        duration = self.collect_duration()

        # Step 5: Collect notes
        notes = self.collect_notes()

        # Compile all details
        self.consultation_details = {
            "client_id": client['id'],
            "client_name": client['name'],
            "animal_id": animal['id'],
            "animal_name": animal['name'],
            "animal_species": animal['species'],
            "date": date_time['date'],
            "time": date_time['time'],
            "duration_minutes": duration,
            "notes": notes
        }

        return self.consultation_details

    def review_details(self) -> bool:
        """Display collected details for user review."""
        print("\n--- Review Consultation Details ---")
        print(f"Client: {self.consultation_details['client_name']} (ID: {self.consultation_details['client_id']})")
        print(f"Animal: {self.consultation_details['animal_name']} - {self.consultation_details['animal_species']} (ID: {self.consultation_details['animal_id']})")
        print(f"Date: {self.consultation_details['date']}")
        print(f"Time: {self.consultation_details['time']}")
        print(f"Duration: {self.consultation_details['duration_minutes']} minutes")
        print(f"Notes: {self.consultation_details['notes'] or 'None'}")

        confirm = input("\nAre these details correct? (y/n): ").strip().lower()
        return confirm == 'y'


def collect_consultation_details_workflow(data_path: str = "clinic_data.json"):
    """Complete workflow for collecting consultation booking details."""
    collector = ConsultationDetailCollector(data_path)

    # Collect all details
    details = collector.collect_consultation_details()
    if not details:
        return None

    # Review and edit cycle
    while True:
        if collector.review_details():
            break
        else:
            edit = input("Would you like to collect the details again? (y/n): ").strip().lower()
            if edit == 'y':
                details = collector.collect_consultation_details()
                if not details:
                    return None
            else:
                print("Consultation detail collection cancelled.")
                return None

    return collector.consultation_details


if __name__ == "__main__":
    # Test the consultation detail collection workflow
    print("Testing Consultation Detail Collection")
    details = collect_consultation_details_workflow()
    if details:
        print("\nConsultation details collected successfully:")
        print(details)
    else:
        print("\nNo consultation details collected.")
