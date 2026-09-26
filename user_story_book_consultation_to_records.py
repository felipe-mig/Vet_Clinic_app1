#!/usr/bin/env python3
"""
User Story: Book Consultation to Clinic Records
Handles adding validated consultation details to the clinic's data storage system.
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, Optional, List


class ConsultationBooker:
    """Manages consultation booking and record operations."""

    def __init__(self, data_path: str = "clinic_data.json"):
        """Initialize the consultation booker."""
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

    def get_clinic_hours(self, day_of_week: int) -> Optional[Dict]:
        """Get clinic hours for a specific day (0=Monday, 6=Sunday)."""
        for hours in self.data['clinic_hours']:
            if hours['day_of_week'] == day_of_week:
                return hours.copy()
        return None

    def is_within_clinic_hours(self, date: str, time: str) -> bool:
        """Check if a given date/time is within clinic hours."""
        try:
            dt = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
            day_of_week = dt.weekday()  # 0=Monday, 6=Sunday

            hours = self.get_clinic_hours(day_of_week)
            if not hours:
                return False

            start = datetime.strptime(f"{date} {hours['start_time']}", "%Y-%m-%d %H:%M")
            end = datetime.strptime(f"{date} {hours['end_time']}", "%Y-%m-%d %H:%M")

            return start <= dt < end
        except ValueError:
            return False

    def get_slot_conflicts(self, date: str, time: str, duration_minutes: int) -> List[Dict]:
        """Check for conflicting appointments in the same time slot."""
        conflicts = []
        start_time = time
        end_dt = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M") + timedelta(minutes=duration_minutes)
        end_time = end_dt.strftime("%H:%M")

        for apt in self.data['appointments']:
            if apt['status'] == 'cancelled':
                continue
            if apt['type'] != 'consultation':
                continue
            if apt['date'] != date:
                continue

            # Check for time overlap
            apt_start = apt['time']
            apt_end_dt = datetime.strptime(f"{date} {apt_start}", "%Y-%m-%d %H:%M") + timedelta(minutes=apt['duration_minutes'])
            apt_end = apt_end_dt.strftime("%H:%M")

            # Check if intervals overlap
            if not (end_time <= apt_start or start_time >= apt_end):
                conflicts.append(apt.copy())

        return conflicts

    def verify_client_exists(self, client_id: int) -> bool:
        """Verify that the client exists and is active."""
        for client in self.data['clients']:
            if client['id'] == client_id and client['active']:
                return True
        return False

    def verify_animal_exists(self, animal_id: int) -> bool:
        """Verify that the animal exists and is active."""
        for animal in self.data['animals']:
            if animal['id'] == animal_id and animal['active']:
                return True
        return False

    def validate_consultation_details(self, consultation_details: Dict) -> tuple:
        """Validate all consultation details before booking."""
        errors = []

        # Verify client exists
        if not self.verify_client_exists(consultation_details['client_id']):
            errors.append("Client does not exist or is inactive.")

        # Verify animal exists
        if not self.verify_animal_exists(consultation_details['animal_id']):
            errors.append("Animal does not exist or is inactive.")

        # Validate clinic hours
        if not self.is_within_clinic_hours(consultation_details['date'], consultation_details['time']):
            errors.append("Appointment time is outside clinic hours.")

        # Validate 15-minute increments
        if consultation_details['duration_minutes'] % 15 != 0:
            errors.append("Duration must be in 15-minute increments.")

        # Check for conflicts
        conflicts = self.get_slot_conflicts(
            consultation_details['date'],
            consultation_details['time'],
            consultation_details['duration_minutes']
        )

        if conflicts:
            error_msg = f"Time slot conflicts with {len(conflicts)} existing appointment(s):"
            for conflict in conflicts:
                error_msg += f"\n  - {conflict['time']} ({conflict['duration_minutes']} min)"
            errors.append(error_msg)

        return (len(errors) == 0, errors, conflicts)

    def book_consultation(self, consultation_details: Dict) -> Optional[int]:
        """Book the consultation to clinic records."""
        # Validate details
        is_valid, errors, conflicts = self.validate_consultation_details(consultation_details)

        if not is_valid:
            print("\nValidation Errors:")
            for error in errors:
                print(f"  - {error}")

            if conflicts:
                print("\nConflicting appointments:")
                for conflict in conflicts:
                    print(f"  - {conflict['time']} ({conflict['duration_minutes']} min)")

            proceed = input("\nDo you want to proceed anyway? (y/n): ").strip().lower()
            if proceed != 'y':
                print("Consultation booking cancelled due to validation errors.")
                return None

        # Generate new appointment ID
        appointment_id = self._get_next_id(self.data['appointments'])

        # Create appointment record
        appointment = {
            "id": appointment_id,
            "type": "consultation",
            "animal_id": consultation_details['animal_id'],
            "property_id": None,
            "client_id": consultation_details['client_id'],
            "date": consultation_details['date'],
            "time": consultation_details['time'],
            "duration_minutes": consultation_details['duration_minutes'],
            "status": "booked",
            "notes": consultation_details.get('notes'),
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


def book_consultation_to_records_workflow(consultation_details: Dict, data_path: str = "clinic_data.json"):
    """Complete workflow for booking consultation to clinic records."""
    print("\n--- Book Consultation to Clinic Records ---")

    # Initialize consultation booker
    booker = ConsultationBooker(data_path)

    # Display consultation details being booked
    print("Booking the following consultation:")
    print(f"Client: {consultation_details['client_name']} (ID: {consultation_details['client_id']})")
    print(f"Animal: {consultation_details['animal_name']} - {consultation_details['animal_species']} (ID: {consultation_details['animal_id']})")
    print(f"Date: {consultation_details['date']}")
    print(f"Time: {consultation_details['time']}")
    print(f"Duration: {consultation_details['duration_minutes']} minutes")
    print(f"Notes: {consultation_details.get('notes') or 'None'}")

    # Book the consultation
    appointment_id = booker.book_consultation(consultation_details)

    if appointment_id:
        print(f"\nSuccess! Consultation booked with ID: {appointment_id}")
        print(f"Appointment status: Booked")
        print(f"Appointment is now active in the system.")

        # Show appointment details
        appointment = booker.get_appointment_by_id(appointment_id)
        if appointment:
            print(f"\nAppointment Confirmation:")
            print(f"  ID: {appointment['id']}")
            print(f"  Date: {appointment['date']}")
            print(f"  Time: {appointment['time']}")
            print(f"  Duration: {appointment['duration_minutes']} minutes")
            print(f"  Status: {appointment['status']}")

        return appointment_id
    else:
        print("\nFailed to book consultation to clinic records.")
        return None


if __name__ == "__main__":
    # Test the book consultation workflow
    test_consultation_details = {
        "client_id": 1,
        "client_name": "Test Client",
        "animal_id": 1,
        "animal_name": "Test Animal",
        "animal_species": "Dog",
        "date": "2026-09-25",
        "time": "10:00",
        "duration_minutes": 15,
        "notes": "Test consultation"
    }

    appointment_id = book_consultation_to_records_workflow(test_consultation_details)
    if appointment_id:
        print(f"\nTest completed. Appointment ID: {appointment_id}")
    else:
        print("\nTest failed.")
