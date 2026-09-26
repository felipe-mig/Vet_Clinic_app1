#!/usr/bin/env python3
"""
Main Application Entry Point
Brings together all the separated modules into a unified application.
"""

from data_management import DataManager
from client_management import ClientManager
from animal_management import AnimalManager
from property_management import PropertyManager
from appointment_management import AppointmentManager
from reporting import ReportingManager
from ui_menus import (
    print_menu,
    client_menu,
    animal_menu,
    property_menu,
    book_consultation,
    book_farm_visit,
    view_day_schedule,
    manage_appointments,
    search_animals,
    generate_reports
)


class ClinicManager:
    """Main clinic management application facade."""

    def __init__(self, data_path: str = "clinic_data.json"):
        """Initialize the clinic manager with all sub-managers."""
        self.data_manager = DataManager(data_path)
        self.client_manager = ClientManager(self.data_manager)
        self.animal_manager = AnimalManager(self.data_manager, self.client_manager)
        self.property_manager = PropertyManager(self.data_manager, self.client_manager)
        self.appointment_manager = AppointmentManager(
            self.data_manager,
            self.client_manager,
            self.animal_manager,
            self.property_manager
        )
        self.reporting_manager = ReportingManager(self.data_manager)

    # Client Management
    def create_client(self, name: str, phone: str = None, email: str = None, address: str = None) -> int:
        return self.client_manager.create_client(name, phone, email, address)

    def find_client(self, client_id: int = None, name: str = None):
        return self.client_manager.find_client(client_id, name)

    def update_client(self, client_id: int, name: str = None, phone: str = None,
                     email: str = None, address: str = None) -> bool:
        return self.client_manager.update_client(client_id, name, phone, email, address)

    def deactivate_client(self, client_id: int) -> bool:
        return self.client_manager.deactivate_client(client_id)

    def list_clients(self):
        return self.client_manager.list_clients()

    # Animal Management
    def create_animal(self, name: str, species: str, client_id: int, breed: str = None) -> int:
        return self.animal_manager.create_animal(name, species, client_id, breed)

    def find_animal(self, animal_id: int = None, name: str = None, client_id: int = None):
        return self.animal_manager.find_animal(animal_id, name, client_id)

    def search_animals_by_name(self, name: str):
        return self.animal_manager.search_animals_by_name(name)

    def list_animals(self, client_id: int = None):
        return self.animal_manager.list_animals(client_id)

    # Property Management
    def create_property(self, address: str, client_id: int) -> int:
        return self.property_manager.create_property(address, client_id)

    def find_property(self, property_id: int = None, address: str = None, client_id: int = None):
        return self.property_manager.find_property(property_id, address, client_id)

    def list_properties(self, client_id: int = None):
        return self.property_manager.list_properties(client_id)

    # Appointment Management
    def create_consultation(self, client_id: int, animal_id: int, date: str, time: str,
                           duration_minutes: int = 15, notes: str = None):
        return self.appointment_manager.create_consultation(client_id, animal_id, date, time, duration_minutes, notes)

    def create_farm_visit(self, client_id: int, property_id: int, date: str, time: str,
                         duration_hours: float, notes: str = None):
        return self.appointment_manager.create_farm_visit(client_id, property_id, date, time, duration_hours, notes)

    def move_appointment(self, appointment_id: int, new_date: str, new_time: str) -> bool:
        return self.appointment_manager.move_appointment(appointment_id, new_date, new_time)

    def cancel_appointment(self, appointment_id: int) -> bool:
        return self.appointment_manager.cancel_appointment(appointment_id)

    def update_appointment_status(self, appointment_id: int, status: str) -> bool:
        return self.appointment_manager.update_appointment_status(appointment_id, status)

    def get_appointment(self, appointment_id: int):
        return self.appointment_manager.get_appointment(appointment_id)

    def list_appointments(self, date: str = None, client_id: int = None, status: str = None):
        return self.appointment_manager.list_appointments(date, client_id, status)

    def get_day_schedule(self, date: str):
        return self.appointment_manager.get_day_schedule(date)

    # Reporting
    def get_appointment_report(self, start_date: str, end_date: str):
        return self.reporting_manager.get_appointment_report(start_date, end_date)

    def close(self):
        """Save data and close."""
        self.data_manager.close()


def main():
    """Main application entry point."""
    manager = ClinicManager()

    try:
        while True:
            print_menu()
            choice = input("Select option: ")

            if choice == "1":
                client_menu(manager)
            elif choice == "2":
                animal_menu(manager)
            elif choice == "3":
                property_menu(manager)
            elif choice == "4":
                book_consultation(manager)
            elif choice == "5":
                book_farm_visit(manager)
            elif choice == "6":
                view_day_schedule(manager)
            elif choice == "7":
                manage_appointments(manager)
            elif choice == "8":
                search_animals(manager)
            elif choice == "9":
                generate_reports(manager)
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Invalid option. Please try again.")

    finally:
        manager.close()


if __name__ == "__main__":
    main()
