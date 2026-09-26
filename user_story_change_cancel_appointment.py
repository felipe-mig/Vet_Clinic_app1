#!/usr/bin/env python3
"""
User Story: Change or Cancel appointment
This module contains all functions related to changing (moving) or canceling appointments.
"""

from datetime import datetime, timedelta
from typing import List, Optional, Dict


class AppointmentChangeManager:
    """Manages appointment change and cancel operations."""

    def __init__(self, data_manager, client_manager, animal_manager, property_manager):
        """Initialize with required manager instances."""
        self.data_manager = data_manager
        self.client_manager = client_manager
        self.animal_manager = animal_manager
        self.property_manager = property_manager

    def get_clinic_hours(self, day_of_week: int) -> Optional[Dict]:
        """Get clinic hours for a specific day (0=Monday, 6=Sunday)."""
        for hours in self.data_manager.data['clinic_hours']:
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

    def get_slot_conflicts(self, date: str, time: str, duration_minutes: int = 15,
                          exclude_appointment_id: int = None) -> List[Dict]:
        """Check for conflicting appointments in the same time slot."""
        conflicts = []
        start_time = time
        end_dt = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M") + timedelta(minutes=duration_minutes)
        end_time = end_dt.strftime("%H:%M")

        for apt in self.data_manager.data['appointments']:
            if apt['status'] == 'cancelled':
                continue
            if apt['type'] != 'consultation':
                continue
            if apt['date'] != date:
                continue
            if exclude_appointment_id and apt['id'] == exclude_appointment_id:
                continue

            # Check for time overlap
            apt_start = apt['time']
            apt_end_dt = datetime.strptime(f"{date} {apt_start}", "%Y-%m-%d %H:%M") + timedelta(minutes=apt['duration_minutes'])
            apt_end = apt_end_dt.strftime("%H:%M")

            # Check if intervals overlap
            if not (end_time <= apt_start or start_time >= apt_end):
                conflicts.append(apt.copy())

        return conflicts

    def move_appointment(self, appointment_id: int, new_date: str, new_time: str) -> bool:
        """
        Move an appointment to a new date/time.
        
        Args:
            appointment_id: The ID of the appointment to move
            new_date: The new date in YYYY-MM-DD format
            new_time: The new time in HH:MM format
            
        Returns:
            bool: True if move was successful, False otherwise
        """
        appointment = None
        for apt in self.data_manager.data['appointments']:
            if apt['id'] == appointment_id:
                appointment = apt
                break

        if not appointment:
            print("Error: Appointment not found.")
            return False

        # Validate clinic hours for consultations
        if appointment['type'] == 'consultation':
            if not self.is_within_clinic_hours(new_date, new_time):
                print("Error: Appointment is outside clinic hours.")
                return False

            # Check for conflicts
            conflicts = self.get_slot_conflicts(new_date, new_time, appointment['duration_minutes'], appointment_id)
            if conflicts:
                print(f"Error: Time slot conflicts with {len(conflicts)} existing appointment(s).")
                return False

        appointment['date'] = new_date
        appointment['time'] = new_time
        self.data_manager._save_data()
        return True

    def cancel_appointment(self, appointment_id: int) -> bool:
        """
        Cancel an appointment.
        
        Args:
            appointment_id: The ID of the appointment to cancel
            
        Returns:
            bool: True if cancellation was successful, False otherwise
        """
        for apt in self.data_manager.data['appointments']:
            if apt['id'] == appointment_id:
                apt['status'] = 'cancelled'
                self.data_manager._save_data()
                return True
        return False

    def get_appointment(self, appointment_id: int) -> Optional[Dict]:
        """Get appointment details."""
        for apt in self.data_manager.data['appointments']:
            if apt['id'] == appointment_id:
                result = apt.copy()
                # Add related information
                client = self.client_manager.find_client(client_id=apt['client_id'])
                if client:
                    result['client_name'] = client['name']

                if apt['animal_id']:
                    animal = self.animal_manager.find_animal(animal_id=apt['animal_id'])
                    if animal:
                        result['animal_name'] = animal['name']

                if apt['property_id']:
                    prop = self.property_manager.find_property(property_id=apt['property_id'])
                    if prop:
                        result['property_address'] = prop['address']

                return result
        return None


