#!/usr/bin/env python3
"""
Appointment Management Module
Handles appointment operations including consultations and farm visits.
"""

from datetime import datetime, timedelta
from typing import List, Optional, Dict


class AppointmentManager:
    """Manages appointment operations."""

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

    def create_consultation(self, client_id: int, animal_id: int, date: str, time: str,
                           duration_minutes: int = 15, notes: str = None) -> Optional[int]:
        """Create a consultation appointment."""
        # Validate clinic hours
        if not self.is_within_clinic_hours(date, time):
            print("Error: Appointment is outside clinic hours.")
            return None

        # Validate 15-minute slots
        if duration_minutes % 15 != 0:
            print("Error: Consultation duration must be in 15-minute increments.")
            return None

        # Check for conflicts
        conflicts = self.get_slot_conflicts(date, time, duration_minutes)
        if conflicts:
            print(f"Error: Time slot conflicts with {len(conflicts)} existing appointment(s).")
            return None

        appointment_id = self.data_manager._get_next_id(self.data_manager.data['appointments'])
        appointment = {
            "id": appointment_id,
            "type": "consultation",
            "animal_id": animal_id,
            "property_id": None,
            "client_id": client_id,
            "date": date,
            "time": time,
            "duration_minutes": duration_minutes,
            "status": "booked",
            "notes": notes,
            "created_at": datetime.now().isoformat()
        }
        self.data_manager.data['appointments'].append(appointment)
        self.data_manager._save_data()
        return appointment_id

    def create_farm_visit(self, client_id: int, property_id: int, date: str, time: str,
                         duration_hours: float, notes: str = None) -> Optional[int]:
        """Create a farm visit appointment."""
        duration_minutes = int(duration_hours * 60)

        appointment_id = self.data_manager._get_next_id(self.data_manager.data['appointments'])
        appointment = {
            "id": appointment_id,
            "type": "farm_visit",
            "animal_id": None,
            "property_id": property_id,
            "client_id": client_id,
            "date": date,
            "time": time,
            "duration_minutes": duration_minutes,
            "status": "booked",
            "notes": notes,
            "created_at": datetime.now().isoformat()
        }
        self.data_manager.data['appointments'].append(appointment)
        self.data_manager._save_data()
        return appointment_id

    def move_appointment(self, appointment_id: int, new_date: str, new_time: str) -> bool:
        """Move an appointment to a new date/time."""
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
        """Cancel an appointment."""
        for apt in self.data_manager.data['appointments']:
            if apt['id'] == appointment_id:
                apt['status'] = 'cancelled'
                self.data_manager._save_data()
                return True
        return False

    def update_appointment_status(self, appointment_id: int, status: str) -> bool:
        """Update appointment status (completed, cancelled, dna)."""
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

    def list_appointments(self, date: str = None, client_id: int = None, status: str = None) -> List[Dict]:
        """List appointments with optional filters."""
        results = []
        for apt in self.data_manager.data['appointments']:
            # Apply filters
            if date and apt['date'] != date:
                continue
            if client_id and apt['client_id'] != client_id:
                continue
            if status and apt['status'] != status:
                continue

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

            results.append(result)

        # Sort by date and time
        results.sort(key=lambda x: (x['date'], x['time']))
        return results

    def get_day_schedule(self, date: str) -> Dict:
        """Get day schedule with 15-minute slots and farm visits."""
        # Get all consultations for the day
        consultations = self.list_appointments(date=date, status='booked')
        consultations = [a for a in consultations if a['type'] == 'consultation']

        # Get all farm visits for the day
        farm_visits = self.list_appointments(date=date, status='booked')
        farm_visits = [a for a in farm_visits if a['type'] == 'farm_visit']

        # Get clinic hours for the day
        dt = datetime.strptime(date, "%Y-%m-%d")
        day_of_week = dt.weekday()
        hours = self.get_clinic_hours(day_of_week)

        # Generate 15-minute slots
        slots = []
        if hours:
            start = datetime.strptime(f"{date} {hours['start_time']}", "%Y-%m-%d %H:%M")
            end = datetime.strptime(f"{date} {hours['end_time']}", "%Y-%m-%d %H:%M")

            current = start
            while current < end:
                slot_time = current.strftime("%H:%M")
                slot_end = (current + timedelta(minutes=15)).strftime("%H:%M")

                # Check if slot is booked
                booked = False
                appointment = None
                for cons in consultations:
                    cons_time = cons['time']
                    cons_end_dt = datetime.strptime(f"{date} {cons_time}", "%Y-%m-%d %H:%M") + timedelta(minutes=cons['duration_minutes'])
                    cons_end = cons_end_dt.strftime("%H:%M")

                    if cons_time <= slot_time < cons_end:
                        booked = True
                        appointment = cons
                        break

                slots.append({
                    'time': slot_time,
                    'end_time': slot_end,
                    'booked': booked,
                    'appointment': appointment
                })

                current += timedelta(minutes=15)

        return {
            'date': date,
            'clinic_hours': hours,
            'slots': slots,
            'farm_visits': farm_visits
        }
