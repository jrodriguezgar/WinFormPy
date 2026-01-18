"""
Example: Database Connection Manager Demo

Demonstrates the DBConnectionManager, DBConnectionUI and DBConnectionPanel
from WinFormPy ui_elements.

This example uses a mock storage backend since the actual storage
backend is external to the project.

Features shown:
- Mock storage backend implementation
- DBConnectionManager usage
- DBConnectionUI form (standalone)
- DBConnectionPanel (embeddable)
- CRUD operations for database connections

Note: In a real application, you would provide your own storage backend
that implements the required interface.
"""

import sys
import os

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from winformpy import Form, Button, Label


# ============================================================
# Mock Storage Backend (for demonstration purposes)
# In production, you would provide your own implementation
# ============================================================

class MockStorageBackend:
    """
    Mock storage backend for demonstration.
    
    In a real application, this would be replaced with your
    actual storage implementation (file-based, database, etc.)
    
    Required methods:
        - save(name, data) -> str ('created' | 'updated')
        - read(name) -> dict | None
        - read_all() -> dict
        - delete(name) -> bool
        - list_names() -> list[str]
    
    Optional method:
        - test_connection(conn_data) -> tuple[bool, str]
    """
    
    def __init__(self):
        # In-memory storage for demo
        self._connections = {
            'Production Oracle': {
                'type': 'oracle',
                'host': 'prod-db.example.com',
                'port': '1521',
                'service_name': 'PRODDB',
                'database': '',
                'user': 'app_user',
                'password': '********',
                'schema': 'APP_SCHEMA'
            },
            'Dev PostgreSQL': {
                'type': 'postgresql',
                'host': 'localhost',
                'port': '5432',
                'database': 'dev_db',
                'user': 'developer',
                'password': '********',
                'schema': 'public'
            },
            'Test MySQL': {
                'type': 'mysql',
                'host': '192.168.1.100',
                'port': '3306',
                'database': 'test_db',
                'user': 'test_user',
                'password': '********',
                'schema': ''
            },
            'Local SQLite': {
                'type': 'sqlite',
                'database': './data/local.db',
                'host': '',
                'port': '',
                'user': '',
                'password': '',
                'schema': ''
            },
            'MongoDB Atlas': {
                'type': 'mongodb',
                'host': 'cluster0.mongodb.net',
                'port': '27017',
                'database': 'myapp',
                'user': 'admin',
                'password': '********',
                'schema': ''
            }
        }
    
    def save(self, name: str, data: dict) -> str:
        """Save or update a connection."""
        action = 'updated' if name in self._connections else 'created'
        self._connections[name] = data.copy()
        print(f"[MockBackend] Connection '{name}' {action}")
        return action
    
    def read(self, name: str) -> dict:
        """Read a specific connection."""
        return self._connections.get(name)
    
    def read_all(self) -> dict:
        """Read all connections."""
        return self._connections.copy()
    
    def delete(self, name: str) -> bool:
        """Delete a connection."""
        if name in self._connections:
            del self._connections[name]
            print(f"[MockBackend] Connection '{name}' deleted")
            return True
        return False
    
    def list_names(self) -> list:
        """Get list of connection names."""
        return list(self._connections.keys())
    
    def test_connection(self, conn_data: dict) -> tuple:
        """
        Mock connection test.
        
        In a real implementation, this would attempt to connect
        to the database and return the result.
        """
        db_type = conn_data.get('type', 'unknown')
        host = conn_data.get('host', 'unknown')
        
        # Simulate connection test
        if db_type == 'sqlite':
            return True, f"SQLite database accessible: {conn_data.get('database')}"
        elif host == 'localhost' or host.startswith('192.168'):
            return True, f"Connection successful to {db_type} at {host}"
        else:
            # Simulate random success for demo
            import random
            if random.random() > 0.3:
                return True, f"Connected to {db_type} at {host}"
            else:
                return False, f"Connection timeout: Could not reach {host}"


# ============================================================
# Demo Application
# ============================================================

