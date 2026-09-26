#!/usr/bin/env python3
"""
User Story: Add Property to Clinic Records
Handles adding validated property details to the clinic's data storage system.
"""

import json
import os
from datetime import datetime
from typing import Dict, Optional, List


class PropertyRecordManager:
    """Manages the clinic's property data storage and record operations."""

    def __init__(self, data_path: str = "clinic_data.json"):
        """Initialize the property record manager."""
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

    def verify_client_exists(self, client_id: int) -> Optional[Dict]:
        """Verify that the client exists and is active."""
        for client in self.data['clients']:
            if client['id'] == client_id and client['active']:
                return client.copy()
        return None

    def check_duplicate_property(self, address: str, client_id: int) -> Optional[Dict]:
        """Check if a property with the same address exists for the same client."""
        for property in self.data['properties']:
            if not property['active']:
                continue

            # Check by address and client combination
            if (address.lower() == property['address'].lower() and
                client_id == property['client_id']):
                return {
                    'duplicate': True,
                    'existing_property': property,
                    'message': f"A property at '{address}' already exists for this client."
                }

        return {'duplicate': False}

    def add_property_to_records(self, property_details: Dict) -> Optional[int]:
        """Add property details to clinic records."""
        client_id = property_details['client_id']

        # Verify client exists
        client = self.verify_client_exists(client_id)
        if not client:
            print(f"\nError: Client with ID {client_id} does not exist or is inactive.")
            return None

        # Check for duplicates
        duplicate_check = self.check_duplicate_property(
            property_details['address'],
            client_id
        )

        if duplicate_check['duplicate']:
            print(f"\nWarning: {duplicate_check['message']}")
            print(f"Existing property ID: {duplicate_check['existing_property']['id']}")
            print(f"Existing property address: {duplicate_check['existing_property']['address']}")

            proceed = input("Do you want to proceed anyway? (y/n): ").strip().lower()
            if proceed != 'y':
                print("Property addition cancelled due to duplicate.")
                return None

        # Generate new property ID
        property_id = self._get_next_id(self.data['properties'])

        # Create property record
        property_record = {
            "id": property_id,
            "address": property_details['address'],
            "property_type": property_details.get('property_type'),
            "size_hectares": property_details.get('size_hectares'),
            "location": property_details.get('location'),
            "client_id": client_id,
            "active": True,
            "created_at": datetime.now().isoformat()
        }

        # Add to records
        self.data['properties'].append(property_record)

        # Save to file
        self._save_data()

        return property_id

    def get_property_by_id(self, property_id: int) -> Optional[Dict]:
        """Retrieve a property record by ID."""
        for property in self.data['properties']:
            if property['id'] == property_id and property['active']:
                return property.copy()
        return None

    def list_properties_by_client(self, client_id: int) -> List[Dict]:
        """List all active properties for a specific client."""
        return [property.copy() for property in self.data['properties']
                if property['active'] and property['client_id'] == client_id]

    def close(self):
        """Save data and close."""
        self._save_data()


def add_property_to_clinic_records_workflow(property_details: Dict, data_path: str = "clinic_data.json"):
    """Complete workflow for adding property to clinic records."""
    print("\n--- Add Property to Clinic Records ---")

    # Initialize record manager
    record_manager = PropertyRecordManager(data_path)

    # Display property details being added
    print("Adding the following property to records:")
    print(f"Client ID: {property_details['client_id']}")
    print(f"Address: {property_details['address']}")
    print(f"Property Type: {property_details.get('property_type') or 'Not provided'}")
    print(f"Size (hectares): {property_details.get('size_hectares') or 'Not provided'}")
    print(f"Location: {property_details.get('location') or 'Not provided'}")

    # Add to records
    property_id = record_manager.add_property_to_records(property_details)

    if property_id:
        print(f"\nSuccess! Property added to clinic records with ID: {property_id}")
        print(f"Property is now active in the system.")

        # Show updated property count for this client
        client_properties = record_manager.list_properties_by_client(property_details['client_id'])
        print(f"Total properties for this client: {len(client_properties)}")

        record_manager.close()
        return property_id
    else:
        print("\nFailed to add property to clinic records.")
        record_manager.close()
        return None


if __name__ == "__main__":
    # Test the add property to records workflow
    test_property_details = {
        "address": "123 Farm Road",
        "property_type": "Farm",
        "size_hectares": "50",
        "location": "Rural Area",
        "client_id": 1
    }

    property_id = add_property_to_clinic_records_workflow(test_property_details)
    if property_id:
        print(f"\nTest completed. Property ID: {property_id}")
    else:
        print("\nTest failed.")
