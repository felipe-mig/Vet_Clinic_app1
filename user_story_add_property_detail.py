#!/usr/bin/env python3
"""
User Story: Add Property Detail
Handles the collection and validation of property information before adding to records.
"""

from datetime import datetime
from typing import Dict, Optional


class PropertyDetailCollector:
    """Handles collection and validation of property details."""

    def __init__(self):
        """Initialize the property detail collector."""
        self.property_details = {}
        self.client_id = None

    def set_client(self, client_id: int, client_name: str = None):
        """Set the client for this property."""
        self.client_id = client_id
        self.client_name = client_name

    def collect_basic_info(self) -> Dict:
        """Collect basic property information."""
        print("\n--- Collect Property Details ---")
        print("Please enter the following property information:")

        address = input("Property address: ").strip()
        while not address:
            print("Address is required.")
            address = input("Property address: ").strip()

        # Optional property details
        property_type = input("Property type (optional - e.g., Farm, House, Stable): ").strip() or None
        size_hectares = input("Size in hectares (optional): ").strip() or None
        location = input("Location/area (optional): ").strip() or None

        self.property_details = {
            "address": address,
            "property_type": property_type,
            "size_hectares": size_hectares,
            "location": location,
            "client_id": self.client_id
        }

        return self.property_details

    def validate_address(self, address: str) -> bool:
        """Validate address format."""
        if len(address) < 5:
            print("Warning: Address appears to be very short.")
            confirm = input("Continue with this address? (y/n): ").strip().lower()
            return confirm == 'y'
        return True

    def validate_size(self, size: str) -> bool:
        """Validate size if provided."""
        if size:
            try:
                size_float = float(size)
                if size_float <= 0:
                    print("Warning: Size must be greater than 0.")
                    return False
                if size_float > 10000:
                    print("Warning: Size is very large. Please verify.")
                    confirm = input("Continue with this size? (y/n): ").strip().lower()
                    return confirm == 'y'
            except ValueError:
                print("Warning: Size must be a number.")
                return False
        return True

    def review_details(self) -> bool:
        """Display collected details for user review."""
        print("\n--- Review Property Details ---")
        print(f"Client: {self.client_name or f'ID: {self.client_id}'}")
        print(f"Address: {self.property_details['address']}")
        print(f"Property Type: {self.property_details.get('property_type') or 'Not provided'}")
        print(f"Size (hectares): {self.property_details.get('size_hectares') or 'Not provided'}")
        print(f"Location: {self.property_details.get('location') or 'Not provided'}")

        confirm = input("\nAre these details correct? (y/n): ").strip().lower()
        return confirm == 'y'

    def edit_details(self):
        """Allow user to edit specific fields."""
        print("\n--- Edit Property Details ---")
        print("1. Address")
        print("2. Property Type")
        print("3. Size (hectares)")
        print("4. Location")
        print("0. Done editing")

        while True:
            choice = input("Select field to edit (0-4): ").strip()

            if choice == "0":
                break
            elif choice == "1":
                new_address = input(f"Enter new address (current: {self.property_details['address']}): ").strip()
                if new_address:
                    self.property_details['address'] = new_address
            elif choice == "2":
                new_type = input(f"Enter new property type (current: {self.property_details.get('property_type') or 'None'}): ").strip()
                self.property_details['property_type'] = new_type if new_type else None
            elif choice == "3":
                new_size = input(f"Enter new size in hectares (current: {self.property_details.get('size_hectares') or 'None'}): ").strip()
                self.property_details['size_hectares'] = new_size if new_size else None
            elif choice == "4":
                new_location = input(f"Enter new location (current: {self.property_details.get('location') or 'None'}): ").strip()
                self.property_details['location'] = new_location if new_location else None
            else:
                print("Invalid choice.")

    def get_details(self) -> Dict:
        """Return the collected property details."""
        return self.property_details.copy()


def add_property_detail_workflow(client_id: int, client_name: str = None):
    """Complete workflow for adding property details."""
    collector = PropertyDetailCollector()
    collector.set_client(client_id, client_name)

    # Collect basic information
    collector.collect_basic_info()

    # Validate address
    collector.validate_address(collector.property_details['address'])

    # Validate size if provided
    if collector.property_details.get('size_hectares'):
        collector.validate_size(collector.property_details['size_hectares'])

    # Review and edit cycle
    while True:
        if collector.review_details():
            break
        else:
            edit = input("Would you like to edit the details? (y/n): ").strip().lower()
            if edit == 'y':
                collector.edit_details()
            else:
                print("Property detail collection cancelled.")
                return None

    return collector.get_details()


if __name__ == "__main__":
    # Test the property detail collection workflow
    print("Testing Property Detail Collection")
    test_client_id = 1
    test_client_name = "Test Client"

    details = add_property_detail_workflow(test_client_id, test_client_name)
    if details:
        print("\nProperty details collected successfully:")
        print(details)
    else:
        print("\nNo property details collected.")
