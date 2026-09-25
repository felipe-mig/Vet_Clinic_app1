#!/usr/bin/env python3
"""
User Story: Add Client to Clinic Records
Handles adding validated client details to the clinic's data storage system.
"""

import json
import os
from datetime import datetime
from typing import Dict, Optional, List


class ClinicRecordManager:
    """Manages the clinic's data storage and client record operations."""

    def __init__(self, data_path: str = "clinic_data.json"):
        """Initialize the clinic record manager."""
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

    def check_duplicate_client(self, name: str, phone: str = None, email: str = None) -> Optional[Dict]:
        """Check if a client with similar details already exists."""
        for client in self.data['clients']:
            if not client['active']:
                continue

            # Check by name (case-insensitive)
            if name.lower() == client['name'].lower():
                return {
                    'duplicate': True,
                    'field': 'name',
                    'existing_client': client,
                    'message': f"A client with the name '{name}' already exists."
                }

            # Check by phone if provided
            if phone and client['phone'] and phone == client['phone']:
                return {
                    'duplicate': True,
                    'field': 'phone',
                    'existing_client': client,
                    'message': f"A client with phone number '{phone}' already exists."
                }

            # Check by email if provided
            if email and client['email'] and email.lower() == client['email'].lower():
                return {
                    'duplicate': True,
                    'field': 'email',
                    'existing_client': client,
                    'message': f"A client with email '{email}' already exists."
                }

        return {'duplicate': False}

    def add_client_to_records(self, client_details: Dict) -> Optional[int]:
        """Add client details to clinic records."""
        # Check for duplicates
        duplicate_check = self.check_duplicate_client(
            client_details['name'],
            client_details.get('phone'),
            client_details.get('email')
        )

        if duplicate_check['duplicate']:
            print(f"\nWarning: {duplicate_check['message']}")
            print(f"Existing client ID: {duplicate_check['existing_client']['id']}")
            print(f"Existing client name: {duplicate_check['existing_client']['name']}")

            proceed = input("Do you want to proceed anyway? (y/n): ").strip().lower()
            if proceed != 'y':
                print("Client addition cancelled due to duplicate.")
                return None

        # Generate new client ID
        client_id = self._get_next_id(self.data['clients'])

        # Create client record
        client_record = {
            "id": client_id,
            "name": client_details['name'],
            "phone": client_details.get('phone'),
            "email": client_details.get('email'),
            "address": client_details.get('address'),
            "active": True,
            "created_at": datetime.now().isoformat()
        }

        # Add to records
        self.data['clients'].append(client_record)

        # Save to file
        self._save_data()

        return client_id

    def get_client_by_id(self, client_id: int) -> Optional[Dict]:
        """Retrieve a client record by ID."""
        for client in self.data['clients']:
            if client['id'] == client_id and client['active']:
                return client.copy()
        return None

    def list_all_clients(self) -> List[Dict]:
        """List all active clients in the records."""
        return [client.copy() for client in self.data['clients'] if client['active']]

    def close(self):
        """Save data and close."""
        self._save_data()


def add_client_to_clinic_records_workflow(client_details: Dict, data_path: str = "clinic_data.json"):
    """Complete workflow for adding client to clinic records."""
    print("\n--- Add Client to Clinic Records ---")

    # Initialize record manager
    record_manager = ClinicRecordManager(data_path)

    # Display client details being added
    print("Adding the following client to records:")
    print(f"Name: {client_details['name']}")
    print(f"Phone: {client_details.get('phone') or 'Not provided'}")
    print(f"Email: {client_details.get('email') or 'Not provided'}")
    print(f"Address: {client_details.get('address') or 'Not provided'}")

    # Add to records
    client_id = record_manager.add_client_to_records(client_details)

    if client_id:
        print(f"\nSuccess! Client added to clinic records with ID: {client_id}")
        print(f"Client is now active in the system.")

        # Show updated client count
        total_clients = len(record_manager.list_all_clients())
        print(f"Total active clients in system: {total_clients}")

        record_manager.close()
        return client_id
    else:
        print("\nFailed to add client to clinic records.")
        record_manager.close()
        return None


if __name__ == "__main__":
    # Test the add client to records workflow
    test_client_details = {
        "name": "Test Client",
        "phone": "555-1234",
        "email": "test@example.com",
        "address": "123 Test Street"
    }

    client_id = add_client_to_clinic_records_workflow(test_client_details)
    if client_id:
        print(f"\nTest completed. Client ID: {client_id}")
    else:
        print("\nTest failed.")
