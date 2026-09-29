#!/usr/bin/env python3
"""
Integrated Book Farm Visit Workflow
Combines both user stories: Collect Farm Visit Details and Book Farm Visit to Clinic Records
This demonstrates the complete end-to-end process of booking a farm visit.
"""

from user_story_collect_farm_visit_details import collect_farm_visit_details_workflow
from user_story_book_farm_visit_to_records import book_farm_visit_to_records_workflow


def complete_book_farm_visit_workflow(data_path: str = "clinic_data.json"):
    """
    Complete workflow for booking a farm visit.
    This integrates both user stories into a seamless process.
    """
    print("="*60)
    print("BOOK FARM VISIT WORKFLOW")
    print("="*60)
    print("This process involves two steps:")
    print("1. Collect farm visit booking details")
    print("2. Book farm visit to clinic records")
    print("="*60)

    # Step 1: Collect Farm Visit Details (User Story 1)
    print("\n--- STEP 1: Collect Farm Visit Details ---")
    farm_visit_details = collect_farm_visit_details_workflow(data_path)

    if not farm_visit_details:
        print("\nFarm visit detail collection failed or was cancelled.")
        print("Workflow terminated.")
        return None

    print(f"\nCollected farm visit details for:")
    print(f"Client: {farm_visit_details['client_name']}")
    print(f"Property: {farm_visit_details['property_address']} ({farm_visit_details['property_type']})")
    print(f"Date/Time: {farm_visit_details['date']} at {farm_visit_details['time']}")
    print(f"Duration: {farm_visit_details['duration_hours']} hours")

    # Step 2: Book Farm Visit to Clinic Records (User Story 2)
    print("\n--- STEP 2: Book Farm Visit to Clinic Records ---")
    appointment_id = book_farm_visit_to_records_workflow(farm_visit_details, data_path)

    if appointment_id:
        print("\n" + "="*60)
        print("BOOK FARM VISIT WORKFLOW COMPLETED SUCCESSFULLY")
        print("="*60)
        print(f"Client: {farm_visit_details['client_name']} (ID: {farm_visit_details['client_id']})")
        print(f"Property: {farm_visit_details['property_address']} - {farm_visit_details['property_type']} (ID: {farm_visit_details['property_id']})")
        print(f"Appointment ID: {appointment_id}")
        print(f"Date: {farm_visit_details['date']}")
        print(f"Time: {farm_visit_details['time']}")
        print(f"Duration: {farm_visit_details['duration_hours']} hours")
        print(f"Status: Booked")
        print(f"Notes: {farm_visit_details.get('notes') or 'None'}")
        print("="*60)
        return appointment_id
    else:
        print("\n" + "="*60)
        print("BOOK FARM VISIT WORKFLOW FAILED")
        print("="*60)
        print("The farm visit details were collected but could not be booked.")
        print("="*60)
        return None


def main():
    """Main entry point for the integrated book farm visit workflow."""
    print("\nWelcome to the Veterinary Clinic Management System")
    print("Book Farm Visit Module\n")

    while True:
        print("\nOptions:")
        print("1. Book a new farm visit (complete workflow)")
        print("2. Exit")

        choice = input("Select option (1-2): ").strip()

        if choice == "1":
            complete_book_farm_visit_workflow()
        elif choice == "2":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
