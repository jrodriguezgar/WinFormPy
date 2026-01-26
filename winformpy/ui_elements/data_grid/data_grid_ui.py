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
    from data_grid_backend import DataGridBackend, DataRequest, DataResponse, ColumnDefinition
    
    class SimpleBackend(DataGridBackend):
        """Simple demo backend."""
        def get_data(self, request):
            return DataResponse(data=[], total_records=0)
        def get_columns(self):
            return [ColumnDefinition("id", "ID")]
    
    form = DataGridForm(backend=SimpleBackend())
    form.ShowDialog()
    


