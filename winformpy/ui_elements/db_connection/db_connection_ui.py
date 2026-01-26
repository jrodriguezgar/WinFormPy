"""
Module: db_connection_ui.py
Description: Visual Form UI for database connection management with ListView.

Provides a standalone Form interface with:
- Left panel: ListView showing all saved connections
- Right panel: Form for editing connection details

The storage backend is external and not part of this project.
"""

import sys
import os

# Add project root to path for direct execution
_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.abspath(os.path.join(_current_dir, '..', '..', '..'))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from winformpy.winformpy import (
    Form, Panel, Label, TextBox, Button, ComboBox, MessageBox, 
    GroupBox, ListView, ColumnHeader
)
from winformpy.ui_elements.db_connection.db_connection_manager import DBConnectionManager


class DBConnectionUI(Form):
    """
    Full graphical interface for managing database connections.
    
    Features:
    - Left panel with ListView showing all connections
    - Right panel with detailed form
    - CRUD operations via DBConnectionManager
    - Connection testing support
    
    Architecture:
        ┌─────────────────────────────────────┐
        │  Visual Layer (same level)          │
        │  - DBConnectionUI (Form + ListView) │
        │  - DBConnectionPanel (Panel)        │
        └─────────────┬───────────────────────┘
                      │ uses
        ┌─────────────▼───────────────────────┐
        │  DBConnectionManager (Service)      │
        └─────────────┬───────────────────────┘
                      │ delegates to
        ┌─────────────▼───────────────────────┐
        │  Storage Backend (External)         │
        └─────────────────────────────────────┘
    
    Example:
        >>> backend = MyStorageBackend()
        >>> manager = DBConnectionManager(backend)
        >>> ui = DBConnectionUI(manager)
        >>> ui.show_dialog()
    """
    
    def __init__(self, connection_manager, props=None):
        """
        Initializes the connection management UI.
        
        Args:
            connection_manager: DBConnectionManager instance providing CRUD operations.
            props: Additional properties for the Form.
        """
        default_props = {
            'Text': "Database Connection Manager",
            'Width': 900,
            'Height': 650,
            'StartPosition': 'CenterScreen'
        }
        if props:
            default_props.update(props)
        
        super().__init__(default_props)
        
        # CRUD Layer
        self.manager = connection_manager
        
        # Control references
        self.lst_connections = None
        self.txt_name = None
        self.cmb_type = None
        self.txt_host = None
        self.txt_port = None
        self.txt_database = None
        self.txt_service_name = None
        self.txt_user = None
        self.txt_password = None
        self.txt_schema = None
        self.lbl_status = None
        
        # Current state
        self.current_selection = None
        
        self._create_ui()
        self._load_connections_list()
    
    def _create_ui(self):
        """Creates the full user interface."""
        # === LEFT PANEL: Connections list ===
        left_panel = self._create_connections_list_panel()
        left_panel.Left = 10
        left_panel.Top = 10
        left_panel.Width = 300
        left_panel.Height = 550
        
        # === RIGHT PANEL: Details and form ===
        right_panel = self._create_form_panel()
        right_panel.Left = 320
        right_panel.Top = 10
        right_panel.Width = 560
        right_panel.Height = 550
        
        # === BOTTOM PANEL: Status bar ===
        status_panel = Panel(self, {
            'Left': 10,
            'Top': 570,
            'Width': 870,
            'Height': 30,
            'BorderStyle': 'groove'
        })
        self.lbl_status = Label(status_panel, {
            'Text': "Ready",
            'Left': 5,
            'Top': 5,
            'Width': 860,
            'Height': 20
        })
    
    def _create_connections_list_panel(self) -> Panel:
        """Creates the connections list panel with ListView."""
        panel = Panel(self, {
            'BorderStyle': 'groove'
        })
        
        # Title
        title = Label(panel, {
            'Text': "📋 Saved Connections",
            'Left': 5,
            'Top': 5,
            'Width': 290,
            'Height': 30,
            'Font': ('Arial', 11, 'bold')
        })
        
        # ListView to show connections
        self.lst_connections = ListView(panel, {
            'Left': 5,
            'Top': 40,
            'Width': 290,
            'Height': 470,
            'View': 'Details',
            'FullRowSelect': True,
            'GridLines': True
        })
        
        # Columns
        col_name = ColumnHeader()
        col_name.Text = "Name"
        col_name.Width = 150
        
        col_type = ColumnHeader()
        col_type.Text = "Type"
        col_type.Width = 80
        
        col_host = ColumnHeader()
        col_host.Text = "Host"
        col_host.Width = 120
        
        self.lst_connections.Columns.Add(col_name)
        self.lst_connections.Columns.Add(col_type)
        self.lst_connections.Columns.Add(col_host)
        
        # Selection event
        self.lst_connections.SelectedIndexChanged = self._on_connection_selected
        
        # Refresh button
        btn_refresh = Button(panel, {
            'Text': "🔄 Refresh",
            'Left': 5,
            'Top': 515,
            'Width': 290,
            'Height': 35
        })
        btn_refresh.Click = lambda: self._load_connections_list()
        
        return panel
    
    def _create_form_panel(self) -> Panel:
        """Creates the detail form panel."""
        panel = Panel(self, {
            'BorderStyle': 'groove'
        })
        
        y = 10
        
        # Title
        title = Label(panel, {
            'Text': "✏️ Connection Details",
            'Left': 10,
            'Top': y,
            'Width': 540,
            'Height': 30,
            'Font': ('Arial', 11, 'bold')
        })
        y += 40
        
        # === FORM FIELDS ===
        
        # Name
        Label(panel, {'Text': "Connection Name:", 'Left': 10, 'Top': y, 'Width': 150, 'Height': 25})
        self.txt_name = TextBox(panel, {'Left': 170, 'Top': y, 'Width': 300, 'Height': 25})
        y += 35
        
        # Type
        Label(panel, {'Text': "DB Type:", 'Left': 10, 'Top': y, 'Width': 150, 'Height': 25})
        self.cmb_type = ComboBox(panel, {
            'Left': 170,
            'Top': y,
            'Width': 200,
            'Height': 25,
            'DropDownStyle': 'DropDownList',
            'Items': DBConnectionManager.SUPPORTED_DB_TYPES
        })
        self.cmb_type.SelectedIndexChanged = self._on_type_changed
        y += 35
        
        # Host
        Label(panel, {'Text': "Host:", 'Left': 10, 'Top': y, 'Width': 150, 'Height': 25})
        self.txt_host = TextBox(panel, {'Left': 170, 'Top': y, 'Width': 300, 'Height': 25})
        y += 35
        
        # Port
        Label(panel, {'Text': "Port:", 'Left': 10, 'Top': y, 'Width': 150, 'Height': 25})
        self.txt_port = TextBox(panel, {'Left': 170, 'Top': y, 'Width': 100, 'Height': 25})
        y += 35
        
        # Database
        Label(panel, {'Text': "Database:", 'Left': 10, 'Top': y, 'Width': 150, 'Height': 25})
        self.txt_database = TextBox(panel, {'Left': 170, 'Top': y, 'Width': 300, 'Height': 25})
        y += 35
        
        # Service Name
        Label(panel, {'Text': "Service Name:", 'Left': 10, 'Top': y, 'Width': 150, 'Height': 25})
        self.txt_service_name = TextBox(panel, {'Left': 170, 'Top': y, 'Width': 300, 'Height': 25})
        y += 35
        
        # User
        Label(panel, {'Text': "User:", 'Left': 10, 'Top': y, 'Width': 150, 'Height': 25})
        self.txt_user = TextBox(panel, {'Left': 170, 'Top': y, 'Width': 250, 'Height': 25})
        y += 35
        
        # Password
        Label(panel, {'Text': "Password:", 'Left': 10, 'Top': y, 'Width': 150, 'Height': 25})
        self.txt_password = TextBox(panel, {
            'Left': 170,
            'Top': y,
            'Width': 250,
            'Height': 25,
            'PasswordChar': '●'
        })
        y += 35
        
        # Schema
        Label(panel, {'Text': "Schema (optional):", 'Left': 10, 'Top': y, 'Width': 150, 'Height': 25})
        self.txt_schema = TextBox(panel, {'Left': 170, 'Top': y, 'Width': 250, 'Height': 25})
        y += 50
        
        # === ACTION BUTTONS ===
        btn_x = 10
        
        # New Button
        btn_new = Button(panel, {
            'Text': "📄 New",
            'Left': btn_x,
            'Top': y,
            'Width': 120,
            'Height': 35
        })
        btn_new.Click = lambda: self._new_connection()
        btn_x += 130
        
        # Save Button
        btn_save = Button(panel, {
            'Text': "💾 Save",
            'Left': btn_x,
            'Top': y,
            'Width': 120,
            'Height': 35
        })
        btn_save.Click = lambda: self._save_connection()
        btn_x += 130
        
        # Delete Button
        btn_delete = Button(panel, {
            'Text': "🗑️ Delete",
            'Left': btn_x,
            'Top': y,
            'Width': 120,
            'Height': 35
        })
        btn_delete.Click = lambda: self._delete_connection()
        btn_x += 130
        
        # Test Button
        btn_test = Button(panel, {
            'Text': "🔌 Test",
            'Left': btn_x,
            'Top': y,
            'Width': 120,
            'Height': 35
        })
        btn_test.Click = lambda: self._test_connection()
        
        return panel
    
    # === EVENT HANDLERS ===
    
    def _on_type_changed(self, sender, e):
        """Handles database type change."""
        db_type = self.cmb_type.Text
        
        # Show/hide fields according to type
        if db_type == 'oracle':
            self.txt_database.Visible = False
            self.txt_service_name.Visible = True
            self.txt_port.Text = "1521"
        else:
            self.txt_host.Visible = True
            self.txt_port.Visible = True
            self.txt_user.Visible = True
            self.txt_password.Visible = True
            self.txt_database.Visible = True
            self.txt_service_name.Visible = False
            
            if db_type == 'mysql':
                self.txt_port.Text = "3306"
            elif db_type == 'postgresql':
                self.txt_port.Text = "5432"
            elif db_type == 'mssql':
                self.txt_port.Text = "1433"
            elif db_type == 'sqlite':
                self.txt_port.Text = ""
    
    def _on_connection_selected(self, sender, e):
        """Handles connection selection in the list."""
        if self.lst_connections.SelectedItems.Count == 0:
            return
        
        selected_item = self.lst_connections.SelectedItems[0]
        conn_name = selected_item.Text
        
        self.current_selection = conn_name
        self._load_connection_to_form(conn_name)
        self._set_status(f"Connection '{conn_name}' loaded")
    
    # === CRUD OPERATIONS ===
    
    def _load_connections_list(self):
        """Loads the connections list into the ListView."""
        self.lst_connections.Items.Clear()
        
        connections = self.manager.read_all()
        
        for name, config in connections.items():
            item = self.lst_connections.Items.Add(name)
            item.SubItems.append(config.get('type', 'N/A'))
            item.SubItems.append(config.get('host', 'N/A'))
        
        self._set_status(f"{len(connections)} connections loaded")
    
    def _load_connection_to_form(self, name: str):
        """Loads a specific connection into the form."""
        config = self.manager.read(name)
        
        if not config:
            MessageBox.Show(f"Could not load connection '{name}'", "Error")
            return
        
        self.txt_name.Text = name
        self.cmb_type.Text = config.get('type', '')
        self.txt_host.Text = config.get('host', '')
        self.txt_port.Text = str(config.get('port', ''))
        self.txt_user.Text = config.get('user', '')
        self.txt_password.Text = config.get('password', '')
        self.txt_schema.Text = config.get('schema', '')
        
        # Handle database vs service_name
        if 'service_name' in config:
            self.txt_service_name.Text = config['service_name']
        if 'database' in config:
            self.txt_database.Text = config['database']
        
        # Trigger type changed to adjust fields
        self._on_type_changed(None, None)
    
    def _new_connection(self):
        """Clears the form to create a new connection."""
        self.txt_name.Text = ""
        self.cmb_type.SelectedIndex = -1
        self.txt_host.Text = "localhost"
        self.txt_port.Text = ""
        self.txt_database.Text = ""
        self.txt_service_name.Text = ""
        self.txt_user.Text = ""
        self.txt_password.Text = ""
        self.txt_schema.Text = ""
        
        self.current_selection = None
        self._set_status("New connection")
    
    def _save_connection(self):
        """Saves current connection."""
        name = self.txt_name.Text.strip()
        
        if not name:
            MessageBox.Show("Specify a connection name", "Error")
            return
        
        db_type = self.cmb_type.Text
        
        if not db_type:
            MessageBox.Show("Select a database type", "Error")
            return
        
        # Build connection data
        connection_data = {
            'type': db_type,
            'host': self.txt_host.Text,
            'port': self.txt_port.Text,
            'user': self.txt_user.Text,
            'password': self.txt_password.Text,
            'schema': self.txt_schema.Text
        }
        
        # Add database or service_name according to type
        if db_type == 'oracle':
            connection_data['service_name'] = self.txt_service_name.Text
        else:
            connection_data['database'] = self.txt_database.Text
        
        # Validate data
        is_valid, error_msg = self.manager.validate_connection_data(connection_data)
        
        if not is_valid:
            MessageBox.Show(f"Invalid data: {error_msg}", "Validation Error")
            return
        
        # Save using CRUD
        try:
            action = self.manager.save(name, connection_data)
            
            if action == 'created':
                MessageBox.Show(f"Connection '{name}' created successfully", "Success")
            else:
                MessageBox.Show(f"Connection '{name}' updated successfully", "Success")
            
            self._load_connections_list()
            self._set_status(f"Connection '{name}' saved")
            
        except Exception as e:
            MessageBox.Show(f"Error saving: {str(e)}", "Error")
    
    def _delete_connection(self):
        """Deletes selected connection."""
        name = self.txt_name.Text.strip()
        
        if not name:
            MessageBox.Show("Select a connection to delete", "Error")
            return
        
        # Confirm
        result = MessageBox.Show(
            f"Are you sure you want to delete connection '{name}'?",
            "Confirm Deletion",
            "YesNo"
        )
        
        if result != "Yes":
            return
        
        # Delete using CRUD
        if self.manager.delete(name):
            MessageBox.Show(f"Connection '{name}' deleted", "Success")
            self._new_connection()
            self._load_connections_list()
            self._set_status(f"Connection '{name}' deleted")
        else:
            MessageBox.Show(f"Could not delete connection '{name}'", "Error")
    
    def _test_connection(self):
        """Tests current connection."""
        # Get current config
        db_type = self.cmb_type.Text
        
        if not db_type:
            MessageBox.Show("Select a database type", "Error")
            return
        
        config = {
            'type': db_type,
            'host': self.txt_host.Text,
            'port': self.txt_port.Text,
            'user': self.txt_user.Text,
            'password': self.txt_password.Text,
            'schema': self.txt_schema.Text
        }
        
        if db_type == 'oracle':
            config['service_name'] = self.txt_service_name.Text
        else:
            config['database'] = self.txt_database.Text
        
        # Use manager test
        success, message = self.manager.test_connection(connection_data=config)
        
        if success:
            MessageBox.Show(message, "Success")
        else:
            MessageBox.Show(f"Test failed:\n{message}", "Error")

    def _set_status(self, message: str):
        """Updates the status bar."""
        if self.lbl_status:
            self.lbl_status.Text = message
    
    # ===== Public API (delegates to manager) =====
    
    def save(self, name: str, connection_data: dict) -> str:
        """Saves or updates a connection."""
        return self.manager.save(name, connection_data)
    
    def read(self, name: str) -> dict:
        """Reads a specific connection."""
        return self.manager.read(name)
    
    def read_all(self) -> dict:
        """Reads all connections."""
        return self.manager.read_all()
    
    def delete(self, name: str) -> bool:
        """Deletes a connection."""
        return self.manager.delete(name)
    
    def exists(self, name: str) -> bool:
        """Checks if a connection exists."""
        return self.manager.exists(name)
    
    def list_names(self) -> list:
        """Gets the list of all connection names."""
        return self.manager.list_names()
    
    def test_connection(self, name: str = None, connection_data: dict = None) -> tuple:
        """Tests the database connection."""
        return self.manager.test_connection(name, connection_data)
    
    def get_config(self) -> dict:
        """Gets current form configuration."""
        db_type = self.cmb_type.Text
        config = {
            'type': db_type,
            'host': self.txt_host.Text,
            'port': self.txt_port.Text,
            'user': self.txt_user.Text,
            'password': self.txt_password.Text,
            'schema': self.txt_schema.Text
        }
        if db_type == 'oracle':
            config['service_name'] = self.txt_service_name.Text
        else:
            config['database'] = self.txt_database.Text
        return config
    
    def show(self):
        """Shows the form as a non-modal window."""
        self.Show()
    
    def show_dialog(self):
        """Shows the form as a modal dialog."""
        return self.ShowDialog()


