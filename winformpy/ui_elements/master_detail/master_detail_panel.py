"""
Master-Detail Panel - Visual component for Master-Detail data display.

This module provides the MasterDetailPanel, an embeddable component that
combines a master view (DataGrid or ListView) with a detail DataGrid.

Configuration:
- MasterType: DataGrid or ListView (configured via props or backend)
- Orientation: 'horizontal' (side-by-side) or 'vertical' (top-bottom)
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from winformpy.winformpy import (
    Panel, Label, ListBox, Button, MessageBox,
    DockStyle, AnchorStyles, Font, FontStyle, ControlBase
)
from typing import Any, List, Dict, Optional, Callable


# Handle imports for both module and direct execution
try:
    # Module import - use relative imports
    from ..data_grid.data_grid_backend import (
        DataRequest, DataResponse, ColumnDefinition
    )
    from ..data_grid.data_grid_panel import DataGridPanel
    from ..data_grid.data_grid_manager import DataGridManager
    from .master_detail_backend import (
        MasterDetailBackend, MasterType, MasterItem, MasterListResponse
    )
    from .master_detail_manager import MasterDetailManager
except ImportError:
    # Direct execution - add paths and use direct imports
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'data_grid'))
    from data_grid_backend import DataRequest, DataResponse, ColumnDefinition
    from data_grid_panel import DataGridPanel
    from data_grid_manager import DataGridManager
    from master_detail_backend import (
        MasterDetailBackend, MasterType, MasterItem, MasterListResponse
    )
    from master_detail_manager import MasterDetailManager


# =============================================================================
# Internal Adapters
# =============================================================================

class _MasterGridBackend:
    """
    Internal adapter that wraps MasterDetailManager for the master DataGridPanel.
    
    Implements the DataGridBackend interface by delegating to the manager.
    """
    
    def __init__(self, md_manager: MasterDetailManager):
        self._manager = md_manager
    
    def get_columns(self) -> List[ColumnDefinition]:
        return self._manager.get_master_columns()
    
    def fetch_data(self, request: DataRequest) -> DataResponse:
        return self._manager.fetch_master_data(request)
    
    def format_value(self, value: Any, column: ColumnDefinition) -> str:
        return self._manager.format_master_value(value, column)


class _DetailGridBackend:
    """
    Internal adapter that wraps MasterDetailManager for the detail DataGridPanel.
    
    Implements the DataGridBackend interface by delegating to the manager.
    """
    
    def __init__(self, md_manager: MasterDetailManager):
        self._manager = md_manager
    
    def get_columns(self) -> List[ColumnDefinition]:
        return self._manager.get_detail_columns()
    
    def fetch_data(self, request: DataRequest) -> DataResponse:
        return self._manager.fetch_detail_data(request)
    
    def format_value(self, value: Any, column: ColumnDefinition) -> str:
        return self._manager.format_detail_value(value, column)


# =============================================================================
# MasterDetailPanel
# =============================================================================

class MasterDetailPanel(Panel):
    """
    A panel component that displays master-detail data relationships.
    
    Two containers layout:
    - Master container: Can be DataGrid or ListView (configurable via MasterType property)
    - Detail container: Always a DataGrid showing related records
    
    Layout options:
    - Orientation: 'horizontal' (master left, detail right) or 'vertical' (master top, detail bottom)
    
    Properties:
        MasterType: MasterType.DATA_GRID or MasterType.LIST_VIEW
        Orientation: 'horizontal' or 'vertical'
        MasterWidth: Width of master panel (when horizontal)
        MasterHeight: Height of master panel (when vertical)
    
    Features:
    - Automatic detail refresh on master selection
    - Resizable split layout
    - Sub-properties for customizing internal elements
    
    Example (horizontal layout with DataGrid master):
        panel = MasterDetailPanel(form, props={
            'Dock': DockStyle.Fill,
            'Orientation': 'horizontal',
            'MasterType': MasterType.DATA_GRID,
            'MasterWidth': 350,
        }, manager=manager)
        
        panel.MasterSelectionChanged = lambda s, e: print(f"Selected: {e['master_id']}")
        panel.DetailRowDoubleClick = lambda s, e: edit_order(e['record'])
    
    Example (vertical layout with ListView master):
        panel = MasterDetailPanel(form, props={
            'Dock': DockStyle.Fill,
            'Orientation': 'vertical',
            'MasterType': MasterType.LIST_VIEW,
            'MasterHeight': 200,
        }, manager=manager)
    """
    
    # Color scheme
    COLORS = {
        'background': '#FFFFFF',
        'panel_bg': '#FFFFFF',
        'header_bg': '#F3F3F3',
        'header_text': '#1A1A1A',
        'list_bg': '#FFFFFF',
        'list_selected': '#CCE4F7',
        'list_hover': '#E8F4FD',
        'border': '#E0E0E0',
        'text': '#1A1A1A',
        'text_secondary': '#666666',
        'splitter': '#D0D0D0',
    }
    
    def __init__(self, master_form, props: dict = None,
                 backend: MasterDetailBackend = None,
                 manager: MasterDetailManager = None):
        """
        Initialize the MasterDetailPanel.
        
        Args:
            master_form: Parent Form or Panel
            props: Optional properties dictionary. Supports:
                - 'MasterType': MasterType.DATA_GRID or MasterType.LIST_VIEW
                  (if not provided, uses backend's get_master_type())
                - 'Orientation': 'horizontal' (side-by-side) or 'vertical' (top-bottom)
                - 'MasterWidth': Width of master panel (horizontal mode, default 300)
                - 'MasterHeight': Height of master panel (vertical mode, default 250)
                - 'MasterPanel': Sub-properties for master panel container
                - 'MasterGrid': Sub-properties for master DataGridPanel
                - 'MasterList': Sub-properties for master ListView
                - 'DetailPanel': Sub-properties for detail panel container
                - 'DetailGrid': Sub-properties for detail DataGridPanel
            backend: Optional MasterDetailBackend for data source
            manager: Optional pre-configured MasterDetailManager
            
        Example (horizontal with DataGrid master):
            panel = MasterDetailPanel(form, props={
                'Dock': DockStyle.Fill,
                'Orientation': 'horizontal',
                'MasterType': MasterType.DATA_GRID,
                'MasterWidth': 350,
                'MasterGrid': {'Header': {'BackColor': '#E0E0E0'}},
                'DetailGrid': {'Rows': {'Height': 40}}
            }, manager=my_manager)
        
        Example (vertical with ListView master):
            panel = MasterDetailPanel(form, props={
                'Dock': DockStyle.Fill,
                'Orientation': 'vertical',
                'MasterType': MasterType.LIST_VIEW,
                'MasterHeight': 200,
            }, manager=my_manager)
        """
        # Extract configuration from props
        props = props or {}
        
        # Default: vertical layout. MasterType from backend or DATA_GRID if not specified
        self._orientation = props.pop('Orientation', 'vertical')
        self._master_width = props.pop('MasterWidth', 300)
        self._master_height = props.pop('MasterHeight', 250)
        self._master_type_override = props.pop('MasterType', None)  # None = use backend's type
        
        # Extract sub-properties
        self._master_panel_props = props.pop('MasterPanel', {})
        self._master_grid_props = props.pop('MasterGrid', {})
        self._master_list_props = props.pop('MasterList', {})
        self._detail_panel_props = props.pop('DetailPanel', {})
        self._detail_grid_props = props.pop('DetailGrid', {})
        
        defaults = {
            'Width': 1000,
            'Height': 600,
            'BackColor': self.COLORS['background'],
        }
        defaults.update(props)
        
        super().__init__(master_form, defaults)
        
        # Setup manager
        if manager:
            self._manager = manager
        elif backend:
            self._manager = MasterDetailManager(backend)
        else:
            raise ValueError("Either 'backend' or 'manager' must be provided")
        
        # Wire up manager events
        self._manager.on_master_selection_changed = self._on_master_selection_changed
        self._manager.on_master_data_changed = self._on_master_data_changed
        
        # External event handlers - Master
        self.MasterSelectionChanged: Callable[[object, Dict], None] = lambda s, e: None
        self.MasterRowClick: Callable[[object, Dict], None] = lambda s, e: None
        self.MasterRowDoubleClick: Callable[[object, Dict], None] = lambda s, e: None
        
        # External event handlers - Detail (DataGrid)
        self.DetailRowClick: Callable[[object, Dict], None] = lambda s, e: None
        self.DetailRowDoubleClick: Callable[[object, Dict], None] = lambda s, e: None
        self.DetailSelectionChanged: Callable[[object, Dict], None] = lambda s, e: None
        
        # Build UI
        self._master_panel = None
        self._detail_panel = None
        self._master_grid = None
        self._master_listbox = None
        self._detail_grid = None
        self._master_grid_manager = None
        self._detail_grid_manager = None
        
        # Store widgets with event handlers to prevent GC
        self._list_items = []
        
        self._build_ui()
    
    # =========================================================================
    # Properties
    # =========================================================================
    
    @property
    def manager(self) -> MasterDetailManager:
        """Get the MasterDetailManager instance."""
        return self._manager
    
    @property
    def master_grid(self) -> Optional[DataGridPanel]:
        """Get the master DataGridPanel (if using DataGrid master type)."""
        return self._master_grid
    
    @property
    def master_listbox(self) -> Optional[ListBox]:
        """Get the master ListBox (if using ListView master type)."""
        return self._master_listbox
    
    @property
    def detail_grid(self) -> DataGridPanel:
        """Get the detail DataGridPanel."""
        return self._detail_grid
    
    @property
    def master_type(self) -> MasterType:
        """Get the master view type (DATA_GRID or LIST_VIEW)."""
        if self._master_type_override is not None:
            return self._master_type_override
        return self._manager.get_master_type() or MasterType.DATA_GRID
    
    @property
    def selected_master_id(self) -> Any:
        """Get the currently selected master ID."""
        return self._manager.selected_master_id
    
    @property
    def selected_master_record(self) -> dict:
        """Get the currently selected master record."""
        return self._manager.selected_master_record
    
    @property
    def orientation(self) -> str:
        """Get the panel orientation ('horizontal' or 'vertical')."""
        return self._orientation
    
    # =========================================================================
    # UI Building
    # =========================================================================
    
    def _build_ui(self):
        """Build the master-detail UI."""
        # Use override MasterType if provided, otherwise get from backend, default to DATA_GRID
        if self._master_type_override is not None:
            master_type = self._master_type_override
        else:
            master_type = self._manager.get_master_type() or MasterType.DATA_GRID
        
        if self._orientation == 'horizontal':
            self._build_horizontal_layout(master_type)
        else:
            self._build_vertical_layout(master_type)
    
    def _build_horizontal_layout(self, master_type: MasterType):
        """Build side-by-side layout (master left, detail right)."""
        # Master panel (left)
        master_props = {
            'Dock': DockStyle.Left,
            'Width': self._master_width,
            'BackColor': self.COLORS['panel_bg'],
        }
        master_props.update(self._master_panel_props)
        self._master_panel = Panel(self, master_props)
        
        # Splitter visual indicator
        self._splitter = Panel(self, {
            'Dock': DockStyle.Left,
            'Width': 4,
            'BackColor': self.COLORS['splitter'],
        })
        
        # Detail panel (fill remaining)
        detail_props = {
            'Dock': DockStyle.Fill,
            'BackColor': self.COLORS['panel_bg'],
        }
        detail_props.update(self._detail_panel_props)
        self._detail_panel = Panel(self, detail_props)
        
        # Build content
        self._build_master_content(master_type)
        self._build_detail_content()
    
    def _build_vertical_layout(self, master_type: MasterType):
        """Build top-bottom layout (master top, detail bottom)."""
        # Master panel (top)
        master_props = {
            'Dock': DockStyle.Top,
            'Height': self._master_height,
            'BackColor': self.COLORS['panel_bg'],
        }
        master_props.update(self._master_panel_props)
        self._master_panel = Panel(self, master_props)
        
        # Splitter visual indicator
        self._splitter = Panel(self, {
            'Dock': DockStyle.Top,
            'Height': 4,
            'BackColor': self.COLORS['splitter'],
        })
        
        # Detail panel (fill remaining)
        detail_props = {
            'Dock': DockStyle.Fill,
            'BackColor': self.COLORS['panel_bg'],
        }
        detail_props.update(self._detail_panel_props)
        self._detail_panel = Panel(self, detail_props)
        
        # Build content
        self._build_master_content(master_type)
        self._build_detail_content()
    
    def _build_master_content(self, master_type: MasterType):
        """Build the master panel content."""
        # Title header
        title = self._manager.get_master_title()
        self._master_header = Label(self._master_panel, {
            'Dock': DockStyle.Top,
            'Height': 35,
            'Text': title,
            'Font': Font('Segoe UI', 11, FontStyle.Bold),
            'BackColor': self.COLORS['header_bg'],
            'Padding': (10, 8, 10, 8),
        })
        
        if master_type == MasterType.DATA_GRID:
            self._build_master_grid()
        else:
            self._build_master_listbox()
    
    def _build_master_grid(self):
        """Build the master as a DataGrid."""
        # Create adapter backend
        master_backend = _MasterGridBackend(self._manager)
        self._master_grid_manager = DataGridManager(master_backend)
        
        # Build grid props
        grid_props = {
            'Dock': DockStyle.Fill,
        }
        grid_props.update(self._master_grid_props)
        
        self._master_grid = DataGridPanel(
            self._master_panel,
            props=grid_props,
            manager=self._master_grid_manager
        )
        
        # Wire up events
        self._master_grid.RowClick = self._on_master_grid_row_click
        self._master_grid.RowDoubleClick = lambda s, e: self.MasterRowDoubleClick(s, e)
        
        # Initial load
        self._master_grid_manager.refresh()
    
    def _build_master_listbox(self):
        """Build the master as a ListView (using ListBox)."""
        list_props = {
            'Dock': DockStyle.Fill,
            'BackColor': self.COLORS['list_bg'],
        }
        list_props.update(self._master_list_props)
        
        self._master_listbox = ListBox(self._master_panel, list_props)
        
        # Bind selection event
        self._master_listbox._tk_widget.bind('<<ListboxSelect>>', self._on_listbox_select)
        
        # Load items
        self._load_master_list()
    
    def _load_master_list(self):
        """Load items into the master listbox."""
        response = self._manager.fetch_master_list()
        
        self._list_items = response.items
        self._master_listbox._tk_widget.delete(0, 'end')
        
        for item in response.items:
            display = f"{item.icon}  {item.text}" if item.icon else item.text
            self._master_listbox._tk_widget.insert('end', display)
    
    def _build_detail_content(self):
        """Build the detail panel content (always a DataGrid)."""
        # Title header
        title = self._manager.get_detail_title()
        self._detail_header = Label(self._detail_panel, {
            'Dock': DockStyle.Top,
            'Height': 35,
            'Text': title,
            'Font': Font('Segoe UI', 11, FontStyle.Bold),
            'BackColor': self.COLORS['header_bg'],
            'Padding': (10, 8, 10, 8),
        })
        
        # Build detail DataGrid
        self._build_detail_grid()
        
        # Empty state - no master selected
        self._update_detail_title(None)
    
    def _build_detail_grid(self):
        """Build the detail DataGrid."""
        # Create adapter backend
        detail_backend = _DetailGridBackend(self._manager)
        self._detail_grid_manager = DataGridManager(detail_backend)
        
        # Build grid props
        grid_props = {
            'Dock': DockStyle.Fill,
        }
        grid_props.update(self._detail_grid_props)
        
        self._detail_grid = DataGridPanel(
            self._detail_panel,
            props=grid_props,
            manager=self._detail_grid_manager
        )
        
        # Wire up events
        self._detail_grid.RowClick = lambda s, e: self.DetailRowClick(s, e)
        self._detail_grid.RowDoubleClick = lambda s, e: self.DetailRowDoubleClick(s, e)
        self._detail_grid.SelectionChanged = lambda s, e: self.DetailSelectionChanged(s, e)
    
    # =========================================================================
    # Event Handlers
    # =========================================================================
    
    def _on_master_grid_row_click(self, sender, event_args):
        """Handle click on a master grid row."""
        record = event_args.get('record')
        if record:
            id_field = self._manager.get_master_id_field()
            master_id = record.get(id_field)
            self._manager.set_selected_master_id(master_id, record)
        
        # Forward event
        self.MasterRowClick(sender, event_args)
    
    def _on_listbox_select(self, event):
        """Handle listbox selection change."""
        selection = self._master_listbox._tk_widget.curselection()
        if selection:
            index = selection[0]
            if index < len(self._list_items):
                item = self._list_items[index]
                self._manager.set_selected_master_id(item.id, {'item': item})
    
    def _on_master_selection_changed(self, master_id: Any):
        """Handle master selection change from manager."""
        # Update detail title
        self._update_detail_title(master_id)
        
        # Refresh detail DataGrid
        self._detail_grid_manager.go_to_page(1)  # Reset to first page
        self._detail_grid_manager.refresh()
        
        # Fire external event
        self.MasterSelectionChanged(self, {
            'master_id': master_id,
            'master_record': self._manager.selected_master_record
        })

    def _on_master_data_changed(self):
        """Handle master data change from manager - triggers refresh of master view."""
        self.refresh_master()
    
    def _update_detail_title(self, master_id: Any):
        """Update the detail header based on selection."""
        base_title = self._manager.get_detail_title()
        
        if master_id is None:
            self._detail_header.Text = f"{base_title} (select a master record)"
        else:
            # Try to get a display name from the master record
            record = self._manager.selected_master_record
            name = None
            
            if record:
                # Check if it's a MasterItem wrapper (from ListView)
                item = record.get('item') if isinstance(record, dict) else None
                if isinstance(item, MasterItem):
                    name = item.text
                elif isinstance(record, dict):
                    # Look for common name fields
                    name = (record.get('name') or record.get('Name') or
                            record.get('title') or record.get('Title') or
                            record.get('text'))
            
            if not name:
                name = str(master_id)
            
            self._detail_header.Text = f"{base_title} - {name}"
    
    # =========================================================================
    # Public Methods
    # =========================================================================
    
    def refresh_master(self):
        """Refresh the master view data."""
        if self._master_grid:
            self._master_grid_manager.refresh()
        else:
            self._load_master_list()
    
    def refresh_detail(self):
        """Refresh the detail DataGrid."""
        self._detail_grid_manager.refresh()
    
    def refresh(self):
        """Refresh both master and detail views."""
        self.refresh_master()
        if self._manager.selected_master_id is not None:
            self.refresh_detail()
    
    def select_master_by_id(self, master_id: Any):
        """
        Programmatically select a master record by ID.
        
        Args:
            master_id: The ID of the master record to select
        """
        if self._master_grid:
            # For grid, we need to find and select the row
            # This triggers the row click handler
            self._manager.set_selected_master_id(master_id, None)
        else:
            # For listbox, find the item and select it
            for i, item in enumerate(self._list_items):
                if item.id == master_id:
                    self._master_listbox._tk_widget.selection_clear(0, 'end')
                    self._master_listbox._tk_widget.selection_set(i)
                    self._master_listbox._tk_widget.see(i)
                    self._manager.set_selected_master_id(master_id, {'item': item})
                    break
    
    def clear_selection(self):
        """Clear both master and detail selections."""
        self._manager.clear_master_selection()
        if self._master_listbox:
            self._master_listbox._tk_widget.selection_clear(0, 'end')
        if self._detail_grid:
            self._detail_grid_manager.clear_selection()


# =============================================================================
# Demo - Customer Orders Example
# =============================================================================
if __name__ == "__main__":
    import random
    from datetime import datetime, timedelta
    
    # Import Form for the demo
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    from winformpy.winformpy import Form, Application
    from data_grid_backend import ColumnDefinition, DataType, DataRequest, DataResponse, PageInfo
    from master_detail_backend import MasterDetailBackend, MasterType, MasterItem, MasterListResponse
    from master_detail_manager import MasterDetailManager
    
    # =========================================================================
    # Demo Backend - Customers and Orders
    # =========================================================================
    class CustomerOrdersBackend(MasterDetailBackend):
        """Demo backend showing customers (master) and their orders (detail)."""
        
        def __init__(self):
            """Generate sample customer and order data."""
            self._customers = self._generate_customers(15)
            self._orders = self._generate_orders()
        
        def _generate_customers(self, count: int) -> list:
            """Generate sample customer data."""
            first_names = ["John", "Jane", "Robert", "Emily", "Michael", "Sarah", 
                          "David", "Lisa", "James", "Maria", "William", "Anna",
                          "Richard", "Jennifer", "Thomas"]
            last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia",
                         "Miller", "Davis", "Rodriguez", "Martinez", "Anderson", "Taylor"]
            cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
                     "Philadelphia", "San Antonio", "San Diego", "Dallas", "Austin"]
            
            customers = []
            for i in range(1, count + 1):
                first = random.choice(first_names)
                last = random.choice(last_names)
                customers.append({
                    'id': i,
                    'name': f"{first} {last}",
                    'email': f"{first.lower()}.{last.lower()}@email.com",
                    'city': random.choice(cities),
                    'total_orders': 0,  # Will be updated
                    'total_spent': 0.0,  # Will be updated
                })
            return customers
        
        def _generate_orders(self) -> list:
            """Generate sample orders for each customer."""
            products = ["Widget Pro", "Gadget X", "Tool Kit", "Component A", 
                       "Module B", "System C", "Device D", "Unit E"]
            statuses = ["Completed", "Processing", "Shipped", "Pending", "Delivered"]
            
            orders = []
            order_id = 1000
            
            for customer in self._customers:
                num_orders = random.randint(2, 8)
                customer_total = 0.0
                
                for _ in range(num_orders):
                    amount = round(random.uniform(25.0, 500.0), 2)
                    customer_total += amount
                    
                    orders.append({
                        'order_id': order_id,
                        'customer_id': customer['id'],
                        'product': random.choice(products),
                        'amount': amount,
                        'quantity': random.randint(1, 10),
                        'date': datetime.now() - timedelta(days=random.randint(1, 365)),
                        'status': random.choice(statuses),
                    })
                    order_id += 1
                
                customer['total_orders'] = num_orders
                customer['total_spent'] = round(customer_total, 2)
            
            return orders
        
        # Master configuration
        def get_master_type(self) -> MasterType:
            return MasterType.DATA_GRID
        
        def get_master_title(self) -> str:
            return "Customers"
        
        def get_master_id_field(self) -> str:
            return 'id'
        
        def get_master_columns(self) -> list:
            return [
                ColumnDefinition('id', 'ID', DataType.INTEGER, width=50, align='right'),
                ColumnDefinition('name', 'Customer Name', DataType.STRING, width=180),
                ColumnDefinition('city', 'City', DataType.STRING, width=120),
                ColumnDefinition('total_orders', 'Orders', DataType.INTEGER, width=70, align='right'),
                ColumnDefinition('total_spent', 'Total Spent', DataType.CURRENCY, width=100, align='right'),
            ]
        
        def fetch_master_data(self, request: DataRequest) -> DataResponse:
            filtered = self._customers.copy()
            
            # Search filter
            if request.search_text:
                search = request.search_text.lower()
                filtered = [c for c in filtered if 
                           search in c['name'].lower() or 
                           search in c['city'].lower() or
                           search in c['email'].lower()]
            
            # Sorting
            if request.sort_column:
                reverse = request.sort_order.value == 'descending'
                filtered.sort(
                    key=lambda x: (x.get(request.sort_column) is None, x.get(request.sort_column)),
                    reverse=reverse
                )
            
            total = len(filtered)
            total_pages = max(1, (total + request.page_size - 1) // request.page_size)
            current_page = min(request.page, total_pages)
            
            start = (current_page - 1) * request.page_size
            end = start + request.page_size
            
            return DataResponse(
                records=filtered[start:end],
                page_info=PageInfo(
                    current_page=current_page,
                    page_size=request.page_size,
                    total_records=total,
                    total_pages=total_pages
                ),
                columns=self.get_master_columns()
            )
        
        # Detail configuration
        def get_detail_title(self) -> str:
            return "Orders"
        
        def get_detail_columns(self) -> list:
            return [
                ColumnDefinition('order_id', 'Order #', DataType.INTEGER, width=80, align='right'),
                ColumnDefinition('product', 'Product', DataType.STRING, width=150),
                ColumnDefinition('quantity', 'Qty', DataType.INTEGER, width=50, align='right'),
                ColumnDefinition('amount', 'Amount', DataType.CURRENCY, width=100, align='right'),
                ColumnDefinition('date', 'Date', DataType.DATE, width=100, align='center'),
                ColumnDefinition('status', 'Status', DataType.STRING, width=100),
            ]
        
        def fetch_detail_data(self, master_id, request: DataRequest) -> DataResponse:
            # Filter orders by customer
            filtered = [o for o in self._orders if o['customer_id'] == master_id]
            
            # Search filter
            if request.search_text:
                search = request.search_text.lower()
                filtered = [o for o in filtered if 
                           search in o['product'].lower() or
                           search in o['status'].lower()]
            
            # Sorting
            if request.sort_column:
                reverse = request.sort_order.value == 'descending'
                filtered.sort(
                    key=lambda x: (x.get(request.sort_column) is None, x.get(request.sort_column)),
                    reverse=reverse
                )
            
            total = len(filtered)
            total_pages = max(1, (total + request.page_size - 1) // request.page_size)
            current_page = min(request.page, total_pages)
            
            start = (current_page - 1) * request.page_size
            end = start + request.page_size
            
            return DataResponse(
                records=filtered[start:end],
                page_info=PageInfo(
                    current_page=current_page,
                    page_size=request.page_size,
                    total_records=total,
                    total_pages=total_pages
                ),
                columns=self.get_detail_columns()
            )
    
    # =========================================================================
    # Demo with ListView Master
    # =========================================================================
    class CategoryProductsBackend(MasterDetailBackend):
        """Demo backend using ListView for master (categories) and Grid for detail (products)."""
        
        def __init__(self):
            self._categories = [
                {'id': 1, 'name': 'Electronics', 'icon': '💻'},
                {'id': 2, 'name': 'Clothing', 'icon': '👕'},
                {'id': 3, 'name': 'Books', 'icon': '📚'},
                {'id': 4, 'name': 'Home & Garden', 'icon': '🏠'},
                {'id': 5, 'name': 'Sports', 'icon': '⚽'},
            ]
            self._products = self._generate_products()
        
        def _generate_products(self) -> list:
            products_by_category = {
                1: [("Laptop Pro", 1299.99), ("Smartphone X", 899.99), ("Tablet Air", 649.99),
                    ("Wireless Earbuds", 199.99), ("Smart Watch", 349.99)],
                2: [("T-Shirt Basic", 19.99), ("Jeans Classic", 59.99), ("Jacket Winter", 129.99),
                    ("Sneakers Sport", 89.99), ("Hat Summer", 24.99)],
                3: [("Python Guide", 49.99), ("Data Science", 59.99), ("Web Development", 44.99),
                    ("Machine Learning", 69.99), ("Clean Code", 39.99)],
                4: [("Garden Tools Set", 79.99), ("Plant Pot Large", 29.99), ("LED Lights", 49.99),
                    ("Furniture Polish", 12.99), ("Outdoor Chair", 149.99)],
                5: [("Football Pro", 39.99), ("Tennis Racket", 89.99), ("Yoga Mat", 29.99),
                    ("Running Shoes", 119.99), ("Weights Set", 199.99)],
            }
            
            products = []
            prod_id = 1
            for cat_id, items in products_by_category.items():
                for name, price in items:
                    products.append({
                        'id': prod_id,
                        'category_id': cat_id,
                        'name': name,
                        'price': price,
                        'stock': random.randint(0, 100),
                        'rating': round(random.uniform(3.5, 5.0), 1),
                    })
                    prod_id += 1
            return products
        
        def get_master_type(self) -> MasterType:
            return MasterType.LIST_VIEW
        
        def get_master_title(self) -> str:
            return "Categories"
        
        def fetch_master_list(self) -> MasterListResponse:
            items = [
                MasterItem(
                    id=cat['id'],
                    text=f"{cat['icon']} {cat['name']}",
                    data=cat
                )
                for cat in self._categories
            ]
            return MasterListResponse(items=items)
        
        def get_detail_title(self) -> str:
            return "Products"
        
        def get_detail_columns(self) -> list:
            return [
                ColumnDefinition('id', 'ID', DataType.INTEGER, width=50, align='right'),
                ColumnDefinition('name', 'Product Name', DataType.STRING, width=180),
                ColumnDefinition('price', 'Price', DataType.CURRENCY, width=100, align='right'),
                ColumnDefinition('stock', 'In Stock', DataType.INTEGER, width=80, align='right'),
                ColumnDefinition('rating', 'Rating', DataType.FLOAT, width=70, align='center'),
            ]
        
        def fetch_detail_data(self, master_id, request: DataRequest) -> DataResponse:
            filtered = [p for p in self._products if p['category_id'] == master_id]
            
            if request.search_text:
                search = request.search_text.lower()
                filtered = [p for p in filtered if search in p['name'].lower()]
            
            if request.sort_column:
                reverse = request.sort_order.value == 'descending'
                filtered.sort(
                    key=lambda x: (x.get(request.sort_column) is None, x.get(request.sort_column)),
                    reverse=reverse
                )
            
            return DataResponse(
                records=filtered,
                page_info=PageInfo(
                    current_page=1,
                    page_size=len(filtered),
                    total_records=len(filtered),
                    total_pages=1
                ),
                columns=self.get_detail_columns()
            )
    
    # =========================================================================
    # Run Demo
    # =========================================================================
    def run_demo():
        """Run the Master-Detail Panel demo."""
        print("=" * 60)
        print("Master-Detail Panel Demo")
        print("=" * 60)
        print("\nTwo containers: Master (DataGrid/ListView) + Detail (DataGrid)")
        print("\nSelect demo:")
        print("  1. Customer Orders - DataGrid master, vertical layout")
        print("  2. Category Products - ListView master, horizontal layout")
        print("  3. Customer Orders - DataGrid master, horizontal layout")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == '1':
            # Customer Orders - DataGrid master, vertical layout
            backend = CustomerOrdersBackend()
            manager = MasterDetailManager(backend)
            
            form = Form()
            form.Text = "Customer Orders - Vertical Layout"
            form.Width = 1000
            form.Height = 800
            form.StartPosition = 'CenterScreen'
            form.ApplyLayout()
            
            panel = MasterDetailPanel(form, props={
                'Dock': DockStyle.Fill,
                'Orientation': 'vertical',
                'MasterHeight': 300,
            }, manager=manager)
            
            manager.refresh_master()
            Application.Run(form)
        
        elif choice == '2':
            # Category Products - ListView master
            backend = CategoryProductsBackend()
            manager = MasterDetailManager(backend)
            
            form = Form()
            form.Text = "Category Products - Master-Detail Demo"
            form.Width = 1000
            form.Height = 600
            form.StartPosition = 'CenterScreen'
            form.ApplyLayout()
            
            panel = MasterDetailPanel(form, props={
                'Dock': DockStyle.Fill,
                'Orientation': 'horizontal',
                'MasterWidth': 250,
            }, manager=manager)
            
            def on_category_changed(sender, args):
                item = args.get('master_record', {})
                if item:
                    form.Text = f"Products in: {item.get('text', 'Unknown')}"
            
            panel.MasterSelectionChanged = on_category_changed
            
            manager.refresh_master()
            Application.Run(form)
        
        elif choice == '3':
            # Customer Orders - DataGrid master, horizontal layout
            backend = CustomerOrdersBackend()
            manager = MasterDetailManager(backend)
            
            form = Form()
            form.Text = "Customer Orders - Master-Detail Demo"
            form.Width = 1200
            form.Height = 700
            form.StartPosition = 'CenterScreen'
            form.ApplyLayout()
            
            panel = MasterDetailPanel(form, props={
                'Dock': DockStyle.Fill,
                'Orientation': 'horizontal',
                'MasterWidth': 450,
            }, manager=manager)
            
            # Event handlers
            def on_master_changed(sender, args):
                customer = args.get('master_record', {})
                if customer:
                    form.Text = f"Orders for: {customer.get('name', 'Unknown')}"
            
            def on_detail_double_click(sender, args):
                order = args.get('record', {})
                if order:
                    MessageBox.Show(
                        f"Order #{order.get('order_id')}\n"
                        f"Product: {order.get('product')}\n"
                        f"Amount: ${order.get('amount', 0):,.2f}\n"
                        f"Status: {order.get('status')}",
                        "Order Details"
                    )
            
            panel.MasterSelectionChanged = on_master_changed
            panel.DetailRowDoubleClick = on_detail_double_click
            
            manager.refresh_master()
            Application.Run(form)
        
        else:
            print("Invalid choice")
    
    run_demo()
