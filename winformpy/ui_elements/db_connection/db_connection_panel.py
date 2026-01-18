"""
Module: db_connection_panel.py

Description:
    Embeddable Panel UI for database connection management.
    Provides a reusable Panel component that can be integrated into other windows.
    Uses DBConnectionManager for all CRUD operations.

Note:
    DBConnectionUI and DBConnectionPanel are both visual interfaces at the same level:
    - DBConnectionUI: Standalone Form (window)
    - DBConnectionPanel: Embeddable Panel (for integration into other windows)
"""

import os
import sys
from typing import Dict, Optional, Any

# Add project root to path for direct execution
_current_dir = os.path.dirname(os.path.abspath(__file__))
_project_root = os.path.abspath(os.path.join(_current_dir, '..', '..', '..'))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from winformpy.winformpy import (
    Panel, Label, TextBox, Button, ComboBox, MessageBox
)


class DBConnectionPanel(Panel):
    """
    Embeddable Panel for database connection management.
    
    This is a visual interface at the same level as DBConnectionUI.
    Both use DBConnectionManager for CRUD operations.
    
    Attributes:
        connection_service: DBConnectionManager instance for CRUD operations.
        connections: Cache for loaded connections.
        on_test_connection: Optional callback for custom connection testing.
    
    Example:
        >>> from winformpy import Form
        >>> from winformpy.ui_elements.db_connection import (
        ...     DBConnectionManager, DBConnectionPanel
        ... )
        >>> 
        >>> app = Form({'Text': 'My App', 'Width': 900, 'Height': 700})
        >>> manager = DBConnectionManager(backend)
        >>> panel = DBConnectionPanel(app, manager, {'Left': 10, 'Top': 10})
        >>> app.ShowDialog()
    """
    
    def __init__(self, parent, connection_service, props: Optional[Dict[str, Any]] = None):
        """
        Initialize the connection panel.
        
        Args:
            parent: Parent form or panel to embed this component.
            connection_service: DBConnectionManager instance providing CRUD operations.
            props: Optional dictionary with Panel properties (Left, Top, Width, etc.).
        """
        default_props = {
            'AutoSize': True,
            'AutoSizeMode': 'GrowAndShrink',
            'Padding': (10, 10),
            'BorderStyle': 'groove',
            'Text': "Database Connection Management"
        }
        if props:
            default_props.update(props)
            
        super().__init__(parent, default_props)
        
        self.connection_service = connection_service
        self.connections = {} # Cache for loaded connections
        self._is_loading = False # Flag to prevent recursion in events
        
        # External callbacks (optional)
        self.on_test_connection = None
        
        # Control references
        self.cmb_connections = None
        self.txt_conn_name = None
        self.cmb_db_type = None
        
        self.txt_host = None
        self.txt_port = None
        self.txt_name = None
        self.txt_user = None
        self.txt_password = None
        self.txt_schema = None
        
        self._create_ui()
        self._load_connections_from_service()

    def _create_ui(self):
        # --- Dimensions, margins and vertical spacing ---
        LBL_WIDTH = 150
        FIELD_WIDTH = 400
        MARGIN_X = 20
        MARGIN_Y = 15
        ROW_HEIGHT = 28
        GAP_Y = 8
        STEP_Y = ROW_HEIGHT + GAP_Y
        
        current_y = MARGIN_Y
        field_x = MARGIN_X + LBL_WIDTH + 10
        
        # --- Connection Selector ---
        Label(self, {'Text': "Saved Connection:", 'Left': MARGIN_X, 'Top': current_y, 'Width': LBL_WIDTH, 'Height': ROW_HEIGHT})
        self.cmb_connections = ComboBox(self, {'Left': field_x, 'Top': current_y, 'Width': FIELD_WIDTH - 60, 'DropDownStyle': 'DropDownList'})
        self.cmb_connections.SelectedIndexChanged = self._on_connection_selected
        
        btn_refresh = Button(self, {'Text': "🔄", 'Left': field_x + (FIELD_WIDTH - 60) + 5, 'Top': current_y - 2, 'Width': 45, 'Height': 30})
        btn_refresh.Click = lambda s, e: self._load_connections_from_service()
        
        current_y += STEP_Y
        
        # --- Separator ---
        Panel(self, {
            'Left': MARGIN_X, 
            'Top': current_y + 2, 
            'Height': 2, 
            'BackColor': 'Silver', 
            'Width': LBL_WIDTH + FIELD_WIDTH + 10
        })
        current_y += 12

        # --- Row 1: Name and Type ---
        Label(self, {'Text': "Connection Name:", 'Left': MARGIN_X, 'Top': current_y, 'Width': LBL_WIDTH, 'Height': ROW_HEIGHT})
        self.txt_conn_name = TextBox(self, {'Left': field_x, 'Top': current_y, 'Width': FIELD_WIDTH - 150})
        
        Label(self, {'Text': "DB Type:", 'Left': field_x + (FIELD_WIDTH - 150) + 5, 'Top': current_y, 'Width': 60, 'Height': ROW_HEIGHT, 'TextAlign': 'MiddleLeft'})
        self.cmb_db_type = ComboBox(self, {
            'Left': field_x + (FIELD_WIDTH - 150) + 70, 
            'Top': current_y, 
            'Width': 80, 
            'DropDownStyle': 'DropDownList', 
            'Items': ['oracle', 'mysql', 'postgresql', 'sqlite', 'mssql']
        })
        
        current_y += STEP_Y
        
        # --- Row 2: Host and Port ---
        Label(self, {'Text': "Host:", 'Left': MARGIN_X, 'Top': current_y, 'Width': LBL_WIDTH, 'Height': ROW_HEIGHT})
        self.txt_host = TextBox(self, {'Text': "localhost", 'Left': field_x, 'Top': current_y, 'Width': FIELD_WIDTH - 150})
        
        Label(self, {'Text': "Port:", 'Left': field_x + (FIELD_WIDTH - 150) + 5, 'Top': current_y, 'Width': 60, 'Height': ROW_HEIGHT, 'TextAlign': 'MiddleLeft'})
        self.txt_port = TextBox(self, {'Text': "1521", 'Left': field_x + (FIELD_WIDTH - 150) + 70, 'Top': current_y, 'Width': 80})
        
        current_y += STEP_Y
        
        # --- Row 3: Database / SID ---
        Label(self, {'Text': "Database / SID:", 'Left': MARGIN_X, 'Top': current_y, 'Width': LBL_WIDTH, 'Height': ROW_HEIGHT})
        self.txt_name = TextBox(self, {'Text': "", 'Left': field_x, 'Top': current_y, 'Width': FIELD_WIDTH})
        
        current_y += STEP_Y
        
        # --- Row 4: User ---
        Label(self, {'Text': "User:", 'Left': MARGIN_X, 'Top': current_y, 'Width': LBL_WIDTH, 'Height': ROW_HEIGHT})
        self.txt_user = TextBox(self, {'Text': "", 'Left': field_x, 'Top': current_y, 'Width': FIELD_WIDTH})
        
        current_y += STEP_Y
        
        # --- Row 5: Password ---
        Label(self, {'Text': "Password:", 'Left': MARGIN_X, 'Top': current_y, 'Width': LBL_WIDTH, 'Height': ROW_HEIGHT})
        self.txt_password = TextBox(self, {'Text': "", 'Left': field_x, 'Top': current_y, 'Width': FIELD_WIDTH, 'PasswordChar': '*'})
        
        current_y += STEP_Y
        
        # --- Row 6: Schema (Optional) ---
        Label(self, {'Text': "Schema (optional):", 'Left': MARGIN_X, 'Top': current_y, 'Width': LBL_WIDTH, 'Height': ROW_HEIGHT})
        self.txt_schema = TextBox(self, {'Text': "", 'Left': field_x, 'Top': current_y, 'Width': FIELD_WIDTH})
        
        current_y += STEP_Y + 15
        
        # --- Action Buttons (Centered) ---
        btn_w = 110
        btn_gap = 8
        total_btns_w = (btn_w * 4) + (btn_gap * 3)
        btns_x = MARGIN_X + ( (LBL_WIDTH + FIELD_WIDTH + 10) - total_btns_w ) // 2
        
        self.btn_save = Button(self, {'Text': "💾 Save", 'Left': btns_x, 'Top': current_y, 'Width': btn_w, 'Height': 32})
        self.btn_save.Click = lambda s, e: self._save_connection()
        
        self.btn_delete = Button(self, {'Text': "🗑️ Delete", 'Left': btns_x + (btn_w + btn_gap), 'Top': current_y, 'Width': btn_w, 'Height': 32})
        self.btn_delete.Click = lambda s, e: self._delete_connection()
        
        btn_clear = Button(self, {'Text': "🧹 Clear", 'Left': btns_x + (btn_w + btn_gap) * 2, 'Top': current_y, 'Width': btn_w, 'Height': 32})
        btn_clear.Click = lambda s, e: self._clear_fields()
        
        btn_test = Button(self, {'Text': "🔌 Test", 'Left': btns_x + (btn_w + btn_gap) * 3, 'Top': current_y, 'Width': btn_w, 'Height': 32})
        btn_test.Click = lambda s, e: self._test_connection()
        
        # Adjusting final panel height
        self.Height = current_y + 50

    def _load_connections_from_service(self):
        """Loads connections from the service."""
        if self._is_loading: return
        self._is_loading = True
        
        try:
            names = self.connection_service.list_names()
                
            # Update ComboBox
            self.cmb_connections.Items.clear()
            self.cmb_connections.Items.append("-- New Connection --")
            for name in names:
                self.cmb_connections.Items.append(name)
            
            # Select the first one without triggering redundant events if already 0
            if self.cmb_connections.SelectedIndex != 0:
                self.cmb_connections.SelectedIndex = 0
            else:
                # If already 0, ensure fields are cleared (New Connection)
                self._clear_fields()
                
        except Exception as e:
            MessageBox.Show(f"Error loading settings: {e}", "Error")
        finally:
            self._is_loading = False

    def _on_connection_selected(self, sender, e):
        """Handles connection selection from ComboBox."""
        if self._is_loading: return
        
        selected = self.cmb_connections.Text
        if not selected or selected == "-- New Connection --":
            self._clear_fields()
            self._set_read_only(False)
            return
            
        config = self.connection_service.read(selected)
        if config:
            self.txt_conn_name.Text = selected
            self.set_config(config)
            
            # If it's a GLOBAL connection, disable editing
            is_readonly = selected.startswith("GLOBAL:") or config.get('is_global', False)
            self._set_read_only(is_readonly)

    def _set_read_only(self, readonly):
        """Enables or disables fields for editing."""
        self.txt_conn_name.Enabled = not readonly
        self.cmb_db_type.Enabled = not readonly
        self.txt_host.Enabled = not readonly
        self.txt_port.Enabled = not readonly
        self.txt_name.Enabled = not readonly
        self.txt_user.Enabled = not readonly
        self.txt_password.Enabled = not readonly
        self.txt_schema.Enabled = not readonly
        self.btn_save.Enabled = not readonly
        self.btn_delete.Enabled = not readonly

    def _save_connection(self):
        """Saves current connection."""
        name = self.txt_conn_name.Text.strip()
        if not name:
            MessageBox.Show("Specify a connection name.", "Error")
            return
            
        db_type = self.cmb_db_type.Text
        if not db_type:
            MessageBox.Show("Select a database type.", "Error")
            return

        config = self.get_config()
        
        try:
            self.connection_service.save(name, config)
            # Reload list
            self._load_connections_from_service()
            # Select newly saved
            self.cmb_connections.Text = name
            MessageBox.Show(f"Connection '{name}' saved successfully.", "Success")
        except Exception as e:
            MessageBox.Show(f"Error saving: {e}", "Error")

    def _delete_connection(self):
        """Deletes selected connection."""
        name = self.txt_conn_name.Text.strip()
        if not name:
            MessageBox.Show("Select an existing connection to delete.", "Error")
            return
            
        if name.startswith("GLOBAL:"):
            MessageBox.Show("Global connections cannot be deleted.", "Error")
            return

        if MessageBox.Show(f"Delete connection '{name}'?", "Confirm", "YesNo") == "Yes":
            try:
                success = self.connection_service.delete(name)
                if success:
                    self._load_connections_from_service()
                    self._clear_fields()
                else:
                    MessageBox.Show("Could not delete connection.", "Error")
            except Exception as e:
                MessageBox.Show(f"Error deleting: {e}", "Error")

    def _clear_fields(self):
        """Clears all fields."""
        was_loading = self._is_loading
        self._is_loading = True
        try:
            self.txt_conn_name.Text = ""
            self.cmb_db_type.SelectedIndex = -1
            self.txt_host.Text = ""
            self.txt_port.Text = ""
            self.txt_name.Text = ""
            self.txt_user.Text = ""
            self.txt_password.Text = ""
            self.txt_schema.Text = ""
            self.cmb_connections.SelectedIndex = 0
        finally:
            self._is_loading = was_loading

    def _test_connection(self):
        """Executes connection test via service."""
        name = self.txt_conn_name.Text.strip()
        config = self.get_config()
        
        try:
            # Use service test_connection if supported
            success, message = self.connection_service.test_connection(
                name if name else None, 
                config
            )
            
            if success:
                MessageBox.Show(message, "Success")
            else:
                MessageBox.Show(f"Test failed:\n{message}", "Error")
                
        except Exception as e:
            # Fallback to external callback if exists
            if self.on_test_connection:
                self.on_test_connection(config, self.cmb_db_type.Text)
            else:
                MessageBox.Show(f"Error testing connection: {e}", "Error")

    def get_config(self) -> Dict[str, Any]:
        """
        Get current connection configuration from UI fields.
        
        Returns:
            dict: Connection parameters with keys:
                - type: Database type (mysql, postgresql, etc.)
                - host: Server hostname
                - port: Server port
                - database: Database name
                - service_name: Oracle service name (same as database)
                - user: Username
                - password: Password
                - schema: Database schema
        """
        return {
            'type': self.cmb_db_type.Text,
            'host': self.txt_host.Text,
            'port': self.txt_port.Text,
            'database': self.txt_name.Text,
            'service_name': self.txt_name.Text,  # Oracle compatibility
            'user': self.txt_user.Text,
            'password': self.txt_password.Text,
            'schema': self.txt_schema.Text
        }

    def set_config(self, config: Dict[str, Any]) -> None:
        """
        Set UI fields from a connection configuration dictionary.
        
        Args:
            config: Connection parameters dictionary.
        """
        self._is_loading = True
        try:
            self.cmb_db_type.Text = config.get('type', config.get('db_type', ''))
            self.txt_host.Text = config.get('host', 'localhost')
            self.txt_port.Text = str(config.get('port', ''))
            
            # Map name/database fields
            dbname = config.get('database', config.get('service_name', ''))
            self.txt_name.Text = dbname
            
            self.txt_user.Text = config.get('user', '')
            self.txt_password.Text = config.get('password', config.get('pwd', ''))
            self.txt_schema.Text = config.get('schema', '')
        finally:
            self._is_loading = False


