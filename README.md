# Veterinary Clinic Management System

A Python CLI application for managing a veterinary clinic's clients, animals, properties, and appointments.

## Features

This application addresses all six project objectives:

1. **Unified Records**: Single application holding client records, their animals, and properties
2. **Work Type Support**: Consultations attached to animals, farm visits attached to properties
3. **Time Validation**: Prevents consultations outside clinic hours
4. **Day View**: Shows 15-minute slot availability and farm visit schedule
5. **Offline Capability**: Functions without internet connection using JSON file storage
6. **No-Show Tracking**: Mark appointments as DNA (Did Not Attend) for rate reporting

## Scope Features

- **Client Management**: Create, find, update, and deactivate client records
- **Animal & Property Records**: Record animals and properties against clients
- **Consultation Booking**: Book, move, cancel in-clinic consultations in 15-minute slots
- **Farm Visit Booking**: Book, move, cancel farm visits with estimated duration
- **Animal Search**: Search for animals by name across all clients
- **Day Schedule View**: View daily appointment availability
- **Appointment Status**: Mark as completed, cancelled, or no-show (DNA)
- **Reporting**: Basic statistics on appointment completion rates

## Requirements

- Python 3.7 or higher
- No external dependencies (uses only Python standard library)

## Installation

1. Clone or download this repository
2. Navigate to the project directory
3. Run the application:
   ```bash
   python main.py
   ```

## Usage

### Main Menu

The application starts with a main menu offering the following options:

1. **Client Management** - Create, find, update, deactivate, and list clients
2. **Animal Management** - Create, find, and list animals
3. **Property Management** - Create, find, and list properties
4. **Book Consultation** - Schedule in-clinic appointments
5. **Book Farm Visit** - Schedule on-site farm visits
6. **View Day Schedule** - See appointment availability for a specific day
7. **Manage Appointments** - Move, cancel, or update appointment status
8. **Search Animals** - Find animals by name across all clients
9. **Generate Reports** - View appointment statistics
0. **Exit** - Close the application

### Typical Workflow

1. **Create a Client**: Use Client Management → Create Client
2. **Add Animals/Properties**: Use Animal/Property Management to add records
3. **Book Appointments**: Book consultations or farm visits as needed
4. **View Schedule**: Check daily availability using Day Schedule view
5. **Manage Appointments**: Update status (completed/DNA/cancelled) as they occur
6. **Generate Reports**: View statistics on clinic performance

### Data Storage

The application uses JSON file (`clinic_data.json`) for local storage. The data file is automatically created on first run with the structure defined in `schema.json`.

### JSON Schema

The application uses a JSON schema to define the data structure. The schema file (`schema.json`) specifies:

- **clients**: Array of client records with contact information
- **animals**: Array of animal records linked to clients
- **properties**: Array of property records linked to clients  
- **appointments**: Array of appointment records (consultations and farm visits)
- **clinic_hours**: Array of clinic operating hours for each day

The schema ensures data integrity and provides documentation for the data structure.

### Clinic Hours

Default clinic hours are Monday-Friday, 9:00 AM - 5:00 PM. Consultations can only be booked during these hours.

### Time Slots

- Consultations are booked in 15-minute increments
- Farm visits use estimated duration in hours
- The system prevents double-booking of consultation slots

## Data Model

The data model is defined in `schema.json` and stored in `clinic_data.json`.

### Clients
- id (integer): Unique identifier
- name (string): Client full name
- phone (string, optional): Phone number
- email (string, optional): Email address
- address (string, optional): Physical address
- active (boolean): Whether client is active
- created_at (string): ISO format timestamp

### Animals
- id (integer): Unique identifier
- name (string): Animal name
- species (string): Animal species
- breed (string, optional): Animal breed
- client_id (integer): Reference to client
- active (boolean): Whether animal is active
- created_at (string): ISO format timestamp

### Properties
- id (integer): Unique identifier
- address (string): Property address
- client_id (integer): Reference to client
- active (boolean): Whether property is active
- created_at (string): ISO format timestamp

### Appointments
- id (integer): Unique identifier
- type (string): "consultation" or "farm_visit"
- animal_id (integer, optional): Reference to animal (for consultations)
- property_id (integer, optional): Reference to property (for farm visits)
- client_id (integer): Reference to client
- date (string): Date in YYYY-MM-DD format
- time (string): Time in HH:MM format (24-hour)
- duration_minutes (integer): Duration in minutes
- status (string): "booked", "completed", "cancelled", or "dna"
- notes (string, optional): Additional notes
- created_at (string): ISO format timestamp

### Clinic Hours
- day_of_week (integer): 0=Monday, 6=Sunday
- start_time (string): Opening time in HH:MM format
- end_time (string): Closing time in HH:MM format

## Offline Capability

This application is designed to work completely offline:
- No internet connection required
- All data stored locally in JSON file (`clinic_data.json`)
- No external API calls or cloud services
- Simple file-based storage for easy backup and transfer

## Reporting

The reporting feature provides:
- Total appointments booked
- Completed, cancelled, and no-show counts
- Completion rate percentage
- No-show rate percentage
- Cancellation rate percentage

These metrics help the clinic owner measure performance and identify areas for improvement.

## Example Session

```
1. Create Client: John Smith, phone: 555-1234
2. Create Animal: Buddy (dog) for John Smith
3. Book Consultation: Buddy on 2026-09-25 at 09:00
4. View Day Schedule: 2026-09-25
5. Update Appointment Status: Mark consultation as completed
6. Generate Report: View statistics for the week
```

## JSON Schema File

The `schema.json` file defines the structure and validation rules for the data stored in `clinic_data.json`. It follows the JSON Schema draft-07 specification and includes:

- **Type definitions** for all data fields
- **Required field validation** 
- **Enum constraints** for status and type fields
- **Pattern validation** for time formats
- **Relationship documentation** between entities

This schema serves as:
- Documentation for the data structure
- Validation reference for data integrity
- Contract definition for the application's data model

You can validate your data file against the schema using JSON schema validators if needed.

## Technical Details

- **Data Storage**: JSON file (clinic_data.json) with schema validation (schema.json)
- **Interface**: Command-line menu system
- **Date/Time**: Python datetime module
- **Validation**: Input validation for all data entry
- **Error Handling**: Graceful error messages for invalid operations
- **JSON Schema**: Uses JSON Schema draft-07 for data structure validation

## Troubleshooting

If you encounter issues:
- Ensure Python 3.7+ is installed
- Check that you have write permissions in the directory
- Delete `clinic_data.json` to start with fresh data
- Verify `schema.json` exists and is valid JSON
- Run with `python main.py` from the project directory

## Future Enhancements

Potential improvements for future versions:
- Export data to CSV/Excel
- Recurring appointments
- Staff management
- Inventory tracking
- Billing/invoicing
- Email/SMS reminders
- Advanced reporting with charts
