#!/usr/bin/env python3
"""
Integrated View Schedule Workflow
Combines both user stories: Select Date for Schedule View and View Schedule from Clinic Records
This demonstrates the complete end-to-end process of viewing a day's schedule.
"""

from user_story_select_date_for_schedule import select_date_for_schedule_workflow
from user_story_view_schedule_from_records import view_schedule_from_records_workflow


def complete_view_schedule_workflow(data_path: str = "clinic_data.json"):
    """
    Complete workflow for viewing a day's schedule.
    This integrates both user stories into a seamless process.
    """
    print("="*60)
    print("VIEW DAY SCHEDULE WORKFLOW")
    print("="*60)
    print("This process involves two steps:")
    print("1. Select the date to view")
    print("2. Retrieve and display the schedule from records")
    print("="*60)

    # Step 1: Select Date for Schedule View (User Story 1)
    print("\n--- STEP 1: Select Date for Schedule View ---")
    selected_date = select_date_for_schedule_workflow()

    if not selected_date:
        print("\nDate selection failed or was cancelled.")
        print("Workflow terminated.")
        return None

    print(f"\nSelected date: {selected_date}")

    # Step 2: View Schedule from Clinic Records (User Story 2)
    print("\n--- STEP 2: View Schedule from Clinic Records ---")
    schedule = view_schedule_from_records_workflow(selected_date, data_path)

    if schedule:
        print("\n" + "="*60)
        print("VIEW DAY SCHEDULE WORKFLOW COMPLETED SUCCESSFULLY")
        print("="*60)
        print(f"Schedule displayed for: {selected_date}")
        print(f"Total appointments: {len(schedule['consultations']) + len(schedule['farm_visits'])}")
        print("="*60)
        return schedule
    else:
        print("\n" + "="*60)
        print("VIEW DAY SCHEDULE WORKFLOW FAILED")
        print("="*60)
        print("The date was selected but the schedule could not be retrieved.")
        print("="*60)
        return None


def main():
    """Main entry point for the integrated view schedule workflow."""
    print("\nWelcome to the Veterinary Clinic Management System")
    print("View Day Schedule Module\n")

    while True:
        print("\nOptions:")
        print("1. View a day's schedule (complete workflow)")
        print("2. Exit")

        choice = input("Select option (1-2): ").strip()

        if choice == "1":
            complete_view_schedule_workflow()
        elif choice == "2":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
