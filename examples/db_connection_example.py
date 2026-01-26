"""
Database Connection Manager Demo

This example demonstrates:
- Connection management with multiple database types
- Test connection functionality
- ListView display
- CRUD operations for connections
"""

import sys
import os

# Add project root to path
_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.abspath(os.path.join(_current_dir, '..'))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from winformpy.ui_elements.db_connection.db_connection_ui import DBConnectionUI
from winformpy.ui_elements.db_connection.db_connection_manager import DBConnectionManager


class DemoStorageBackend:
    """
    Demo backend with sample database connections.
    
    In production, the backend is provided externally.
    """
    def __init__(self):
        self._data = {
            'demo-oracle': {
                'type': 'oracle',
                'host': 'db-server.local',
                'port': '1521',
                'service_name': 'ORCL',
                'user': 'admin',
                'password': 'secret123',
                'schema': 'HR'
            },
            'demo-mysql': {
                'type': 'mysql',
                'host': 'localhost',
                'port': '3306',
                'database': 'demo_db',
                'user': 'root',
                'password': 'demo123',
                'schema': ''
            },
            'demo-postgres': {
                'type': 'postgresql',
                'host': '192.168.1.50',
                'port': '5432',
                'database': 'postgres',
                'user': 'postgres',
                'password': 'postgres',
                'schema': 'public'
            }
        }
    
    def save(self, name: str, data: dict) -> str:
        """Save a connection configuration."""
        self._data[name] = data.copy()
        return name
    
    def read(self, name: str) -> dict:
        """Read a connection configuration."""
        return self._data.get(name)
    
    def read_all(self) -> dict:
        """Read all connection configurations."""
        return self._data.copy()
    
    def delete(self, name: str) -> bool:
        """Delete a connection configuration."""
        if name in self._data:
            del self._data[name]
            return True
        return False
    
    def list_names(self) -> list:
        """List all connection configuration names."""
        return list(self._data.keys())
    
    def test_connection(self, conn_data: dict) -> tuple:
        """
        Test database connectivity.
        
        Returns:
            tuple[bool, str]: (success, message)
        """
        db_type = conn_data.get('type', '').lower()
        host = conn_data.get('host', '')
        
        # Demo: simulate connection test
        if host == 'localhost' or host.startswith('192.168.') or host.endswith('.local'):
            return True, f"Connection to {db_type} at {host} successful (demo)."
        else:
            return False, f"Cannot reach {host} (demo simulation)."


def main():
    """Run database connection manager demo."""
    print("=" * 50)
    print("  DATABASE CONNECTION MANAGER - DEMO")
    print("=" * 50)
    print()
    print("Architecture:")
    print("  ┌───────────────────────────────┐")
    print("  │  Visual (DBConnectionUI)      │")
    print("  └───────────────┬───────────────┘")
    print("                  │")
    print("  ┌───────────────▼───────────────┐")
    print("  │  DBConnectionManager          │")
    print("  └───────────────┬───────────────┘")
    print("                  │")
    print("  ┌───────────────▼───────────────┐")
    print("  │  Storage Backend (External)   │")
    print("  └───────────────────────────────┘")
    print()
    
    # Layer 1: External backend
    backend = DemoStorageBackend()
    
    # Layer 2: Manager (service layer)
    manager = DBConnectionManager(backend)
    
    # Layer 3: Visual UI with ListView
    ui = DBConnectionUI(manager, {'Text': "Database Connection Manager - DEMO"})
    
    # Show visual interface
    ui.show_dialog()
    
    print()
    print("Demo finished.")


if __name__ == "__main__":
    main()
