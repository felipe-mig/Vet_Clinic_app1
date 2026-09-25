#!/usr/bin/env python3
"""
User Story: Select Date for Schedule View
Handles the collection and validation of date selection for viewing the day schedule.
"""

from datetime import datetime, timedelta
from typing import Optional


class DateSelector:
    """Handles date selection and validation for schedule viewing."""

    def __init__(self):
        """Initialize the date selector."""
        self.selected_date = None

    def collect_date(self) -> str:
        """Collect date from user."""
        print("\n--- Select Date for Schedule View ---")
        print("Please enter the date you want to view the schedule for:")

        date_input = input("Enter date (YYYY-MM-DD): ").strip()

        while not self.validate_date_format(date_input):
            print("Invalid date format. Please use YYYY-MM-DD format.")
            date_input = input("Enter date (YYYY-MM-DD): ").strip()

        self.selected_date = date_input
        return self.selected_date

    def validate_date_format(self, date_string: str) -> bool:
        """Validate date format (YYYY-MM-DD)."""
        try:
            datetime.strptime(date_string, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def validate_date_not_past(self, date_string: str) -> bool:
        """Check if the date is not in the past."""
        try:
            selected_date = datetime.strptime(date_string, "%Y-%m-%d").date()
            today = datetime.now().date()

            if selected_date < today:
                print(f"Warning: The selected date ({date_string}) is in the past.")
                confirm = input("Do you want to continue? (y/n): ").strip().lower()
                return confirm == 'y'

            return True
        except ValueError:
            return False

    def validate_date_not_too_far(self, date_string: str, max_days: int = 365) -> bool:
        """Check if the date is not too far in the future."""
        try:
            selected_date = datetime.strptime(date_string, "%Y-%m-%d").date()
            today = datetime.now().date()
            max_date = today + timedelta(days=max_days)

            if selected_date > max_date:
                print(f"Warning: The selected date ({date_string}) is more than {max_days} days in the future.")
                confirm = input("Do you want to continue? (y/n): ").strip().lower()
                return confirm == 'y'

            return True
        except ValueError:
            return False

    def suggest_dates(self) -> Optional[str]:
        """Suggest common date options to the user."""
        print("\nQuick options:")
        print("1. Today")
        print("2. Tomorrow")
        print("3. Next Monday")
        print("4. Custom date")
        print("0. Cancel")

        choice = input("Select option (0-4): ").strip()

        if choice == "0":
            return None
        elif choice == "1":
            return datetime.now().strftime("%Y-%m-%d")
        elif choice == "2":
            return (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        elif choice == "3":
            today = datetime.now()
            days_until_monday = (0 - today.weekday()) % 7
            if days_until_monday == 0:
                days_until_monday = 7  # Next Monday, not today if today is Monday
            return (today + timedelta(days=days_until_monday)).strftime("%Y-%m-%d")
        elif choice == "4":
            return self.collect_date()
        else:
            print("Invalid option.")
            return None

    def review_date(self) -> bool:
        """Display selected date for user review."""
        if not self.selected_date:
            return False

        try:
            date_obj = datetime.strptime(self.selected_date, "%Y-%m-%d")
            day_name = date_obj.strftime("%A")
            formatted_date = date_obj.strftime("%B %d, %Y")

            print(f"\n--- Review Selected Date ---")
            print(f"Date: {formatted_date} ({day_name})")
            print(f"Original format: {self.selected_date}")

            confirm = input("\nIs this the correct date? (y/n): ").strip().lower()
            return confirm == 'y'
        except ValueError:
            print("Error: Invalid date format.")
            return False

    def get_selected_date(self) -> Optional[str]:
        """Return the selected date."""
        return self.selected_date


def select_date_for_schedule_workflow():
    """Complete workflow for selecting a date for schedule viewing."""
    selector = DateSelector()

    # Offer quick options first
    print("Would you like to use a quick date option or enter a custom date?")
    quick_option = input("Use quick options? (y/n): ").strip().lower()

    if quick_option == 'y':
        date = selector.suggest_dates()
        if date:
            selector.selected_date = date
        else:
            print("Date selection cancelled.")
            return None
    else:
        # Collect custom date
        date = selector.collect_date()
        if not date:
            print("Date selection cancelled.")
            return None

    # Validate date not in past
    if not selector.validate_date_not_past(selector.selected_date):
        print("Date selection cancelled.")
        return None

    # Validate date not too far in future
    if not selector.validate_date_not_too_far(selector.selected_date):
        print("Date selection cancelled.")
        return None

    # Review date
    if not selector.review_date():
        edit = input("Would you like to select a different date? (y/n): ").strip().lower()
        if edit == 'y':
            return select_date_for_schedule_workflow()  # Recursive call for retry
        else:
            print("Date selection cancelled.")
            return None

    return selector.get_selected_date()


if __name__ == "__main__":
    # Test the date selection workflow
    print("Testing Date Selection for Schedule View")
    selected_date = select_date_for_schedule_workflow()
    if selected_date:
        print(f"\nDate selected successfully: {selected_date}")
    else:
        print("\nNo date selected.")
