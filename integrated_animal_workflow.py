#!/usr/bin/env python3
"""
Integrated Animal Addition Workflow
Combines both user stories: Add Animal Detail and Add Animal to Clinic Records
This demonstrates the complete end-to-end process of adding a new animal to a client.
"""

import json
import os
from typing import Dict, Optional
from user_story_add_animal_detail import add_animal_detail_workflow
from user_story_add_animal_to_clinic_records import add_animal_to_clinic_records_workflow


class ClientSelector:
    """Helper class to select a client for animal addition."""

    def __init__(self, data_path: str = "clinic_data.json"):
        """Initialize the client selector."""
        self.data_path = data_path
        self.data = self._load_data()

    def _load_data(self) -> Dict:
        """Load data from JSON file."""
        if os.path.exists(self.data_path):
            try:
                with open(self.data_path, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {"clients": []}
        else:
            return {"clients": []}

    def list_active_clients(self) -> list:
        """List all active clients."""
        return [client for client in self.data.get('clients', []) if client.get('active', True)]

    def find_client_by_id(self, client_id: int) -> Optional[Dict]:
        """Find a client by ID."""
        for client in self.data.get('clients', []):
            if client['id'] == client_id and client.get('active', True):
                return client
        return None

    def find_client_by_name(self, name: str) -> list:
        """Find clients by name (partial match)."""
        matches = []
        for client in self.data.get('clients', []):
            if client.get('active', True) and name.lower() in client['name'].lower():
                matches.append(client)
        return matches

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
                client = self.find_client_by_id(int(client_id))
                if client:
                    return client
                else:
                    print("Client not found.")
                    return None
            else:
                print("Invalid ID.")
                return None
        elif choice == "2":
            name = input("Enter client name: ").strip()
            matches = self.find_client_by_name(name)
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


def complete_animal_addition_workflow(data_path: str = "clinic_data.json"):
    """
    Complete workflow for adding a new animal to a client.
    This integrates both user stories into a seamless process.
    """
    print("="*60)
    print("ANIMAL ADDITION WORKFLOW")
    print("="*60)
    print("This process involves three steps:")
    print("1. Select the client")
    print("2. Collect and validate animal details")
    print("3. Add animal to clinic records")
    print("="*60)

    # Step 1: Select Client
    print("\n--- STEP 1: Select Client ---")
    selector = ClientSelector(data_path)
    client = selector.select_client()

    if not client:
        print("\nClient selection failed or was cancelled.")
        print("Workflow terminated.")
        return None

    print(f"\nSelected client: {client['name']} (ID: {client['id']})")

    # Step 2: Add Animal Detail (User Story 1)
    print("\n--- STEP 2: Add Animal Detail ---")
    animal_details = add_animal_detail_workflow(client['id'], client['name'])

    if not animal_details:
        print("\nAnimal detail collection failed or was cancelled.")
        print("Workflow terminated.")
        return None

    # Step 3: Add Animal to Clinic Records (User Story 2)
    print("\n--- STEP 3: Add Animal to Clinic Records ---")
    animal_id = add_animal_to_clinic_records_workflow(animal_details, data_path)

    if animal_id:
        print("\n" + "="*60)
        print("ANIMAL ADDITION WORKFLOW COMPLETED SUCCESSFULLY")
        print("="*60)
        print(f"Client: {client['name']} (ID: {client['id']})")
        print(f"Animal Name: {animal_details['name']}")
        print(f"Animal ID: {animal_id}")
        print(f"Species: {animal_details['species']}")
        print(f"Breed: {animal_details.get('breed') or 'Not provided'}")
        print("="*60)
        return animal_id
    else:
        print("\n" + "="*60)
        print("ANIMAL ADDITION WORKFLOW FAILED")
        print("="*60)
        print("The animal details were collected but could not be added to records.")
        print("="*60)
        return None


def main():
    """Main entry point for the integrated animal addition workflow."""
    print("\nWelcome to the Veterinary Clinic Management System")
    print("Animal Addition Module\n")

    while True:
        print("\nOptions:")
        print("1. Add a new animal to a client (complete workflow)")
        print("2. Exit")

        choice = input("Select option (1-2): ").strip()

        if choice == "1":
            complete_animal_addition_workflow()
        elif choice == "2":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
