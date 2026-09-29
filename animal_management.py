#!/usr/bin/env python3
"""
Animal Management Module
Handles animal CRUD operations.
"""

from datetime import datetime
from typing import List, Optional, Dict


class AnimalManager:
    """Manages animal operations."""

    def __init__(self, data_manager, client_manager):
        """Initialize with data manager and client manager instances."""
        self.data_manager = data_manager
        self.client_manager = client_manager

    def create_animal(self, name: str, species: str, client_id: int, breed: str = None) -> int:
        """Create a new animal and return its ID."""
        animal_id = self.data_manager._get_next_id(self.data_manager.data['animals'])
        animal = {
            "id": animal_id,
            "name": name,
            "species": species,
            "breed": breed,
            "client_id": client_id,
            "active": True,
            "created_at": datetime.now().isoformat()
        }
        self.data_manager.data['animals'].append(animal)
        self.data_manager._save_data()
        return animal_id

    def find_animal(self, animal_id: int = None, name: str = None, client_id: int = None) -> Optional[Dict]:
        """Find an animal by ID, name, or client."""
        if animal_id:
            for animal in self.data_manager.data['animals']:
                if animal['id'] == animal_id and animal['active']:
                    result = animal.copy()
                    # Add client name
                    client = self.client_manager.find_client(client_id=animal['client_id'])
                    if client:
                        result['client_name'] = client['name']
                    return result
        elif name:
            for animal in self.data_manager.data['animals']:
                if name.lower() in animal['name'].lower() and animal['active']:
                    result = animal.copy()
                    client = self.client_manager.find_client(client_id=animal['client_id'])
                    if client:
                        result['client_name'] = client['name']
                    return result
        elif client_id:
            for animal in self.data_manager.data['animals']:
                if animal['client_id'] == client_id and animal['active']:
                    result = animal.copy()
                    client = self.client_manager.find_client(client_id=animal['client_id'])
                    if client:
                        result['client_name'] = client['name']
                    return result
        return None

    def search_animals_by_name(self, name: str) -> List[Dict]:
        """Search for animals by name across all clients."""
        results = []
        for animal in self.data_manager.data['animals']:
            if name.lower() in animal['name'].lower() and animal['active']:
                result = animal.copy()
                client = self.client_manager.find_client(client_id=animal['client_id'])
                if client and client['active']:
                    result['client_name'] = client['name']
                    results.append(result)
        return results

    def list_animals(self, client_id: int = None) -> List[Dict]:
        """List animals, optionally filtered by client."""
        results = []
        for animal in self.data_manager.data['animals']:
            if not animal['active']:
                continue
            if client_id and animal['client_id'] != client_id:
                continue

            result = animal.copy()
            client = self.client_manager.find_client(client_id=animal['client_id'])
            if client and client['active']:
                result['client_name'] = client['name']
                results.append(result)
        return results