# ===== DEMO =====
if __name__ == "__main__":
    from winformpy.ui_elements.db_connection.db_connection_manager import DBConnectionManager
    from winformpy.winformpy import Form
    
    # --- Demo Storage Backend (simulates external backend) ---
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
                'demo-sqlite': {
                    'type': 'sqlite',
                    'host': '',
                    'port': '',
                    'database': 'C:/data/demo.db',
                    'user': '',
                    'password': '',
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
            """
            db_type = conn_data.get('type', '').lower()
            host = conn_data.get('host', '')
            
            # Demo: simulate connection test
            if db_type == 'sqlite':
                return True, f"SQLite: Database file configured (demo)."
            elif host == 'localhost' or host.startswith('192.168.'):
                return True, f"Connection to {db_type} at {host} successful (demo)."
            else:
                return False, f"Cannot reach {host} (demo simulation)."
    
    # --- Create demo window with panel ---
    print("=" * 50)
    print("DBConnectionPanel Demo")
    print("=" * 50)
    
    # Create main form
    app = Form({
        'Text': "DBConnectionPanel Demo",
        'Width': 700,
        'Height': 500,
        'StartPosition': 'CenterScreen'
    })
    
    # Create backend and manager
    backend = DemoStorageBackend()
    manager = DBConnectionManager(backend)
    
    # Create panel embedded in form
    panel = DBConnectionPanel(app, manager, {
        'Left': 10,
        'Top': 10,
        'Width': 660,
        'Height': 450
    })
    
    print("Demo panel created with sample connections:")
    for name in backend.list_names():
        print(f"  - {name}")
    print("\nShowing panel window...")
    
    app.ShowDialog()
