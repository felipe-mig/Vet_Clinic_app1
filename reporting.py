#!/usr/bin/env python3
"""
Reporting Module
Handles report generation and statistics.
"""

from typing import Dict


class ReportingManager:
    """Manages reporting operations."""

    def __init__(self, data_manager):
        """Initialize with data manager instance."""
        self.data_manager = data_manager

    def get_appointment_report(self, start_date: str, end_date: str) -> Dict:
        """Generate appointment statistics report."""
        total = 0
        completed = 0
        cancelled = 0
        dna = 0
        booked = 0

        for apt in self.data_manager.data['appointments']:
            if start_date <= apt['date'] <= end_date:
                total += 1
                if apt['status'] == 'completed':
                    completed += 1
                elif apt['status'] == 'cancelled':
                    cancelled += 1
                elif apt['status'] == 'dna':
                    dna += 1
                elif apt['status'] == 'booked':
                    booked += 1

        # Calculate rates
        if total > 0:
            completion_rate = (completed / total) * 100
            dna_rate = (dna / total) * 100
            cancellation_rate = (cancelled / total) * 100
        else:
            completion_rate = 0
            dna_rate = 0
            cancellation_rate = 0

        return {
            'total': total,
            'completed': completed,
            'cancelled': cancelled,
            'dna': dna,
            'booked': booked,
            'completion_rate': completion_rate,
            'dna_rate': dna_rate,
            'cancellation_rate': cancellation_rate
        }
