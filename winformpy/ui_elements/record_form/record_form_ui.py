"""
Record Form UI - Standalone dialog forms for record viewing and editing.

This module provides ready-to-use dialog forms for displaying
and editing individual records.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from winformpy.winformpy import Form, DockStyle, DialogResult
from typing import Any, List, Dict

# Handle imports for both module and direct execution
try:
    from ..data_grid.data_grid_backend import ColumnDefinition, DataType
    from .record_form_panel import RecordFormPanel
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'data_grid'))
    from data_grid_backend import ColumnDefinition, DataType
    from record_form_panel import RecordFormPanel


class RecordFormDialog(Form):
    """
    Dialog form for displaying/editing a single record's details.
    
    Uses RecordFormPanel internally with action buttons enabled.
    Automatically generates input fields based on column definitions.
    
    Example:
        columns = backend.get_columns()
        dialog = RecordFormDialog(columns, record, title="Edit Customer")
        if dialog.ShowDialog() == DialogResult.OK:
            updated = dialog.get_values()
            save_record(updated)
    """
    
    COLORS = {
        'background': '#F5F5F5',
        'panel_bg': '#FFFFFF',
    }
    
    def __init__(self, columns: List[ColumnDefinition],
                 record: Dict[str, Any] = None,
                 title: str = "Record Details",
                 readonly: bool = False,
                 width: int = 500,
                 height: int = None):
        """
        Initialize the RecordFormDialog.
        
        Args:
            columns: Column definitions for the record.
            record: Optional record data to display/edit.
            title: Window title.
            readonly: If True, fields are read-only.
            width: Form width.
            height: Form height (auto-calculated if None).
        """
        self._columns = columns
        self._record = record or {}
        self._readonly = readonly
        
        # Filter to visible columns for height calculation
        visible_columns = [c for c in columns if c.visible]
        
        # Calculate height based on fields
        if height is None:
            height = min(700, 150 + len(visible_columns) * 60)
        
        super().__init__({
            'Text': title,
            'Width': width,
            'Height': height,
            'StartPosition': 'CenterScreen',
            'BackColor': self.COLORS['background']
        })
        self.ApplyLayout()
        
        self._result = DialogResult.Cancel
        
        self._build_ui()
    
    def _build_ui(self):
        """Build the form UI using RecordFormPanel."""
        # Create panel with action buttons
        self._panel = RecordFormPanel(self, props={
            'Dock': DockStyle.Fill,
            'Columns': self._columns,
            'Record': self._record,
            'ReadOnly': self._readonly,
            'ShowActionButtons': True,
            'BackColor': self.COLORS['panel_bg']
        })
        
        # Handle events
        self._panel.SaveClick = lambda s, e: self._save(e)
        self._panel.CancelClick = lambda s, e: self._cancel()
    
    def _save(self, args=None):
        """Save and close with OK result."""
        self._result = DialogResult.OK
        self.Close()
    
    def _cancel(self):
        """Close with Cancel result."""
        self._result = DialogResult.Cancel
        self.Close()
    
    def get_values(self) -> Dict[str, Any]:
        """
        Get the current values from all input fields.
        
        Returns:
            Dictionary with field names and values.
        """
        return self._panel.get_values()
    
    def set_values(self, record: Dict[str, Any]):
        """
        Set values in all input fields.
        
        Args:
            record: Dictionary with field names and values.
        """
        self._panel.set_values(record)
    
    @property
    def panel(self) -> RecordFormPanel:
        """Get the RecordFormPanel instance."""
        return self._panel
    
    @property
    def ReadOnly(self) -> bool:
        """Get read-only state."""
        return self._readonly
    
    @ReadOnly.setter
    def ReadOnly(self, value: bool):
        """Set read-only state."""
        self._readonly = value
        self._panel.ReadOnly = value
    
    def ShowDialog(self) -> DialogResult:
        """Show the form as a dialog and return the result."""
        super().ShowDialog()
        return self._result


# Backwards compatibility alias
RecordDetailForm = RecordFormDialog


# =============================================================================
# Example Usage
# =============================================================================
if __name__ == "__main__":
    from data_grid_backend import ColumnDefinition, DataType
    
    # Sample dialog
    columns = [ColumnDefinition("name", "Name", DataType.STRING, width=200)]
    dialog = RecordFormDialog(columns=columns, record={"name": "Sample"})
    dialog.ShowDialog()
