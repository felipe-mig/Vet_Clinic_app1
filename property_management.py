#!/usr/bin/env python3
"""
Property Management Module
Handles property CRUD operations.
"""

from datetime import datetime
from typing import List, Optional, Dict


class PropertyManager:
    """Manages property operations."""

    def __init__(self, data_manager, client_manager):
        """Initialize with data manager and client manager instances."""
        self.data_manager = data_manager
        self.client_manager = client_manager

    def create_property(self, address: str, client_id: int) -> int:
        """Create a new property and return its ID."""
        property_id = self.data_manager._get_next_id(self.data_manager.data['properties'])
        prop = {
            "id": property_id,
            "address": address,
            "client_id": client_id,
            "active": True,
            "created_at": datetime.now().isoformat()
        }
        self.data_manager.data['properties'].append(prop)
        self.data_manager._save_data()
        return property_id

    def find_property(self, property_id: int = None, address: str = None, client_id: int = None) -> Optional[Dict]:
        """Find a property by ID, address, or client."""
        if property_id:
            for prop in self.data_manager.data['properties']:
                if prop['id'] == property_id and prop['active']:
                    result = prop.copy()
                    client = self.client_manager.find_client(client_id=prop['client_id'])
                    if client:
                        result['client_name'] = client['name']
                    return result
        elif address:
            for prop in self.data_manager.data['properties']:
                if address.lower() in prop['address'].lower() and prop['active']:
                    result = prop.copy()
                    client = self.client_manager.find_client(client_id=prop['client_id'])
                    if client:
                        result['client_name'] = client['name']
                    return result
        elif client_id:
            for prop in self.data_manager.data['properties']:
                if prop['client_id'] == client_id and prop['active']:
                    result = prop.copy()
                    client = self.client_manager.find_client(client_id=prop['client_id'])
                    if client:
                        result['client_name'] = client['name']
                    return result
        return None

    def list_properties(self, client_id: int = None) -> List[Dict]:
        """List properties, optionally filtered by client."""
        results = []
        for prop in self.data_manager.data['properties']:
            if not prop['active']:
                continue
            if client_id and prop['client_id'] != client_id:
                continue

            result = prop.copy()
            client = self.client_manager.find_client(client_id=prop['client_id'])
            if client and client['active']:
                result['client_name'] = client['name']
                results.append(result)
        return results
