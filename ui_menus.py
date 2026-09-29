#!/usr/bin/env python3
"""
UI Menus Module
Contains all menu and user interface functions.
"""


def print_menu():
    """Print the main menu."""
    print("\n" + "="*50)
    print("VETERINARY CLINIC MANAGEMENT SYSTEM")
    print("="*50)
    print("1. Client Management")
    print("2. Animal Management")
    print("3. Property Management")
    print("4. Book Consultation")
    print("5. Book Farm Visit")
    print("6. View Day Schedule")
    print("7. Manage Appointments")
    print("8. Search Animals")
    print("9. Generate Reports")
    print("0. Exit")
    print("="*50)


def client_menu(manager):
    """Client management submenu."""
    while True:
        print("\n--- Client Management ---")
        print("1. Create Client")
        print("2. Find Client")
        print("3. Update Client")
        print("4. Deactivate Client")
        print("5. List All Clients")
        print("0. Back to Main Menu")

        choice = input("Select option: ")

        if choice == "1":
            name = input("Client name: ")
            phone = input("Phone (optional): ") or None
            email = input("Email (optional): ") or None
            address = input("Address (optional): ") or None

            client_id = manager.create_client(name, phone, email, address)
            print(f"Client created with ID: {client_id}")

        elif choice == "2":
            search = input("Search by ID (number) or name: ")
            if search.isdigit():
                client = manager.find_client(client_id=int(search))
            else:
                client = manager.find_client(name=search)

            if client:
                print(f"\nClient Found:")
                print(f"ID: {client['id']}")
                print(f"Name: {client['name']}")
                print(f"Phone: {client['phone'] or 'N/A'}")
                print(f"Email: {client['email'] or 'N/A'}")
                print(f"Address: {client['address'] or 'N/A'}")
            else:
                print("Client not found.")

        elif choice == "3":
            client_id = int(input("Enter client ID: "))
            client = manager.find_client(client_id=client_id)
            if not client:
                print("Client not found.")
                continue

            print(f"Current name: {client['name']}")
            name = input("New name (leave blank to keep current): ") or None
            print(f"Current phone: {client['phone'] or 'N/A'}")
            phone = input("New phone (leave blank to keep current): ") or None
            print(f"Current email: {client['email'] or 'N/A'}")
            email = input("New email (leave blank to keep current): ") or None
            print(f"Current address: {client['address'] or 'N/A'}")
            address = input("New address (leave blank to keep current): ") or None

            if manager.update_client(client_id, name, phone, email, address):
                print("Client updated successfully.")
            else:
                print("No changes made.")

        elif choice == "4":
            client_id = int(input("Enter client ID to deactivate: "))
            if manager.deactivate_client(client_id):
                print("Client deactivated successfully.")
            else:
                print("Client not found.")

        elif choice == "5":
            clients = manager.list_clients()
            if clients:
                print("\nAll Clients:")
                for client in clients:
                    print(f"ID: {client['id']} - Name: {client['name']} - Phone: {client['phone'] or 'N/A'}")
            else:
                print("No clients found.")

        elif choice == "0":
            break

        else:
            print("Invalid option.")


def animal_menu(manager):
    """Animal management submenu."""
    while True:
        print("\n--- Animal Management ---")
        print("1. Create Animal")
        print("2. Find Animal")
        print("3. List Animals")
        print("0. Back to Main Menu")

        choice = input("Select option: ")

        if choice == "1":
            client_id = int(input("Enter client ID: "))
            client = manager.find_client(client_id=client_id)
            if not client:
                print("Client not found.")
                continue

            name = input("Animal name: ")
            species = input("Species: ")
            breed = input("Breed (optional): ") or None

            animal_id = manager.create_animal(name, species, client_id, breed)
            print(f"Animal created with ID: {animal_id}")

        elif choice == "2":
            search = input("Search by ID (number) or name: ")
            if search.isdigit():
                animal = manager.find_animal(animal_id=int(search))
            else:
                animal = manager.find_animal(name=search)

            if animal:
                print(f"\nAnimal Found:")
                print(f"ID: {animal['id']}")
                print(f"Name: {animal['name']}")
                print(f"Species: {animal['species']}")
                print(f"Breed: {animal['breed'] or 'N/A'}")
                print(f"Client: {animal.get('client_name', 'N/A')}")
            else:
                print("Animal not found.")

        elif choice == "3":
            client_id = input("Filter by client ID (leave blank for all): ")
            if client_id.isdigit():
                animals = manager.list_animals(client_id=int(client_id))
            else:
                animals = manager.list_animals()

            if animals:
                print("\nAnimals:")
                for animal in animals:
                    print(f"ID: {animal['id']} - Name: {animal['name']} - Species: {animal['species']} - Client: {animal.get('client_name', 'N/A')}")
            else:
                print("No animals found.")

        elif choice == "0":
            break

        else:
            print("Invalid option.")