# User Interface Functions
def move_appointment_ui(manager):
    """
    User interface for moving an appointment to a new date/time.
    
    Args:
        manager: The clinic manager instance with appointment management capabilities
    """
    print("\n--- Move Appointment ---")
    appointment_id = int(input("Enter appointment ID: "))
    new_date = input("Enter new date (YYYY-MM-DD): ")
    new_time = input("Enter new time (HH:MM): ")

    if manager.move_appointment(appointment_id, new_date, new_time):
        print("Appointment moved successfully.")
    else:
        print("Failed to move appointment.")


def cancel_appointment_ui(manager):
    """
    User interface for canceling an appointment.
    
    Args:
        manager: The clinic manager instance with appointment management capabilities
    """
    print("\n--- Cancel Appointment ---")
    appointment_id = int(input("Enter appointment ID to cancel: "))
    if manager.cancel_appointment(appointment_id):
        print("Appointment cancelled successfully.")
    else:
        print("Failed to cancel appointment.")


def manage_appointments_ui(manager):
    """
    Appointment management submenu with change and cancel options.
    
    Args:
        manager: The clinic manager instance with appointment management capabilities
    """
    while True:
        print("\n--- Appointment Management ---")
        print("1. List Appointments")
        print("2. Move Appointment")
        print("3. Cancel Appointment")
        print("0. Back to Main Menu")

        choice = input("Select option: ")

        if choice == "1":
            date = input("Filter by date (YYYY-MM-DD, leave blank for all): ") or None
            client_id = input("Filter by client ID (leave blank for all): ")
            client_id = int(client_id) if client_id.isdigit() else None
            status = input("Filter by status (booked/completed/cancelled/dna, leave blank for all): ") or None

            appointments = manager.list_appointments(date, client_id, status)
            if appointments:
                print("\nAppointments:")
                for apt in appointments:
                    apt_type = "Consultation" if apt['type'] == 'consultation' else "Farm Visit"
                    details = apt['animal_name'] if apt['type'] == 'consultation' else apt['property_address']
                    print(f"ID: {apt['id']} - {apt_type} - {apt['date']} {apt['time']} - {apt['client_name']} - {details} - Status: {apt['status']}")
            else:
                print("No appointments found.")

        elif choice == "2":
            move_appointment_ui(manager)

        elif choice == "3":
            cancel_appointment_ui(manager)

        elif choice == "0":
            break

        else:
            print("Invalid option.")


# Integration with main ClinicManager class
class ClinicManagerChangeIntegration:
    """Integration layer for appointment change and cancel operations in the main ClinicManager."""

    def __init__(self, data_manager, client_manager, animal_manager, property_manager):
        """Initialize with required managers."""
        self.data_manager = data_manager
        self.client_manager = client_manager
        self.animal_manager = animal_manager
        self.property_manager = property_manager
        self.appointment_change_manager = AppointmentChangeManager(
            data_manager, client_manager, animal_manager, property_manager
        )

    def move_appointment(self, appointment_id: int, new_date: str, new_time: str) -> bool:
        """
        Move an appointment through the main manager interface.
        
        Args:
            appointment_id: The ID of the appointment to move
            new_date: The new date in YYYY-MM-DD format
            new_time: The new time in HH:MM format
            
        Returns:
            bool: True if successful, False otherwise
        """
        return self.appointment_change_manager.move_appointment(appointment_id, new_date, new_time)

    def cancel_appointment(self, appointment_id: int) -> bool:
        """
        Cancel an appointment through the main manager interface.
        
        Args:
            appointment_id: The ID of the appointment to cancel
            
        Returns:
            bool: True if successful, False otherwise
        """
        return self.appointment_change_manager.cancel_appointment(appointment_id)

    def get_appointment(self, appointment_id: int) -> Optional[Dict]:
        """
        Get appointment details through the main manager interface.
        
        Args:
            appointment_id: The ID of the appointment to retrieve
            
        Returns:
            Dict: Appointment details if found, None otherwise
        """
        return self.appointment_change_manager.get_appointment(appointment_id)


# Example usage and testing
if __name__ == "__main__":
    print("User Story: Change or Cancel appointment")
    print("=" * 60)
    print("\nThis module provides functionality to:")
    print("1. Move/change appointments to new date and time")
    print("2. Cancel appointments")
    print("3. Validate clinic hours for consultation changes")
    print("4. Check for time slot conflicts when moving appointments")
    print("\nMain functions:")
    print("- AppointmentChangeManager.move_appointment()")
    print("- AppointmentChangeManager.cancel_appointment()")
    print("- move_appointment_ui()")
    print("- cancel_appointment_ui()")
    print("- manage_appointments_ui()")
    print("- ClinicManagerChangeIntegration class")
