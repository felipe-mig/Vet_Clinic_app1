#!/usr/bin/env python3
"""
User Story: View Schedule from Clinic Records
Handles retrieving and displaying the day schedule from the clinic's data storage system.
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, Optional, List


class ScheduleViewer:
    """Manages schedule retrieval and display from clinic records."""

    def __init__(self, data_path: str = "clinic_data.json"):
        """Initialize the schedule viewer."""
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

    def get_clinic_hours(self, day_of_week: int) -> Optional[Dict]:
        """Get clinic hours for a specific day (0=Monday, 6=Sunday)."""
        for hours in self.data['clinic_hours']:
            if hours['day_of_week'] == day_of_week:
                return hours.copy()
        return None

    def get_appointments_for_date(self, date: str) -> List[Dict]:
        """Get all appointments for a specific date."""
        appointments = []
        for apt in self.data['appointments']:
            if apt['date'] == date and apt['status'] != 'cancelled':
                # Add related information
                appointment = apt.copy()

                # Add client name
                for client in self.data['clients']:
                    if client['id'] == apt['client_id'] and client['active']:
                        appointment['client_name'] = client['name']
                        break

                # Add animal name for consultations
                if apt['type'] == 'consultation' and apt['animal_id']:
                    for animal in self.data['animals']:
                        if animal['id'] == apt['animal_id'] and animal['active']:
                            appointment['animal_name'] = animal['name']
                            break

                # Add property address for farm visits
                if apt['type'] == 'farm_visit' and apt['property_id']:
                    for prop in self.data['properties']:
                        if prop['id'] == apt['property_id'] and prop['active']:
                            appointment['property_address'] = prop['address']
                            break

                appointments.append(appointment)

        return appointments

    def generate_time_slots(self, date: str, clinic_hours: Dict) -> List[Dict]:
        """Generate 15-minute time slots for the day."""
        slots = []
        if not clinic_hours:
            return slots

        start = datetime.strptime(f"{date} {clinic_hours['start_time']}", "%Y-%m-%d %H:%M")
        end = datetime.strptime(f"{date} {clinic_hours['end_time']}", "%Y-%m-%d %H:%M")

        current = start
        while current < end:
            slot_time = current.strftime("%H:%M")
            slot_end = (current + timedelta(minutes=15)).strftime("%H:%M")

            slots.append({
                'time': slot_time,
                'end_time': slot_end,
                'booked': False,
                'appointment': None
            })

            current += timedelta(minutes=15)

        return slots

    def populate_slots_with_appointments(self, slots: List[Dict], consultations: List[Dict]) -> List[Dict]:
        """Populate time slots with consultation appointments."""
        for slot in slots:
            for consultation in consultations:
                cons_time = consultation['time']
                cons_end_dt = datetime.strptime(f"{consultation['date']} {cons_time}", "%Y-%m-%d %H:%M") + \
                              timedelta(minutes=consultation['duration_minutes'])
                cons_end = cons_end_dt.strftime("%H:%M")

                if cons_time <= slot['time'] < cons_end:
                    slot['booked'] = True
                    slot['appointment'] = consultation
                    break

        return slots

    def get_day_schedule(self, date: str) -> Dict:
        """Get complete day schedule with time slots and appointments."""
        # Get the day of the week
        dt = datetime.strptime(date, "%Y-%m-%d")
        day_of_week = dt.weekday()

        # Get clinic hours
        clinic_hours = self.get_clinic_hours(day_of_week)

        # Get all appointments for the day
        all_appointments = self.get_appointments_for_date(date)

        # Separate consultations and farm visits
        consultations = [apt for apt in all_appointments if apt['type'] == 'consultation']
        farm_visits = [apt for apt in all_appointments if apt['type'] == 'farm_visit']

        # Generate time slots
        slots = self.generate_time_slots(date, clinic_hours)

        # Populate slots with consultations
        slots = self.populate_slots_with_appointments(slots, consultations)

        return {
            'date': date,
            'day_of_week': day_of_week,
            'clinic_hours': clinic_hours,
            'slots': slots,
            'consultations': consultations,
            'farm_visits': farm_visits
        }

    def display_schedule(self, schedule: Dict):
        """Display the day schedule in a user-friendly format."""
        date_obj = datetime.strptime(schedule['date'], "%Y-%m-%d")
        day_name = date_obj.strftime("%A")
        formatted_date = date_obj.strftime("%B %d, %Y")

        print(f"\n{'='*60}")
        print(f"SCHEDULE FOR {day_name.upper()}, {formatted_date.upper()}")
        print(f"{'='*60}")

        # Display clinic hours
        if schedule['clinic_hours']:
            print(f"\nClinic Hours: {schedule['clinic_hours']['start_time']} - {schedule['clinic_hours']['end_time']}")
        else:
            print("\nClinic closed on this day")

        # Display consultation slots
        if schedule['slots']:
            print(f"\n{'-'*60}")
            print("15-MINUTE CONSULTATION SLOTS")
            print(f"{'-'*60}")

            for slot in schedule['slots']:
                status = "BOOKED" if slot['booked'] else "AVAILABLE"
                print(f"{slot['time']} - {slot['end_time']}: {status}")

                if slot['appointment']:
                    client_name = slot['appointment'].get('client_name', 'Unknown')
                    animal_name = slot['appointment'].get('animal_name', 'Unknown')
                    duration = slot['appointment']['duration_minutes']
                    print(f"  → {client_name} - {animal_name} ({duration} min)")

        # Display farm visits
        if schedule['farm_visits']:
            print(f"\n{'-'*60}")
            print("FARM VISITS")
            print(f"{'-'*60}")

            for visit in schedule['farm_visits']:
                client_name = visit.get('client_name', 'Unknown')
                property_address = visit.get('property_address', 'Unknown')
                duration_hours = visit['duration_minutes'] / 60
                print(f"{visit['time']} - {client_name} at {property_address} ({duration_hours:.1f}h)")

        # Display summary
        total_consultations = len(schedule['consultations'])
        total_farm_visits = len(schedule['farm_visits'])
        total_appointments = total_consultations + total_farm_visits

        print(f"\n{'-'*60}")
        print("SUMMARY")
        print(f"{'-'*60}")
        print(f"Total Consultations: {total_consultations}")
        print(f"Total Farm Visits: {total_farm_visits}")
        print(f"Total Appointments: {total_appointments}")

        if schedule['slots']:
            available_slots = sum(1 for slot in schedule['slots'] if not slot['booked'])
            print(f"Available Time Slots: {available_slots}")

        print(f"{'='*60}")


def view_schedule_from_records_workflow(date: str, data_path: str = "clinic_data.json"):
    """Complete workflow for viewing schedule from clinic records."""
    print("\n--- View Schedule from Clinic Records ---")

    # Initialize schedule viewer
    viewer = ScheduleViewer(data_path)

    # Get the day schedule
    schedule = viewer.get_day_schedule(date)

    if not schedule:
        print(f"\nNo schedule data found for {date}.")
        return None

    # Display the schedule
    viewer.display_schedule(schedule)

    return schedule


if __name__ == "__main__":
    # Test the view schedule workflow
    print("Testing Schedule View from Records")
    test_date = "2026-09-25"  # Today's date for testing

    schedule = view_schedule_from_records_workflow(test_date)
    if schedule:
        print(f"\nSchedule retrieved successfully for {test_date}")
    else:
        print("\nFailed to retrieve schedule.")
