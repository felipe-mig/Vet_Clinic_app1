#!/usr/bin/env python3
"""
User Story: Add Clients Detail
Handles the collection and validation of client information before adding to records.
"""

from datetime import datetime
from typing import Dict, Optional


class ClientDetailCollector:
    """Handles collection and validation of client details."""

    def __init__(self):
        """Initialize the client detail collector."""
        self.client_details = {}

    def collect_basic_info(self) -> Dict:
        """Collect basic client information."""
        print("\n--- Collect Client Details ---")
        print("Please enter the following client information:")

        name = input("Client name: ").strip()
        while not name:
            print("Name is required.")
            name = input("Client name: ").strip()

        phone = input("Phone number (optional): ").strip() or None
        email = input("Email address (optional): ").strip() or None
        address = input("Physical address (optional): ").strip() or None

        self.client_details = {
            "name": name,
            "phone": phone,
            "email": email,
            "address": address
        }

        return self.client_details

    def validate_email(self, email: str) -> bool:
        """Validate email format."""
        if not email:
            return True  # Email is optional

        # Basic email validation
        if "@" not in email or "." not in email:
            print("Warning: Email format appears invalid.")
            return False
        return True

    def validate_phone(self, phone: str) -> bool:
        """Validate phone number format."""
        if not phone:
            return True  # Phone is optional

        # Basic phone validation - check if it contains mostly digits
        digits = sum(c.isdigit() for c in phone)
        if digits < 7:
            print("Warning: Phone number appears too short.")
            return False
        return True

    def review_details(self) -> bool:
        """Display collected details for user review."""
        print("\n--- Review Client Details ---")
        print(f"Name: {self.client_details['name']}")
        print(f"Phone: {self.client_details['phone'] or 'Not provided'}")
        print(f"Email: {self.client_details['email'] or 'Not provided'}")
        print(f"Address: {self.client_details['address'] or 'Not provided'}")

        confirm = input("\nAre these details correct? (y/n): ").strip().lower()
        return confirm == 'y'

    def edit_details(self):
        """Allow user to edit specific fields."""
        print("\n--- Edit Client Details ---")
        print("1. Name")
        print("2. Phone")
        print("3. Email")
        print("4. Address")
        print("0. Done editing")

        while True:
            choice = input("Select field to edit (0-4): ").strip()

            if choice == "0":
                break
            elif choice == "1":
                new_name = input(f"Enter new name (current: {self.client_details['name']}): ").strip()
                if new_name:
                    self.client_details['name'] = new_name
            elif choice == "2":
                new_phone = input(f"Enter new phone (current: {self.client_details['phone'] or 'None'}): ").strip()
                self.client_details['phone'] = new_phone if new_phone else None
            elif choice == "3":
                new_email = input(f"Enter new email (current: {self.client_details['email'] or 'None'}): ").strip()
                self.client_details['email'] = new_email if new_email else None
            elif choice == "4":
                new_address = input(f"Enter new address (current: {self.client_details['address'] or 'None'}): ").strip()
                self.client_details['address'] = new_address if new_address else None
            else:
                print("Invalid choice.")

    def get_details(self) -> Dict:
        """Return the collected client details."""
        return self.client_details.copy()


def add_client_detail_workflow():
    """Complete workflow for adding client details."""
    collector = ClientDetailCollector()

    # Collect basic information
    collector.collect_basic_info()

    # Validate optional fields
    if collector.client_details['email']:
        collector.validate_email(collector.client_details['email'])
    if collector.client_details['phone']:
        collector.validate_phone(collector.client_details['phone'])

    # Review and edit cycle
    while True:
        if collector.review_details():
            break
        else:
            edit = input("Would you like to edit the details? (y/n): ").strip().lower()
            if edit == 'y':
                collector.edit_details()
            else:
                print("Client detail collection cancelled.")
                return None

    return collector.get_details()


if __name__ == "__main__":
    # Test the client detail collection workflow
    details = add_client_detail_workflow()
    if details:
        print("\nClient details collected successfully:")
        print(details)
    else:
        print("\nNo client details collected.")
