#!/usr/bin/env python3
"""
User Story: Add Animal Detail
Handles the collection and validation of animal information before adding to records.
"""

from datetime import datetime
from typing import Dict, Optional


class AnimalDetailCollector:
    """Handles collection and validation of animal details."""

    def __init__(self):
        """Initialize the animal detail collector."""
        self.animal_details = {}
        self.client_id = None

    def set_client(self, client_id: int, client_name: str = None):
        """Set the client for this animal."""
        self.client_id = client_id
        self.client_name = client_name

    def collect_basic_info(self) -> Dict:
        """Collect basic animal information."""
        print("\n--- Collect Animal Details ---")
        print("Please enter the following animal information:")

        name = input("Animal name: ").strip()
        while not name:
            print("Name is required.")
            name = input("Animal name: ").strip()

        species = input("Species (e.g., Dog, Cat, Horse): ").strip()
        while not species:
            print("Species is required.")
            species = input("Species (e.g., Dog, Cat, Horse): ").strip()

        breed = input("Breed (optional): ").strip() or None

        self.animal_details = {
            "name": name,
            "species": species,
            "breed": breed,
            "client_id": self.client_id
        }

        return self.animal_details

    def validate_species(self, species: str) -> bool:
        """Validate species entry."""
        common_species = ['dog', 'cat', 'horse', 'cow', 'sheep', 'goat', 'pig', 'bird', 'rabbit', 'reptile']
        if species.lower() in common_species:
            return True

        print(f"Note: '{species}' is not a common species. Please verify this is correct.")
        confirm = input("Continue with this species? (y/n): ").strip().lower()
        return confirm == 'y'

    def review_details(self) -> bool:
        """Display collected details for user review."""
        print("\n--- Review Animal Details ---")
        print(f"Client: {self.client_name or f'ID: {self.client_id}'}")
        print(f"Animal Name: {self.animal_details['name']}")
        print(f"Species: {self.animal_details['species']}")
        print(f"Breed: {self.animal_details['breed'] or 'Not provided'}")

        confirm = input("\nAre these details correct? (y/n): ").strip().lower()
        return confirm == 'y'

    def edit_details(self):
        """Allow user to edit specific fields."""
        print("\n--- Edit Animal Details ---")
        print("1. Animal Name")
        print("2. Species")
        print("3. Breed")
        print("0. Done editing")

        while True:
            choice = input("Select field to edit (0-3): ").strip()

            if choice == "0":
                break
            elif choice == "1":
                new_name = input(f"Enter new name (current: {self.animal_details['name']}): ").strip()
                if new_name:
                    self.animal_details['name'] = new_name
            elif choice == "2":
                new_species = input(f"Enter new species (current: {self.animal_details['species']}): ").strip()
                if new_species:
                    self.animal_details['species'] = new_species
            elif choice == "3":
                new_breed = input(f"Enter new breed (current: {self.animal_details['breed'] or 'None'}): ").strip()
                self.animal_details['breed'] = new_breed if new_breed else None
            else:
                print("Invalid choice.")

    def get_details(self) -> Dict:
        """Return the collected animal details."""
        return self.animal_details.copy()


def add_animal_detail_workflow(client_id: int, client_name: str = None):
    """Complete workflow for adding animal details."""
    collector = AnimalDetailCollector()
    collector.set_client(client_id, client_name)

    # Collect basic information
    collector.collect_basic_info()

    # Validate species
    collector.validate_species(collector.animal_details['species'])

    # Review and edit cycle
    while True:
        if collector.review_details():
            break
        else:
            edit = input("Would you like to edit the details? (y/n): ").strip().lower()
            if edit == 'y':
                collector.edit_details()
            else:
                print("Animal detail collection cancelled.")
                return None

    return collector.get_details()


if __name__ == "__main__":
    # Test the animal detail collection workflow
    print("Testing Animal Detail Collection")
    test_client_id = 1
    test_client_name = "Test Client"

    details = add_animal_detail_workflow(test_client_id, test_client_name)
    if details:
        print("\nAnimal details collected successfully:")
        print(details)
    else:
        print("\nNo animal details collected.")