def property_menu(manager):
    """Property management submenu."""
    while True:
        print("\n--- Property Management ---")
        print("1. Create Property")
        print("2. Find Property")
        print("3. List Properties")
        print("0. Back to Main Menu")

        choice = input("Select option: ")

        if choice == "1":
            client_id = int(input("Enter client ID: "))
            client = manager.find_client(client_id=client_id)
            if not client:
                print("Client not found.")
                continue

            address = input("Property address: ")

            property_id = manager.create_property(address, client_id)
            print(f"Property created with ID: {property_id}")

        elif choice == "2":
            search = input("Search by ID (number) or address: ")
            if search.isdigit():
                prop = manager.find_property(property_id=int(search))
            else:
                prop = manager.find_property(address=search)

            if prop:
                print(f"\nProperty Found:")
                print(f"ID: {prop['id']}")
                print(f"Address: {prop['address']}")
                print(f"Client: {prop.get('client_name', 'N/A')}")
            else:
                print("Property not found.")

        elif choice == "3":
            client_id = input("Filter by client ID (leave blank for all): ")
            if client_id.isdigit():
                properties = manager.list_properties(client_id=int(client_id))
            else:
                properties = manager.list_properties()

            if properties:
                print("\nProperties:")
                for prop in properties:
                    print(f"ID: {prop['id']} - Address: {prop['address']} - Client: {prop.get('client_name', 'N/A')}")
            else:
                print("No properties found.")

        elif choice == "0":
            break

        else:
            print("Invalid option.")


def manage_appointments(manager):
    """Appointment management submenu."""
    while True:
        print("\n--- Appointment Management ---")
        print("1. List Appointments")
        print("2. Move Appointment")
        print("3. Cancel Appointment")
        print("4. Update Appointment Status")
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
            appointment_id = int(input("Enter appointment ID: "))
            new_date = input("Enter new date (YYYY-MM-DD): ")
            new_time = input("Enter new time (HH:MM): ")

            if manager.move_appointment(appointment_id, new_date, new_time):
                print("Appointment moved successfully.")
            else:
                print("Failed to move appointment.")

        elif choice == "3":
            appointment_id = int(input("Enter appointment ID to cancel: "))
            if manager.cancel_appointment(appointment_id):
                print("Appointment cancelled successfully.")
            else:
                print("Failed to cancel appointment.")

        elif choice == "4":
            appointment_id = int(input("Enter appointment ID: "))
            print("Valid statuses: booked, completed, cancelled, dna")
            status = input("Enter new status: ")

            if manager.update_appointment_status(appointment_id, status):
                print("Appointment status updated successfully.")
            else:
                print("Failed to update appointment status.")

        elif choice == "0":
            break

        else:
            print("Invalid option.")


def book_consultation(manager):
    """Book a consultation appointment."""
    print("\n--- Book Consultation ---")

    client_id = int(input("Enter client ID: "))
    client = manager.find_client(client_id=client_id)
    if not client:
        print("Client not found.")
        return

    # List client's animals
    animals = manager.list_animals(client_id=client_id)
    if not animals:
        print("No animals found for this client.")
        return

    print("\nClient's animals:")
    for animal in animals:
        print(f"ID: {animal['id']} - Name: {animal['name']} - Species: {animal['species']}")

    animal_id = int(input("Enter animal ID: "))
    animal = manager.find_animal(animal_id=animal_id)
    if not animal:
        print("Animal not found.")
        return

    date = input("Enter date (YYYY-MM-DD): ")
    time = input("Enter time (HH:MM, 24-hour format): ")

    duration = input("Enter duration in minutes (default 15): ")
    duration = int(duration) if duration else 15

    notes = input("Notes (optional): ") or None

    appointment_id = manager.create_consultation(client_id, animal_id, date, time, duration, notes)
    if appointment_id:
        print(f"Consultation booked successfully with ID: {appointment_id}")
    else:
        print("Failed to book consultation.")


