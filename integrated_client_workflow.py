#!/usr/bin/env python3
"""
Integrated Client Addition Workflow
Combines both user stories: Add Clients Detail and Add Client to Clinic Records
This demonstrates the complete end-to-end process of adding a new client.
"""

from user_story_add_clients_detail import add_client_detail_workflow
from user_story_add_client_to_clinic_records import add_client_to_clinic_records_workflow


def complete_client_addition_workflow(data_path: str = "clinic_data.json"):
    """
    Complete workflow for adding a new client to the clinic system.
    This integrates both user stories into a seamless process.
    """
    print("="*60)
    print("CLIENT ADDITION WORKFLOW")
    print("="*60)
    print("This process involves two steps:")
    print("1. Collect and validate client details")
    print("2. Add client to clinic records")
    print("="*60)

    # Step 1: Add Clients Detail (User Story 1)
    print("\n--- STEP 1: Add Clients Detail ---")
    client_details = add_client_detail_workflow()

    if not client_details:
        print("\nClient detail collection failed or was cancelled.")
        print("Workflow terminated.")
        return None

    # Step 2: Add Client to Clinic Records (User Story 2)
    print("\n--- STEP 2: Add Client to Clinic Records ---")
    client_id = add_client_to_clinic_records_workflow(client_details, data_path)

    if client_id:
        print("\n" + "="*60)
        print("CLIENT ADDITION WORKFLOW COMPLETED SUCCESSFULLY")
        print("="*60)
        print(f"Client Name: {client_details['name']}")
        print(f"Client ID: {client_id}")
        print(f"Phone: {client_details.get('phone') or 'Not provided'}")
        print(f"Email: {client_details.get('email') or 'Not provided'}")
        print(f"Address: {client_details.get('address') or 'Not provided'}")
        print("="*60)
        return client_id
    else:
        print("\n" + "="*60)
        print("CLIENT ADDITION WORKFLOW FAILED")
        print("="*60)
        print("The client details were collected but could not be added to records.")
        print("="*60)
        return None


def main():
    """Main entry point for the integrated client addition workflow."""
    print("\nWelcome to the Veterinary Clinic Management System")
    print("Client Addition Module\n")

    while True:
        print("\nOptions:")
        print("1. Add a new client (complete workflow)")
        print("2. Exit")

        choice = input("Select option (1-2): ").strip()

        if choice == "1":
            complete_client_addition_workflow()
        elif choice == "2":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