def demo_manager_api():
    """
    Demonstrates using DBConnectionManager directly via API.
    """
    print("\n" + "="*60)
    print("DBConnectionManager API Demo")
    print("="*60)
    
    from winformpy.ui_elements.db_connection import DBConnectionManager
    
    # Create backend and manager
    backend = MockStorageBackend()
    manager = DBConnectionManager(backend)
    
    # List all connections
    print("\n📋 All Connections:")
    for name in manager.list_names():
        config = manager.read(name)
        print(f"  - {name}: {config.get('type')} @ {config.get('host', config.get('database', 'N/A'))}")
    
    # Create a new connection
    print("\n➕ Creating new connection 'Demo SQL Server'...")
    result = manager.save('Demo SQL Server', {
        'type': 'sqlserver',
        'host': 'sql.example.com',
        'port': '1433',
        'database': 'DemoDb',
        'user': 'demo_user',
        'password': 'secret',
        'schema': 'dbo'
    })
    print(f"  Result: {result}")
    
    # Test a connection
    print("\n🔌 Testing connection 'Dev PostgreSQL'...")
    success, message = manager.test_connection(name='Dev PostgreSQL')
    print(f"  {'✅' if success else '❌'} {message}")
    
    # Read a connection
    print("\n📖 Reading 'Production Oracle'...")
    config = manager.read('Production Oracle')
    for key, value in config.items():
        print(f"  {key}: {value}")
    
    # Delete a connection
    print("\n🗑️ Deleting 'Demo SQL Server'...")
    deleted = manager.delete('Demo SQL Server')
    print(f"  Deleted: {deleted}")
    
    print("\n" + "="*60 + "\n")


def demo_ui():
    """
    Demonstrates the visual UI components.
    """
    from winformpy.ui_elements.db_connection import (
        DBConnectionManager, 
        DBConnectionUI, 
        DBConnectionPanel
    )
    
    # Create backend and manager
    backend = MockStorageBackend()
    manager = DBConnectionManager(backend)
    
    # Create main demo form
    form = Form({
        'Text': 'Database Connection Manager - UI Demo',
        'Width': 800,
        'Height': 650,
        'StartPosition': 'CenterScreen'
    })
    
    # Title label
    lbl_title = Label(form, {
        'Text': '🗄️ Database Connection Manager Demo',
        'Left': 20,
        'Top': 10,
        'Width': 500,
        'Height': 30,
        'Font': ('Segoe UI', 14, 'bold'),
        'TextAlign': 'MiddleLeft'
    })
    
    btn_open_ui = Button(form, {
        'Text': '📋 Open Full UI (Form)',
        'Left': 550,
        'Top': 10,
        'Width': 180,
        'Height': 30
    })
    
    # Info label
    info_label = Label(form, {
        'Text': 'Below is DBConnectionPanel embedded directly in this Form. '
                'Click the button above to open the standalone DBConnectionUI.',
        'Left': 20,
        'Top': 50,
        'Width': 750,
        'Height': 25,
        'TextAlign': 'MiddleLeft'
    })
    
    # Create embedded panel directly in form
    embedded_panel = DBConnectionPanel(form, manager, {
        'Left': 10,
        'Top': 85,
        'Width': 770,
        'Height': 520
    })
    
    # Button to open standalone UI
    def open_standalone_ui(sender, e):
        ui = DBConnectionUI(manager)
        ui.show_dialog()
    
    btn_open_ui.Click = open_standalone_ui
    
    # Show form
    form.ShowDialog()


def main():
    """Main entry point."""
    print("="*60)
    print("WinFormPy - Database Connection Manager Demo")
    print("="*60)
    print("\nThis demo shows the db_connection ui_element components:")
    print("  1. DBConnectionManager - Service layer for CRUD operations")
    print("  2. DBConnectionUI - Standalone Form window")
    print("  3. DBConnectionPanel - Embeddable Panel component")
    print("\nThe storage backend is mocked for this demo.")
    print("In production, you would provide your own implementation.")
    
    # Run API demo first (console output)
    demo_manager_api()
    
    # Then show the visual UI
    print("Launching visual UI demo...")
    demo_ui()


if __name__ == "__main__":
    main()
