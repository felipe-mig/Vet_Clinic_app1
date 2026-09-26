#!/usr/bin/env python3
"""
User Story: Book Farm Visit to Clinic Records
Handles adding validated farm visit details to the clinic's data storage system.
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, Optional, List


class FarmVisitBooker:
    """Manages farm visit booking and record operations."""

    def __init__(self, data_path: str = "clinic_data.json"):
        """Initialize the farm visit booker."""
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

    def verify_client_exists(self, client_id: int) -> bool:
        """Verify that the client exists and is active."""
        for client in self.data['clients']:
            if client['id'] == client_id and client['active']:
                return True
        return False

    def verify_property_exists(self, property_id: int) -> bool:
        """Verify that the property exists and is active."""
        for property in self.data['properties']:
            if property['id'] == property_id and property['active']:
                return True
        return False

    def check_farm_visit_conflicts(self, date: str, time: str, duration_hours: float) -> List[Dict]:
        """Check for conflicting farm visits on the same day."""
        conflicts = []
        duration_minutes = int(duration_hours * 60)

        for apt in self.data['appointments']:
            if apt['status'] == 'cancelled':
                continue
            if apt['type'] != 'farm_visit':
                continue
            if apt['date'] != date:
                continue

            # Check for time overlap
            apt_start = apt['time']
            apt_end_dt = datetime.strptime(f"{date} {apt_start}", "%Y-%m-%d %H:%M") + \
                          timedelta(minutes=apt['duration_minutes'])
            apt_end = apt_end_dt.strftime("%H:%M")

            visit_end_dt = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M") + \
                          timedelta(minutes=duration_minutes)
            visit_end = visit_end_dt.strftime("%H:%M")

            # Check if intervals overlap
            if not (visit_end <= apt_start or time >= apt_end):
                conflicts.append(apt.copy())

        return conflicts

    def validate_farm_visit_details(self, farm_visit_details: Dict) -> tuple:
        """Validate all farm visit details before booking."""
        errors = []

        # Verify client exists
        if not self.verify_client_exists(farm_visit_details['client_id']):
            errors.append("Client does not exist or is inactive.")

        # Verify property exists
        if not self.verify_property_exists(farm_visit_details['property_id']):
            errors.append("Property does not exist or is inactive.")

        # Validate duration is reasonable
        if farm_visit_details['duration_hours'] <= 0:
            errors.append("Duration must be greater than 0 hours.")
        elif farm_visit_details['duration_hours'] > 12:
            errors.append("Duration exceeds 12 hours. Please confirm this is correct.")

        # Check for conflicts
        conflicts = self.check_farm_visit_conflicts(
            farm_visit_details['date'],
            farm_visit_details['time'],
            farm_visit_details['duration_hours']
        )

        if conflicts:
            error_msg = f"Time slot conflicts with {len(conflicts)} existing farm visit(s):"
            for conflict in conflicts:
                duration_h = conflict['duration_minutes'] / 60
                error_msg += f"\n  - {conflict['time']} ({duration_h:.1f}h)"
            errors.append(error_msg)

        return (len(errors) == 0, errors, conflicts)

    def book_farm_visit(self, farm_visit_details: Dict) -> Optional[int]:
        """Book the farm visit to clinic records."""
        # Validate details
        is_valid, errors, conflicts = self.validate_farm_visit_details(farm_visit_details)

        if not is_valid:
            print("\nValidation Errors:")
            for error in errors:
                print(f"  - {error}")

            if conflicts:
                print("\nConflicting farm visits:")
                for conflict in conflicts:
                    duration_h = conflict['duration_minutes'] / 60
                    print(f"  - {conflict['time']} ({duration_h:.1f}h)")

            proceed = input("\nDo you want to proceed anyway? (y/n): ").strip().lower()
            if proceed != 'y':
                print("Farm visit booking cancelled due to validation errors.")
                return None

        # Generate new appointment ID
        appointment_id = self._get_next_id(self.data['appointments'])

        # Convert hours to minutes for storage
        duration_minutes = int(farm_visit_details['duration_hours'] * 60)

        # Create appointment record
        appointment = {
            "id": appointment_id,
            "type": "farm_visit",
            "animal_id": None,
            "property_id": farm_visit_details['property_id'],
            "client_id": farm_visit_details['client_id'],
            "date": farm_visit_details['date'],
            "time": farm_visit_details['time'],
            "duration_minutes": duration_minutes,
            "status": "booked",
            "notes": farm_visit_details.get('notes'),
            "created_at": datetime.now().isoformat()
        }

        # Add to records
        self.data['appointments'].append(appointment)

        # Save to file
        self._save_data()

        return appointment_id

    def get_appointment_by_id(self, appointment_id: int) -> Optional[Dict]:
        """Retrieve an appointment record by ID."""
        for apt in self.data['appointments']:
            if apt['id'] == appointment_id:
                return apt.copy()
        return None


def book_farm_visit_to_records_workflow(farm_visit_details: Dict, data_path: str = "clinic_data.json"):
    """Complete workflow for booking farm visit to clinic records."""
    print("\n--- Book Farm Visit to Clinic Records ---")

    # Initialize farm visit booker
    booker = FarmVisitBooker(data_path)

    # Display farm visit details being booked
    print("Booking the following farm visit:")
    print(f"Client: {farm_visit_details['client_name']} (ID: {farm_visit_details['client_id']})")
    print(f"Property: {farm_visit_details['property_address']} - {farm_visit_details['property_type']} (ID: {farm_visit_details['property_id']})")
    print(f"Date: {farm_visit_details['date']}")
    print(f"Time: {farm_visit_details['time']}")
    print(f"Duration: {farm_visit_details['duration_hours']} hours")
    print(f"Notes: {farm_visit_details.get('notes') or 'None'}")

    # Book the farm visit
    appointment_id = booker.book_farm_visit(farm_visit_details)

    if appointment_id:
        print(f"\nSuccess! Farm visit booked with ID: {appointment_id}")
        print(f"Appointment status: Booked")
        print(f"Appointment is now active in the system.")

        # Show appointment details
        appointment = booker.get_appointment_by_id(appointment_id)
        if appointment:
            duration_h = appointment['duration_minutes'] / 60
            print(f"\nAppointment Confirmation:")
            print(f"  ID: {appointment['id']}")
            print(f"  Date: {appointment['date']}")
            print(f"  Time: {appointment['time']}")
            print(f"  Duration: {duration_h:.1f} hours")
            print(f"  Status: {appointment['status']}")

        return appointment_id
    else:
        print("\nFailed to book farm visit to clinic records.")
        return None


if __name__ == "__main__":
    # Test the book farm visit workflow
    test_farm_visit_details = {
        "client_id": 1,
        "client_name": "Test Client",
        "property_id": 1,
        "property_address": "123 Farm Road",
        "property_type": "Farm",
        "date": "2026-09-25",
        "time": "10:00",
        "duration_hours": 2.0,
        "notes": "Test farm visit"
    }

    appointment_id = book_farm_visit_to_records_workflow(test_farm_visit_details)
    if appointment_id:
        print(f"\nTest completed. Appointment ID: {appointment_id}")
    else:
        print("\nTest failed.")
