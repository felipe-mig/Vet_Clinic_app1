#!/usr/bin/env python3
"""
Client Management Module
Handles client CRUD operations.
"""

from datetime import datetime
from typing import List, Optional, Dict


class ClientManager:
    """Manages client operations."""

    def __init__(self, data_manager):
        """Initialize with data manager instance."""
        self.data_manager = data_manager

    def create_client(self, name: str, phone: str = None, email: str = None, address: str = None) -> int:
        """Create a new client and return their ID."""
        client_id = self.data_manager._get_next_id(self.data_manager.data['clients'])
        client = {
            "id": client_id,
            "name": name,
            "phone": phone,
            "email": email,
            "address": address,
            "active": True,
            "created_at": datetime.now().isoformat()
        }
        self.data_manager.data['clients'].append(client)
        self.data_manager._save_data()
        return client_id

    def find_client(self, client_id: int = None, name: str = None) -> Optional[Dict]:
        """Find a client by ID or name."""
        if client_id:
            for client in self.data_manager.data['clients']:
                if client['id'] == client_id and client['active']:
                    return client.copy()
        elif name:
            for client in self.data_manager.data['clients']:
                if name.lower() in client['name'].lower() and client['active']:
                    return client.copy()
        return None

    def update_client(self, client_id: int, name: str = None, phone: str = None,
                     email: str = None, address: str = None) -> bool:
        """Update client information."""
        for client in self.data_manager.data['clients']:
            if client['id'] == client_id:
                if name:
                    client['name'] = name
                if phone:
                    client['phone'] = phone
                if email:
                    client['email'] = email
                if address:
                    client['address'] = address
                self.data_manager._save_data()
                return True
        return False

    def deactivate_client(self, client_id: int) -> bool:
        """Deactivate a client (soft delete)."""
        for client in self.data_manager.data['clients']:
            if client['id'] == client_id:
                client['active'] = False
                self.data_manager._save_data()
                return True
        return False

    def list_clients(self) -> List[Dict]:
        """List all active clients."""
        return [client.copy() for client in self.data_manager.data['clients'] if client['active']]
