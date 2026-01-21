"""
DataGrid UI - Standalone dialogs and forms for data grid operations.

This module provides ready-to-use dialog forms for displaying and
interacting with tabular data.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from winformpy.winformpy import (
    Form, Panel, Label, TextBox, Button, ComboBox,
    DockStyle, AnchorStyles, Font, FontStyle, DialogResult
)
from typing import Any, List, Dict, Optional, Callable

# Handle imports for both module and direct execution
if __name__ == "__main__":
    from data_grid_backend import (
        DataGridBackend, ColumnDefinition, DataType, SortOrder
    )
    from data_grid_manager import DataGridManager
    from data_grid_panel import DataGridPanel
else:
    from .data_grid_backend import (
        DataGridBackend, ColumnDefinition, DataType, SortOrder
    )
    from .data_grid_manager import DataGridManager
    from .data_grid_panel import DataGridPanel


class DataGridForm(Form):
    """
    Standalone form containing a DataGridPanel.
    
    Use this when you need a complete data grid window with
    title bar, optional toolbar, and status bar.
    
    Example:
        backend = MyDatabaseBackend(connection)
        form = DataGridForm(backend, title="Customers")
        form.RowDoubleClick = lambda s, e: edit_customer(e['record'])
        form.ShowDialog()
    """
    
    def __init__(self, backend: DataGridBackend = None,
                 manager: DataGridManager = None,
                 title: str = "Data Grid",
                 width: int = 1024,
                 height: int = 700):
        """
        Initialize the DataGridForm.
        
        Args:
            backend: Optional DataGridBackend for data source.
            manager: Optional pre-configured DataGridManager.
            title: Window title.
            width: Form width in pixels.
            height: Form height in pixels.
        """
        super().__init__({
            'Text': title,
            'Width': width,
            'Height': height,
            'StartPosition': 'CenterScreen'
        })
        self.ApplyLayout()
        
        # Setup manager
        if manager:
            self._manager = manager
        else:
            self._manager = DataGridManager(backend)
        
        # External events (forwarded from grid)
        self.RowClick: Callable[[object, Dict], None] = lambda s, e: None
        self.RowDoubleClick: Callable[[object, Dict], None] = lambda s, e: None
        self.SelectionChanged: Callable[[object, Dict], None] = lambda s, e: None
        
        # Build UI
        self._build_ui()
    
    def _build_ui(self):
        """Build the form UI."""
        # Main grid
        self._grid = DataGridPanel(self, props={
            'Dock': DockStyle.Fill
        }, manager=self._manager)
        
        # Forward events
        self._grid.RowClick = lambda s, e: self.RowClick(s, e)
        self._grid.RowDoubleClick = lambda s, e: self.RowDoubleClick(s, e)
        self._grid.SelectionChanged = lambda s, e: self.SelectionChanged(s, e)
    
    @property
    def manager(self) -> DataGridManager:
        """Get the data grid manager."""
        return self._manager
    
    @property
    def grid(self) -> DataGridPanel:
        """Get the data grid panel."""
        return self._grid
    
    @property
    def selected_records(self) -> List[Dict[str, Any]]:
        """Get currently selected records."""
        return self._manager.selected_records
    
    def refresh(self):
        """Refresh the grid data."""
        self._manager.refresh()


class DataGridPickerForm(Form):
    """
    Form for selecting one or more records from a data grid.
    
    Returns the selected records when OK is clicked.
    Uses DataGridPanel with ShowActionButtons=True internally.
    
    Example:
        picker = DataGridPickerForm(backend, title="Select Customer")
        if picker.ShowDialog() == DialogResult.OK:
            selected = picker.selected_records
            process_selection(selected)
    """
    
    def __init__(self, backend: DataGridBackend = None,
                 manager: DataGridManager = None,
                 title: str = "Select Records",
                 multi_select: bool = False,
                 width: int = 900,
                 height: int = 600):
        """
        Initialize the picker form.
        
        Args:
            backend: Optional DataGridBackend for data source.
            manager: Optional pre-configured DataGridManager.
            title: Window title.
            multi_select: Allow multiple record selection.
            width: Form width.
            height: Form height.
        """
        super().__init__({
            'Text': title,
            'Width': width,
            'Height': height,
            'StartPosition': 'CenterScreen'
        })
        self.ApplyLayout()
        
        self._multi_select = multi_select
        self._result = DialogResult.Cancel
        self._selected: List[Dict[str, Any]] = []
        
        # Setup manager
        if manager:
            self._manager = manager
        else:
            self._manager = DataGridManager(backend)
        
        self._build_ui()
    
    def _build_ui(self):
        """Build the form UI."""
        # Grid panel with action buttons enabled
        self._grid = DataGridPanel(self, props={
            'Dock': DockStyle.Fill,
            'ShowActionButtons': True  # Enable OK/Cancel buttons
        }, manager=self._manager)
        
        # Handle action button events
        self._grid.OkClick = lambda s, e: self._ok(e)
        self._grid.CancelClick = lambda s, e: self._cancel()
        
        # Handle selection
        self._grid.SelectionChanged = self._on_selection_changed
        
        # Handle double-click as OK
        self._grid.RowDoubleClick = lambda s, e: self._ok({'selected_records': self._manager.selected_records})
    
    def _on_selection_changed(self, sender, args):
        """Handle selection change."""
        self._selected = args.get('selected_records', [])
    
    def _ok(self, args=None):
        """Accept selection and close."""
        if args:
            self._selected = args.get('selected_records', [])
        if not self._selected:
            self._selected = self._manager.selected_records
        if self._selected:
            self._result = DialogResult.OK
            self.Close()
    
    def _cancel(self):
        """Cancel and close."""
        self._result = DialogResult.Cancel
        self.Close()
    
    @property
    def selected_records(self) -> List[Dict[str, Any]]:
        """Get the selected records."""
        return self._selected
    
    @property
    def selected_record(self) -> Optional[Dict[str, Any]]:
        """Get the first selected record (for single selection)."""
        return self._selected[0] if self._selected else None
    
    @property
    def grid(self) -> DataGridPanel:
        """Get the data grid panel."""
        return self._grid
    
    def refresh(self):
        """Refresh the grid data."""
        self._manager.refresh()
    
    def ShowDialog(self) -> DialogResult:
        """Show as dialog and return result."""
        self._manager.refresh()
        super().ShowDialog()
        return self._result


# =============================================================================
# Example Usage - Product Management Demo
# =============================================================================
if __name__ == "__main__":
    import random
    from datetime import datetime, timedelta
    from data_grid_backend import (
        DataGridBackend, DataRequest, DataResponse, 
        ColumnDefinition, PageInfo, DataType, SortOrder
    )
    
    # Import RecordFormPanel for detail dialogs
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'record_form'))
    from record_form_panel import RecordFormPanel
    from record_form_backend import InMemoryRecordBackend
    
    # =========================================================================
    # Demo Backend - Simulates a product database with CRUD operations
    # =========================================================================
    class ProductBackend(DataGridBackend):
        """Backend for product data with full CRUD support."""
        
        def __init__(self, record_count: int = 50):
            """Generate demo data."""
            self._data = self._generate_data(record_count)
            self._next_id = record_count + 1
            self._columns = [
                ColumnDefinition("id", "ID", DataType.INTEGER, width=60, align="right"),
                ColumnDefinition("product", "Product Name", DataType.STRING, width=200),
                ColumnDefinition("category", "Category", DataType.STRING, width=120),
                ColumnDefinition("price", "Price", DataType.CURRENCY, width=100, align="right"),
                ColumnDefinition("stock", "In Stock", DataType.INTEGER, width=80, align="right"),
                ColumnDefinition("last_updated", "Last Updated", DataType.DATE, width=110, align="center"),
                ColumnDefinition("active", "Active", DataType.BOOLEAN, width=70, align="center"),
            ]
        
        def _generate_data(self, count: int) -> list:
            """Generate fake product records."""
            adjectives = ["Premium", "Classic", "Ultra", "Pro", "Basic", "Deluxe", "Standard", "Elite"]
            products = ["Widget", "Gadget", "Device", "Tool", "Component", "Module", "System", "Unit"]
            categories = ["Electronics", "Hardware", "Software", "Accessories", "Services", "Support"]
            
            records = []
            for i in range(1, count + 1):
                adj = random.choice(adjectives)
                prod = random.choice(products)
                cat = random.choice(categories)
                
                records.append({
                    "id": i,
                    "product": f"{adj} {prod} {i:03d}",
                    "category": cat,
                    "price": round(random.uniform(9.99, 999.99), 2),
                    "stock": random.randint(0, 500),
                    "last_updated": datetime.now() - timedelta(days=random.randint(0, 365)),
                    "active": random.random() > 0.1,
                })
            return records
        
        def get_columns(self) -> list:
            return self._columns
        
        def fetch_data(self, request: DataRequest) -> DataResponse:
            filtered = self._data.copy()
            
            if request.search_text:
                search = request.search_text
                search_lower = search.lower()
                
                def matches(value: str) -> bool:
                    val = str(value)
                    if request.exact_match:
                        if request.case_sensitive:
                            return val == search
                        else:
                            return val.lower() == search_lower
                    else:
                        if request.case_sensitive:
                            return search in val
                        else:
                            return search_lower in val.lower()
                
                filtered = [
                    r for r in filtered
                    if matches(r.get("product", "")) or
                       matches(r.get("category", ""))
                ]
            
            if request.sort_column and request.sort_order != SortOrder.NONE:
                reverse = request.sort_order == SortOrder.DESCENDING
                filtered.sort(
                    key=lambda x: (x.get(request.sort_column) is None, x.get(request.sort_column)),
                    reverse=reverse
                )
            
            total = len(filtered)
            total_pages = max(1, (total + request.page_size - 1) // request.page_size)
            current_page = min(request.page, total_pages)
            
            start = (current_page - 1) * request.page_size
            end = start + request.page_size
            page_data = filtered[start:end]
            
            return DataResponse(
                records=page_data,
                page_info=PageInfo(
                    current_page=current_page,
                    page_size=request.page_size,
                    total_records=total,
                    total_pages=total_pages
                ),
                columns=self._columns
            )
        
        def insert(self, record: dict) -> dict:
            """Insert a new product."""
            record['id'] = self._next_id
            self._next_id += 1
            record['last_updated'] = datetime.now()
            self._data.append(record)
            return record
        
        def update(self, record: dict) -> dict:
            """Update an existing product."""
            for i, r in enumerate(self._data):
                if r['id'] == record['id']:
                    record['last_updated'] = datetime.now()
                    self._data[i] = record
                    return record
            return None
        
        def delete(self, record_id: int) -> bool:
            """Delete a product by ID."""
            for i, r in enumerate(self._data):
                if r['id'] == record_id:
                    del self._data[i]
                    return True
            return False
        
        def get_record(self, record_id: int) -> dict:
            """Get a single record by ID."""
            for r in self._data:
                if r['id'] == record_id:
                    return r.copy()
            return None
    
    # =========================================================================
    # Product Management Demo
    # =========================================================================
    def demo():
        """Complete Product Management Demo with CRUD operations."""
        
        # Create backend with 50 products
        backend = ProductBackend(50)
        manager = DataGridManager(backend)
        
        # Create main form
        form = Form()
        form.Text = "Product Management - DataGrid Demo"
        form.Width = 1100
        form.Height = 700
        form.StartPosition = 'CenterScreen'
        form.ApplyLayout()
        
        # Toolbar with CRUD buttons
        toolbar = Panel(form, {
            'Dock': DockStyle.Top,
            'Height': 50,
            'BackColor': '#F5F5F5'
        })
        
        btn_new = Button(toolbar, {
            'Text': '➕ New',
            'Left': 10, 'Top': 10,
            'Width': 80, 'Height': 30,
            'Font': Font('Segoe UI', 10)
        })
        
        btn_edit = Button(toolbar, {
            'Text': '✏️ Edit',
            'Left': 100, 'Top': 10,
            'Width': 80, 'Height': 30,
            'Font': Font('Segoe UI', 10)
        })
        
        btn_delete = Button(toolbar, {
            'Text': '🗑️ Delete',
            'Left': 190, 'Top': 10,
            'Width': 90, 'Height': 30,
            'Font': Font('Segoe UI', 10)
        })
        
        btn_refresh = Button(toolbar, {
            'Text': '🔄 Refresh',
            'Left': 300, 'Top': 10,
            'Width': 90, 'Height': 30,
            'Font': Font('Segoe UI', 10)
        })
        
        # DataGrid panel
        grid = DataGridPanel(form, props={
            'Dock': DockStyle.Fill
        }, manager=manager)
        
        # Helper function to show record form dialog
        def show_record_dialog(record: dict = None, title: str = "Product", readonly: bool = False):
            """Show a dialog with RecordFormPanel for viewing/editing."""
            is_new = record is None
            if is_new:
                record = {
                    'id': 0,
                    'product': '',
                    'category': 'Electronics',
                    'price': 0.0,
                    'stock': 0,
                    'last_updated': datetime.now(),
                    'active': True
                }
                title = "New Product"
            
            # Create dialog
            dialog = Form()
            dialog.Text = title
            dialog.Width = 450
            dialog.Height = 480
            dialog.StartPosition = 'CenterScreen'
            dialog.ApplyLayout()
            
            # Result tracking
            dialog_result = {'saved': False, 'record': None}
            
            # Create RecordFormPanel
            form_backend = InMemoryRecordBackend(
                records=[record.copy()],
                primary_key='id'
            )
            
            form_columns = [
                ColumnDefinition('id', 'ID', DataType.INTEGER),
                ColumnDefinition('product', 'Product Name', DataType.STRING),
                ColumnDefinition('category', 'Category', DataType.STRING),
                ColumnDefinition('price', 'Price', DataType.CURRENCY),
                ColumnDefinition('stock', 'Stock', DataType.INTEGER),
                ColumnDefinition('last_updated', 'Last Updated', DataType.DATE),
                ColumnDefinition('active', 'Active', DataType.BOOLEAN),
            ]
            
            detail_form = RecordFormPanel(dialog, props={
                'Dock': DockStyle.Fill,
                'Backend': form_backend,
                'Columns': form_columns,
                'Record': record,
                'ReadOnly': readonly,
                'ShowInsertButton': False,
                'ShowUpdateButton': False,
                'ShowDeleteButton': False,
            })
            
            # Button panel at bottom
            btn_panel = Panel(dialog, {
                'Dock': DockStyle.Bottom,
                'Height': 50,
                'BackColor': '#F5F5F5'
            })
            
            if not readonly:
                btn_save = Button(btn_panel, {
                    'Text': 'Save',
                    'Left': 120, 'Top': 10,
                    'Width': 100, 'Height': 32,
                    'Font': Font('Segoe UI', 10, FontStyle.Bold)
                })
                
                def on_save(s, e):
                    dialog_result['saved'] = True
                    dialog_result['record'] = detail_form.get_values()
                    dialog.Close()
                
                btn_save.Click = on_save
            
            btn_cancel = Button(btn_panel, {
                'Text': 'Close' if readonly else 'Cancel',
                'Left': 230, 'Top': 10,
                'Width': 100, 'Height': 32,
                'Font': Font('Segoe UI', 10)
            })
            btn_cancel.Click = lambda s, e: dialog.Close()
            
            dialog.ShowDialog()
            
            return dialog_result
        
        # Event handlers
        def on_new(sender, e):
            result = show_record_dialog(None, "New Product")
            if result['saved'] and result['record']:
                new_record = backend.insert(result['record'])
                print(f"Created: {new_record['product']} (ID: {new_record['id']})")
                manager.refresh()
        
        def on_edit(sender, e):
            selected = manager.selected_records
            if not selected:
                print("Please select a product to edit")
                return
            record = selected[0]
            result = show_record_dialog(record.copy(), f"Edit: {record['product']}")
            if result['saved'] and result['record']:
                updated = result['record']
                updated['id'] = record['id']  # Preserve original ID
                backend.update(updated)
                print(f"Updated: {updated['product']}")
                manager.refresh()
        
        def on_delete(sender, e):
            selected = manager.selected_records
            if not selected:
                print("Please select a product to delete")
                return
            record = selected[0]
            # Simple confirmation via console (would use MessageBox in real app)
            print(f"Deleting: {record['product']} (ID: {record['id']})")
            backend.delete(record['id'])
            manager.refresh()
        
        def on_refresh(sender, e):
            manager.refresh()
            print("Grid refreshed")
        
        def on_double_click(sender, args):
            record = args.get('record', {})
            result = show_record_dialog(record.copy(), f"Edit: {record['product']}")
            if result['saved'] and result['record']:
                updated = result['record']
                updated['id'] = record['id']
                backend.update(updated)
                print(f"Updated: {updated['product']}")
                manager.refresh()
        
        # Wire up events
        btn_new.Click = on_new
        btn_edit.Click = on_edit
        btn_delete.Click = on_delete
        btn_refresh.Click = on_refresh
        grid.RowDoubleClick = on_double_click
        
        # Load initial data
        manager.refresh()
        
        # Print instructions
        print("=" * 65)
        print("Product Management Demo - DataGrid with CRUD Operations")
        print("=" * 65)
        print("\nToolbar Actions:")
        print("  ➕ New    - Create a new product")
        print("  ✏️ Edit   - Edit selected product")
        print("  🗑️ Delete - Delete selected product")
        print("  🔄 Refresh - Reload grid data")
        print("\nGrid Features:")
        print("  - Double-click a row to edit")
        print("  - Click column headers to sort")
        print("  - Use search box to filter")
        print("  - Pagination for large datasets")
        print("=" * 65)
        
        form.ShowDialog()
    
    # Run the demo
    demo()