# ===== DEMO =====
if __name__ == "__main__":
    from db_connection_manager import DBConnectionManager
    
    class DemoStorageBackend:
        """
        Demo backend for testing purposes.
        In production, the backend is provided externally.
        
        Required methods (CRUD for connection parameters file):
        - save(name, data) -> str
        - read(name) -> dict | None
        - read_all() -> dict
        - delete(name) -> bool
        - list_names() -> list
        
        Optional method (for connectivity testing):
        - test_connection(conn_data) -> tuple[bool, str]
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
                    'host': '192.168.1.100',
                    'port': '5432',
                    'database': 'analytics',
                    'user': 'admin',
                    'password': 'secret',
                    'schema': 'public'
                }
            }
        
        # === Required CRUD methods ===
        
        def save(self, name: str, data: dict) -> str:
            action = 'updated' if name in self._data else 'created'
            self._data[name] = data
            return action
        
        def read(self, name: str) -> dict:
            return self._data.get(name)
        
        def read_all(self) -> dict:
            return dict(self._data)
        
        def delete(self, name: str) -> bool:
            if name in self._data:
                del self._data[name]
                return True
            return False
        
        def list_names(self) -> list:
            return list(self._data.keys())
        
        # === Optional: Connectivity testing ===
        
        def test_connection(self, conn_data: dict) -> tuple:
            """
            Tests database connectivity.
            This method is OPTIONAL. If not implemented, 
            the UI will show 'test not available'.
            
            Args:
                conn_data: Connection configuration dict
                
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
    
    manager = DBConnectionManager(DemoStorageBackend())
    ui = DBConnectionUI(manager)
    ui.show_dialog()
