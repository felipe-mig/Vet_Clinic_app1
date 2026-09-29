#!/usr/bin/env python3
"""
Integrated Book Consultation Workflow
Combines both user stories: Collect Consultation Details and Book Consultation to Clinic Records
This demonstrates the complete end-to-end process of booking an in-clinic consultation.
"""

from user_story_collect_consultation_details import collect_consultation_details_workflow
from user_story_book_consultation_to_records import book_consultation_to_records_workflow


def complete_book_consultation_workflow(data_path: str = "clinic_data.json"):
    """
    Complete workflow for booking an in-clinic consultation.
    This integrates both user stories into a seamless process.
    """
    print("="*60)
    print("BOOK IN-CLINIC CONSULTATION WORKFLOW")
    print("="*60)
    print("This process involves two steps:")
    print("1. Collect consultation booking details")
    print("2. Book consultation to clinic records")
    print("="*60)

    # Step 1: Collect Consultation Details (User Story 1)
    print("\n--- STEP 1: Collect Consultation Details ---")
    consultation_details = collect_consultation_details_workflow(data_path)

    if not consultation_details:
        print("\nConsultation detail collection failed or was cancelled.")
        print("Workflow terminated.")
        return None

    print(f"\nCollected consultation details for:")
    print(f"Client: {consultation_details['client_name']}")
    print(f"Animal: {consultation_details['animal_name']} ({consultation_details['animal_species']})")
    print(f"Date/Time: {consultation_details['date']} at {consultation_details['time']}")
    print(f"Duration: {consultation_details['duration_minutes']} minutes")

    # Step 2: Book Consultation to Clinic Records (User Story 2)
    print("\n--- STEP 2: Book Consultation to Clinic Records ---")
    appointment_id = book_consultation_to_records_workflow(consultation_details, data_path)

    if appointment_id:
        print("\n" + "="*60)
        print("BOOK IN-CLINIC CONSULTATION WORKFLOW COMPLETED SUCCESSFULLY")
        print("="*60)
        print(f"Client: {consultation_details['client_name']} (ID: {consultation_details['client_id']})")
        print(f"Animal: {consultation_details['animal_name']} - {consultation_details['animal_species']} (ID: {consultation_details['animal_id']})")
        print(f"Appointment ID: {appointment_id}")
        print(f"Date: {consultation_details['date']}")
        print(f"Time: {consultation_details['time']}")
        print(f"Duration: {consultation_details['duration_minutes']} minutes")
        print(f"Status: Booked")
        print(f"Notes: {consultation_details.get('notes') or 'None'}")
        print("="*60)
        return appointment_id
    else:
        print("\n" + "="*60)
        print("BOOK IN-CLINIC CONSULTATION WORKFLOW FAILED")
        print("="*60)
        print("The consultation details were collected but could not be booked.")
        print("="*60)
        return None


def main():
    """Main entry point for the integrated book consultation workflow."""
    print("\nWelcome to the Veterinary Clinic Management System")
    print("Book In-Clinic Consultation Module\n")

    while True:
        print("\nOptions:")
        print("1. Book a new in-clinic consultation (complete workflow)")
        print("2. Exit")

        choice = input("Select option (1-2): ").strip()

        if choice == "1":
            complete_book_consultation_workflow()
        elif choice == "2":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
