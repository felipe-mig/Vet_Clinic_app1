#!/usr/bin/env python3
"""
User Story: Add Animal to Clinic Records
Handles adding validated animal details to the clinic's data storage system.
"""

import json
import os
from datetime import datetime
from typing import Dict, Optional, List


class AnimalRecordManager:
    """Manages the clinic's animal data storage and record operations."""

    def __init__(self, data_path: str = "clinic_data.json"):
        """Initialize the animal record manager."""
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

    def check_duplicate_animal(self, name: str, client_id: int) -> Optional[Dict]:
        """Check if an animal with the same name exists for the same client."""
        for animal in self.data['animals']:
            if not animal['active']:
                continue

            # Check by name and client combination
            if (name.lower() == animal['name'].lower() and
                client_id == animal['client_id']):
                return {
                    'duplicate': True,
                    'existing_animal': animal,
                    'message': f"An animal named '{name}' already exists for this client."
                }

        return {'duplicate': False}

    def add_animal_to_records(self, animal_details: Dict) -> Optional[int]:
        """Add animal details to clinic records."""
        client_id = animal_details['client_id']

        # Verify client exists
        client = self.verify_client_exists(client_id)
        if not client:
            print(f"\nError: Client with ID {client_id} does not exist or is inactive.")
            return None

        # Check for duplicates
        duplicate_check = self.check_duplicate_animal(
            animal_details['name'],
            client_id
        )

        if duplicate_check['duplicate']:
            print(f"\nWarning: {duplicate_check['message']}")
            print(f"Existing animal ID: {duplicate_check['existing_animal']['id']}")
            print(f"Existing animal name: {duplicate_check['existing_animal']['name']}")
            print(f"Existing animal species: {duplicate_check['existing_animal']['species']}")

            proceed = input("Do you want to proceed anyway? (y/n): ").strip().lower()
            if proceed != 'y':
                print("Animal addition cancelled due to duplicate.")
                return None

        # Generate new animal ID
        animal_id = self._get_next_id(self.data['animals'])

        # Create animal record
        animal_record = {
            "id": animal_id,
            "name": animal_details['name'],
            "species": animal_details['species'],
            "breed": animal_details.get('breed'),
            "client_id": client_id,
            "active": True,
            "created_at": datetime.now().isoformat()
        }

        # Add to records
        self.data['animals'].append(animal_record)

        # Save to file
        self._save_data()

        return animal_id

    def get_animal_by_id(self, animal_id: int) -> Optional[Dict]:
        """Retrieve an animal record by ID."""
        for animal in self.data['animals']:
            if animal['id'] == animal_id and animal['active']:
                return animal.copy()
        return None

    def list_animals_by_client(self, client_id: int) -> List[Dict]:
        """List all active animals for a specific client."""
        return [animal.copy() for animal in self.data['animals']
                if animal['active'] and animal['client_id'] == client_id]

    def close(self):
        """Save data and close."""
        self._save_data()


def add_animal_to_clinic_records_workflow(animal_details: Dict, data_path: str = "clinic_data.json"):
    """Complete workflow for adding animal to clinic records."""
    print("\n--- Add Animal to Clinic Records ---")

    # Initialize record manager
    record_manager = AnimalRecordManager(data_path)

    # Display animal details being added
    print("Adding the following animal to records:")
    print(f"Client ID: {animal_details['client_id']}")
    print(f"Animal Name: {animal_details['name']}")
    print(f"Species: {animal_details['species']}")
    print(f"Breed: {animal_details.get('breed') or 'Not provided'}")

    # Add to records
    animal_id = record_manager.add_animal_to_records(animal_details)

    if animal_id:
        print(f"\nSuccess! Animal added to clinic records with ID: {animal_id}")
        print(f"Animal is now active in the system.")

        # Show updated animal count for this client
        client_animals = record_manager.list_animals_by_client(animal_details['client_id'])
        print(f"Total animals for this client: {len(client_animals)}")

        record_manager.close()
        return animal_id
    else:
        print("\nFailed to add animal to clinic records.")
        record_manager.close()
        return None


if __name__ == "__main__":
    # Test the add animal to records workflow
    test_animal_details = {
        "name": "Test Animal",
        "species": "Dog",
        "breed": "Labrador",
        "client_id": 1
    }

    animal_id = add_animal_to_clinic_records_workflow(test_animal_details)
    if animal_id:
        print(f"\nTest completed. Animal ID: {animal_id}")
    else:
        print("\nTest failed.")
