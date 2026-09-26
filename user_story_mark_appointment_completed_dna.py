#!/usr/bin/env python3
"""
User Story: Mark an appointment as completed or DNA
This module contains all functions related to marking appointments as completed or DNA (Did Not Attend).
"""

from typing import Optional, Dict


class AppointmentStatusManager:
    """Manages appointment status operations for marking appointments as completed or DNA."""

    def __init__(self, data_manager):
        """Initialize with required data manager instance."""
        self.data_manager = data_manager

    def update_appointment_status(self, appointment_id: int, status: str) -> bool:
        """
        Update appointment status (completed, cancelled, dna).
        
        Args:
            appointment_id: The ID of the appointment to update
            status: The new status (must be one of: booked, completed, cancelled, dna)
            
        Returns:
            bool: True if update was successful, False otherwise
        """
        valid_statuses = ['booked', 'completed', 'cancelled', 'dna']
        if status not in valid_statuses:
            print(f"Error: Invalid status. Must be one of: {', '.join(valid_statuses)}")
            return False

        for apt in self.data_manager.data['appointments']:
            if apt['id'] == appointment_id:
                apt['status'] = status
                self.data_manager._save_data()
                return True
        return False


def update_appointment_status_ui(manager):
    """
    User interface for updating appointment status.
    Allows marking appointments as completed or DNA (Did Not Attend).
    
    Args:
        manager: The clinic manager instance with appointment management capabilities
    """
    print("\n--- Update Appointment Status ---")
    appointment_id = int(input("Enter appointment ID: "))
    print("Valid statuses: booked, completed, cancelled, dna")
    status = input("Enter new status: ")

    if manager.update_appointment_status(appointment_id, status):
        print("Appointment status updated successfully.")
    else:
        print("Failed to update appointment status.")


# Integration with main ClinicManager class
class ClinicManagerStatusIntegration:
    """Integration layer for appointment status management in the main ClinicManager."""

    def __init__(self, data_manager):
        """Initialize with data manager."""
        self.data_manager = data_manager
        self.appointment_status_manager = AppointmentStatusManager(data_manager)

    def update_appointment_status(self, appointment_id: int, status: str) -> bool:
        """
        Update appointment status through the main manager interface.
        
        Args:
            appointment_id: The ID of the appointment to update
            status: The new status to set
            
        Returns:
            bool: True if successful, False otherwise
        """
        return self.appointment_status_manager.update_appointment_status(appointment_id, status)


# Example usage and testing
if __name__ == "__main__":
    print("User Story: Mark an appointment as completed or DNA")
    print("=" * 60)
    print("\nThis module provides functionality to:")
    print("1. Mark appointments as 'completed'")
    print("2. Mark appointments as 'dna' (Did Not Attend)")
    print("3. Update appointment status to other valid states")
    print("\nValid statuses: booked, completed, cancelled, dna")
    print("\nMain functions:")
    print("- AppointmentStatusManager.update_appointment_status()")
    print("- update_appointment_status_ui()")
    print("- ClinicManagerStatusIntegration.update_appointment_status()")