def book_farm_visit(manager):
    """Book a farm visit appointment."""
    print("\n--- Book Farm Visit ---")

    client_id = int(input("Enter client ID: "))
    client = manager.find_client(client_id=client_id)
    if not client:
        print("Client not found.")
        return

    # List client's properties
    properties = manager.list_properties(client_id=client_id)
    if not properties:
        print("No properties found for this client.")
        return

    print("\nClient's properties:")
    for prop in properties:
        print(f"ID: {prop['id']} - Address: {prop['address']}")

    property_id = int(input("Enter property ID: "))
    prop = manager.find_property(property_id=property_id)
    if not prop:
        print("Property not found.")
        return

    date = input("Enter date (YYYY-MM-DD): ")
    time = input("Enter time (HH:MM, 24-hour format): ")
    duration_hours = float(input("Enter estimated duration in hours: "))

    notes = input("Notes (optional): ") or None

    appointment_id = manager.create_farm_visit(client_id, property_id, date, time, duration_hours, notes)
    if appointment_id:
        print(f"Farm visit booked successfully with ID: {appointment_id}")
    else:
        print("Failed to book farm visit.")


def view_day_schedule(manager):
    """View the day schedule."""
    print("\n--- View Day Schedule ---")

    date = input("Enter date (YYYY-MM-DD): ")
    schedule = manager.get_day_schedule(date)

    print(f"\nSchedule for {date}")
    print("="*50)

    if schedule['clinic_hours']:
        print(f"Clinic Hours: {schedule['clinic_hours']['start_time']} - {schedule['clinic_hours']['end_time']}")
    else:
        print("Clinic closed on this day")

    print("\n15-Minute Slots:")
    print("-" * 50)
    for slot in schedule['slots']:
        status = "BOOKED" if slot['booked'] else "FREE"
        print(f"{slot['time']} - {slot['end_time']}: {status}")
        if slot['appointment']:
            print(f"  -> {slot['appointment']['client_name']} - {slot['appointment']['animal_name']}")

    if schedule['farm_visits']:
        print("\nFarm Visits:")
        print("-" * 50)
        for visit in schedule['farm_visits']:
            duration_hours = visit['duration_minutes'] / 60
            print(f"{visit['time']} - {visit['client_name']} at {visit['property_address']} ({duration_hours}h)")


def search_animals(manager):
    """Search for animals by name across all clients."""
    print("\n--- Search Animals ---")

    name = input("Enter animal name to search: ")
    animals = manager.search_animals_by_name(name)

    if animals:
        print(f"\nFound {len(animals)} animal(s):")
        for animal in animals:
            print(f"ID: {animal['id']} - Name: {animal['name']} - Species: {animal['species']} - Client: {animal['client_name']}")
    else:
        print("No animals found.")


def generate_reports(manager):
    """Generate reports."""
    print("\n--- Generate Reports ---")

    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")

    stats = manager.get_appointment_report(start_date, end_date)

    print(f"\nAppointment Report ({start_date} to {end_date})")
    print("="*50)
    print(f"Total Appointments: {stats['total']}")
    print(f"Completed: {stats['completed']}")
    print(f"Cancelled: {stats['cancelled']}")
    print(f"No-Show (DNA): {stats['dna']}")
    print(f"Still Booked: {stats['booked']}")
    print("-" * 50)
    print(f"Completion Rate: {stats['completion_rate']:.1f}%")
    print(f"No-Show Rate: {stats['dna_rate']:.1f}%")
    print(f"Cancellation Rate: {stats['cancellation_rate']:.1f}%")
