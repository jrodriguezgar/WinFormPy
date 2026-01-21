"""
Record Form Panel - Embeddable panel for displaying/editing record details.

This module provides a reusable panel component that auto-generates
input fields based on column definitions. Supports a pluggable backend
architecture for CRUD operations.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from winformpy.winformpy import (
    Panel, Label, TextBox, Button, CheckBox,
    DockStyle, AnchorStyles, Font, FontStyle
)
from typing import Any, List, Dict, Optional, Callable

# Import DataType from data_grid for column type handling
try:
    # When imported as part of the package
    from ..data_grid.data_grid_backend import ColumnDefinition, DataType
except ImportError:
    # When run directly or imported in unusual contexts
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'data_grid'))
    from data_grid_backend import ColumnDefinition, DataType

# Import backend classes
try:
    from .record_form_backend import (
        RecordFormBackend, RecordFormMode, RecordResponse, 
        ValidationResult, InMemoryRecordBackend
    )
except ImportError:
    from record_form_backend import (
        RecordFormBackend, RecordFormMode, RecordResponse,
        ValidationResult, InMemoryRecordBackend
    )


class RecordFormPanel(Panel):
    """
    Embeddable panel for displaying and editing record details.
    
    Auto-generates input fields based on column definitions.
    Supports both read-only viewing and editing modes.
    Uses AutoScroll for handling content that exceeds the visible area.
    Supports pluggable backend for CRUD operations.
    
    Properties:
        ReadOnly: bool - If True, all fields are read-only.
        ShowActionButtons: bool - Show action buttons panel (default False).
        ShowInsertButton: bool - Show Insert/New button (default True when Backend is set).
        ShowUpdateButton: bool - Show Update/Save button (default True when Backend is set).
        ShowDeleteButton: bool - Show Delete button (default True when Backend is set).
        ShowCancelButton: bool - Show Cancel/Close button (default True when Backend is set or ShowActionButtons=True).
        Backend: RecordFormBackend - Backend for CRUD operations (optional).
        Mode: RecordFormMode - Current form mode (VIEW, EDIT, INSERT).
        Columns: List[ColumnDefinition] - Column definitions for fields.
        Record: Dict[str, Any] - Current record data.
        FieldSpacing: int - Vertical spacing between fields.
        LabelWidth: int - Width of field labels.
        ContentPadding: int - Internal padding.
    
    Sub-Properties:
        Supports sub-properties for customizing internal elements:
        - 'ContentPanel': {'BackColor': '#F5F5F5', 'Padding': 15, ...}
        - 'ActionPanel': {'Height': 60, 'BackColor': '#FAFAFA', ...}
        - 'Labels': {'Font': Font('Segoe UI', 11), 'ForeColor': '#333', ...}
        - 'Inputs': {'Font': Font('Segoe UI', 10), 'Height': 28, ...}
        - 'Buttons': {'Font': Font('Segoe UI', 10), 'Width': 90, 'Height': 32, ...}
    
    Events:
        SaveClick: Fired when Save button is clicked.
        InsertClick: Fired when Insert button is clicked.
        UpdateClick: Fired when Update button is clicked.
        DeleteClick: Fired when Delete button is clicked.
        CancelClick: Fired when Cancel button is clicked.
        ValueChanged: Fired when any field value changes.
        RecordInserted: Fired after successful insert via backend.
        RecordUpdated: Fired after successful update via backend.
        RecordDeleted: Fired after successful delete via backend.
        ValidationFailed: Fired when validation fails.
    
    Example (with backend and sub-properties):
        from record_form_backend import InMemoryRecordBackend
        
        backend = InMemoryRecordBackend(records=my_records)
        
        panel = RecordFormPanel(parent, props={
            'Dock': DockStyle.Fill,
            'Columns': columns,
            'Record': record,
            'Backend': backend,
            'ContentPanel': {'BackColor': '#FAFAFA'},
            'ActionPanel': {'Height': 70, 'BackColor': '#F0F0F0'},
            'Labels': {'Font': Font('Segoe UI', 11, FontStyle.Bold)},
            'Inputs': {'Height': 32},
            'Buttons': {'Width': 100, 'Height': 36}
        })
        
        panel.RecordUpdated = lambda s, e: print(f"Updated: {e['record']}")
    
    Example (without backend - manual handling):
        panel = RecordFormPanel(parent, props={
            'Dock': DockStyle.Fill,
            'Columns': columns,
            'Record': record,
            'ShowActionButtons': True
        })
        panel.SaveClick = lambda s, e: save_record(panel.get_values())
    """
    
    COLORS = {
        'background': '#FFFFFF',
        'text': '#1A1A1A',
        'text_secondary': '#666666',
        'primary': '#0078D4',
        'success': '#28A745',
        'danger': '#DC3545',
        'warning': '#FFC107',
        'border': '#E0E0E0',
        'input_bg': '#FFFFFF',
        'button_bg': '#F0F0F0',
    }
    
    def __init__(self, master_form, props: Dict = None, 
                 columns: List[ColumnDefinition] = None,
                 record: Dict[str, Any] = None):
        """
        Initialize the RecordFormPanel.
        
        Args:
            master_form: Parent form or container.
            props: Optional dictionary of properties.
            columns: Column definitions for the record fields.
            record: Optional initial record data.
        """
        # Extract custom properties before calling super
        props = props or {}
        
        self._columns: List[ColumnDefinition] = columns or props.pop('Columns', [])
        self._record: Dict[str, Any] = record or props.pop('Record', {})
        self._readonly: bool = props.pop('ReadOnly', False)
        self._show_action_buttons: bool = props.pop('ShowActionButtons', False)
        self._field_spacing: int = props.pop('FieldSpacing', 60)
        self._label_width: int = props.pop('LabelWidth', 150)
        self._content_padding: int = props.pop('ContentPadding', 20)
        
        # Backend for CRUD operations
        self._backend: Optional[RecordFormBackend] = props.pop('Backend', None)
        self._mode: RecordFormMode = props.pop('Mode', RecordFormMode.VIEW if self._readonly else RecordFormMode.EDIT)
        
        # Individual button visibility (default True when Backend is provided)
        has_backend = self._backend is not None
        self._show_insert_button: bool = props.pop('ShowInsertButton', has_backend)
        self._show_update_button: bool = props.pop('ShowUpdateButton', has_backend)
        self._show_delete_button: bool = props.pop('ShowDeleteButton', has_backend)
        self._show_cancel_button: bool = props.pop('ShowCancelButton', has_backend or self._show_action_buttons)
        
        # Extract sub-properties for internal elements
        self._content_panel_props = props.pop('ContentPanel', {})
        self._action_panel_props = props.pop('ActionPanel', {})
        self._labels_props = props.pop('Labels', {})
        self._inputs_props = props.pop('Inputs', {})
        self._buttons_props = props.pop('Buttons', {})
        
        # Set default background
        if 'BackColor' not in props:
            props['BackColor'] = self.COLORS['background']
        
        super().__init__(master_form, props)
        
        # Internal state
        self._inputs: Dict[str, tuple] = {}  # name -> (type, widget, column)
        self._field_labels: List[Label] = []
        self._content_panel: Panel = None
        self._action_panel: Panel = None
        
        # Button references
        self._insert_btn: Button = None
        self._update_btn: Button = None
        self._delete_btn: Button = None
        self._cancel_btn: Button = None
        self._save_btn: Button = None  # Legacy support
        self._close_btn: Button = None  # Legacy support
        
        # Events - Legacy
        self.SaveClick: Callable[[object, Dict], None] = lambda s, e: None
        self.CancelClick: Callable[[object, Dict], None] = lambda s, e: None
        self.ValueChanged: Callable[[object, Dict], None] = lambda s, e: None
        
        # Events - CRUD operations
        self.InsertClick: Callable[[object, Dict], None] = lambda s, e: None
        self.UpdateClick: Callable[[object, Dict], None] = lambda s, e: None
        self.DeleteClick: Callable[[object, Dict], None] = lambda s, e: None
        
        # Events - Backend results
        self.RecordInserted: Callable[[object, Dict], None] = lambda s, e: None
        self.RecordUpdated: Callable[[object, Dict], None] = lambda s, e: None
        self.RecordDeleted: Callable[[object, Dict], None] = lambda s, e: None
        self.ValidationFailed: Callable[[object, Dict], None] = lambda s, e: None
        
        # Connect backend callbacks if backend is provided
        if self._backend:
            self._connect_backend()
        
        # Build UI if columns provided
        if self._columns:
            self._build_ui()
    
    def _connect_backend(self):
        """Connect backend callbacks to panel events."""
        if not self._backend:
            return
        
        self._backend.on_insert_complete = self._on_backend_insert_complete
        self._backend.on_update_complete = self._on_backend_update_complete
        self._backend.on_delete_complete = self._on_backend_delete_complete
        self._backend.on_validation_error = self._on_backend_validation_error
    
    def _on_backend_insert_complete(self, response: RecordResponse):
        """Handle backend insert completion."""
        if response.success:
            self._record = response.record.copy()
            self._mode = RecordFormMode.EDIT
            self.set_values(response.record)
            self.RecordInserted(self, {'record': response.record, 'response': response})
        else:
            self.ValidationFailed(self, {'error': response.error_message, 'errors': response.validation_errors})
    
    def _on_backend_update_complete(self, response: RecordResponse):
        """Handle backend update completion."""
        if response.success:
            self._record = response.record.copy()
            self.RecordUpdated(self, {'record': response.record, 'response': response})
        else:
            self.ValidationFailed(self, {'error': response.error_message, 'errors': response.validation_errors})
    
    def _on_backend_delete_complete(self, response: RecordResponse):
        """Handle backend delete completion."""
        if response.success:
            self.RecordDeleted(self, {'record': response.record, 'response': response})
            self.clear()
        else:
            self.ValidationFailed(self, {'error': response.error_message})
    
    def _on_backend_validation_error(self, validation: ValidationResult):
        """Handle backend validation error."""
        self.ValidationFailed(self, {'errors': validation.errors})
    
    def _build_ui(self):
        """Build the panel UI with input fields."""
        # Clear existing
        self._clear_fields()
        
        # Action buttons panel (if enabled) - at bottom
        # Action buttons panel (if enabled) - at bottom
        has_any_buttons = (self._show_action_buttons or self._show_insert_button or 
                          self._show_update_button or self._show_delete_button or 
                          self._show_cancel_button)
        if has_any_buttons:
            self._build_action_buttons()
        
        # Content panel with AutoScroll for the fields
        content_props = {
            'Dock': DockStyle.Fill,
            'BackColor': self.COLORS['background'],
            'AutoScroll': True,
            'AutoScrollMargin': (10, 10)
        }
        # Apply sub-properties for ContentPanel
        content_props.update(self._content_panel_props)
        self._content_panel = Panel(self, content_props)
        
        # Get label and input styling from sub-properties
        label_font = self._labels_props.get('Font', Font('Segoe UI', 10))
        label_color = self._labels_props.get('ForeColor', self.COLORS['text'])
        input_height = self._inputs_props.get('Height', 28)
        input_font = self._inputs_props.get('Font', Font('Segoe UI', 10))
        
        # Filter to visible columns only
        visible_columns = [c for c in self._columns if c.visible]
        
        y = self._content_padding
        for col in visible_columns:
            # Label with sub-properties
            lbl_props = {
                'Text': col.header,
                'Left': self._content_padding,
                'Top': y,
                'Width': self._label_width,
                'Height': 20,
                'Font': label_font,
                'ForeColor': label_color
            }
            # Apply additional label sub-properties
            for key, val in self._labels_props.items():
                if key not in lbl_props:
                    lbl_props[key] = val
            lbl = Label(self._content_panel, lbl_props)
            self._field_labels.append(lbl)
            y += 22
            
            # Get value
            value = self._format_value(col, self._record.get(col.name))
            
            # Create appropriate input widget with sub-properties
            widget = self._create_input_widget(col, value, y, input_height, input_font)
            y += self._field_spacing
        
        # Update scroll region after layout
        self._tk_widget.after(100, self._update_content_scroll)
        
        # Bind to update content width on resize
        self._tk_widget.bind('<Configure>', self._on_resize)
    
    def _update_content_scroll(self):
        """Update the scroll region of the content panel."""
        if self._content_panel and hasattr(self._content_panel, 'UpdateScroll'):
            self._content_panel.UpdateScroll()
    
    def _build_action_buttons(self):
        """Build the action buttons panel with CRUD buttons."""
        # Determine if we need to show any buttons
        has_crud_buttons = self._show_insert_button or self._show_update_button or self._show_delete_button
        has_legacy_buttons = self._show_action_buttons and not has_crud_buttons
        
        if not (has_crud_buttons or has_legacy_buttons or self._show_cancel_button):
            return
        
        # Build ActionPanel with sub-properties
        action_props = {
            'Dock': DockStyle.Bottom,
            'Height': 60,
            'BackColor': self.COLORS['background']
        }
        action_props.update(self._action_panel_props)
        self._action_panel = Panel(self, action_props)
        
        # Button sub-properties
        btn_width = self._buttons_props.get('Width', 90)
        btn_height = self._buttons_props.get('Height', 32)
        btn_font = self._buttons_props.get('Font', Font('Segoe UI', 10))
        
        # Create buttons based on visibility settings
        if has_crud_buttons:
            # New CRUD button architecture - position from left initially
            btn_x = 20
            btn_y = (action_props.get('Height', 60) - btn_height) // 2
            btn_spacing = btn_width + 10
            
            if self._show_insert_button:
                self._insert_btn = Button(self._action_panel, {
                    'Text': 'New',
                    'Left': btn_x,
                    'Top': btn_y,
                    'Width': btn_width,
                    'Height': btn_height,
                    'Font': btn_font,
                    'BackColor': self.COLORS['success'],
                    'ForeColor': '#FFFFFF'
                })
                self._insert_btn.Click = self._on_insert_click
                btn_x += btn_spacing
            
            if self._show_update_button:
                self._update_btn = Button(self._action_panel, {
                    'Text': 'Save',
                    'Left': btn_x,
                    'Top': btn_y,
                    'Width': btn_width,
                    'Height': btn_height,
                    'Font': btn_font,
                    'BackColor': self.COLORS['primary'],
                    'ForeColor': '#FFFFFF'
                })
                self._update_btn.Click = self._on_update_click
                btn_x += btn_spacing
            
            if self._show_delete_button:
                self._delete_btn = Button(self._action_panel, {
                    'Text': 'Delete',
                    'Left': btn_x,
                    'Top': btn_y,
                    'Width': btn_width,
                    'Height': btn_height,
                    'Font': btn_font,
                    'BackColor': self.COLORS['danger'],
                    'ForeColor': '#FFFFFF'
                })
                self._delete_btn.Click = self._on_delete_click
                btn_x += btn_spacing
            
            if self._show_cancel_button:
                self._cancel_btn = Button(self._action_panel, {
                    'Text': 'Cancel',
                    'Left': btn_x,
                    'Top': btn_y,
                    'Width': btn_width,
                    'Height': btn_height,
                    'Font': btn_font,
                    'BackColor': self.COLORS['button_bg']
                })
                self._cancel_btn.Click = lambda s, e: self.CancelClick(self, {})
        
        elif has_legacy_buttons:
            # Legacy button mode (ShowActionButtons=True)
            btn_x = 20
            btn_y = (action_props.get('Height', 60) - btn_height) // 2
            btn_spacing = btn_width + 10
            
            if self._readonly:
                # Just close button
                self._close_btn = Button(self._action_panel, {
                    'Text': 'Close',
                    'Left': btn_x,
                    'Top': btn_y,
                    'Width': btn_width,
                    'Height': btn_height,
                    'Font': btn_font,
                    'Anchor': AnchorStyles.Right | AnchorStyles.Bottom
                })
                self._close_btn.Click = lambda s, e: self.CancelClick(self, {})
            else:
                # Save button
                self._save_btn = Button(self._action_panel, {
                    'Text': 'Save',
                    'Left': btn_x,
                    'Top': btn_y,
                    'Width': btn_width,
                    'Height': btn_height,
                    'Font': btn_font,
                    'BackColor': self.COLORS['primary'],
                    'ForeColor': '#FFFFFF'
                })
                self._save_btn.Click = lambda s, e: self.SaveClick(self, {'values': self.get_values()})
                btn_x += btn_spacing
                
                # Cancel button
                self._cancel_btn = Button(self._action_panel, {
                    'Text': 'Cancel',
                    'Left': btn_x,
                    'Top': btn_y,
                    'Width': btn_width,
                    'Height': btn_height,
                    'Font': btn_font
                })
                self._cancel_btn.Click = lambda s, e: self.CancelClick(self, {})
        
        elif self._show_cancel_button:
            # Only cancel button
            btn_y = (action_props.get('Height', 60) - btn_height) // 2
            self._cancel_btn = Button(self._action_panel, {
                'Text': 'Close',
                'Left': 20,
                'Top': btn_y,
                'Width': btn_width,
                'Height': btn_height,
                'Font': btn_font,
                'BackColor': self.COLORS['button_bg']
            })
            self._cancel_btn.Click = lambda s, e: self.CancelClick(self, {})
        
        # Position buttons after a short delay
        self._tk_widget.after(50, self._position_action_buttons)
    
    def _on_insert_click(self, sender, e):
        """Handle Insert button click."""
        values = self.get_values()
        
        # Fire event for manual handling
        self.InsertClick(self, {'values': values})
        
        # If backend is connected, perform insert
        if self._backend:
            self._backend.insert(values)
    
    def _on_update_click(self, sender, e):
        """Handle Update button click."""
        values = self.get_values()
        
        # Fire events for manual handling (including legacy SaveClick)
        self.UpdateClick(self, {'values': values})
        self.SaveClick(self, {'values': values})
        
        # If backend is connected, perform update
        if self._backend:
            self._backend.update(values)
    
    def _on_delete_click(self, sender, e):
        """Handle Delete button click."""
        # Use the original record (with ID) not the form values
        record_to_delete = self._record.copy()
        # Update with current form values to ensure we have all data
        record_to_delete.update(self.get_values())
        
        # Fire event for manual handling
        self.DeleteClick(self, {'record': record_to_delete})
        
        # If backend is connected, perform delete
        if self._backend:
            self._backend.delete(record_to_delete)
    
    def _position_action_buttons(self):
        """Position action buttons based on panel width."""
        try:
            width = self._tk_widget.winfo_width()
            if width < 10:
                width = 400  # Default
            
            # Calculate positions from right edge
            right_pos = width - 20
            btn_spacing = 100  # button width + margin
            
            # Position buttons from right to left
            buttons_to_position = []
            
            # Collect buttons in order (right to left: Cancel, Delete, Save/Update, Insert)
            if self._cancel_btn:
                buttons_to_position.append(self._cancel_btn)
            if self._close_btn:
                buttons_to_position.append(self._close_btn)
            if self._delete_btn:
                buttons_to_position.append(self._delete_btn)
            if self._update_btn:
                buttons_to_position.append(self._update_btn)
            if self._save_btn:
                buttons_to_position.append(self._save_btn)
            if self._insert_btn:
                buttons_to_position.append(self._insert_btn)
            
            for btn in buttons_to_position:
                btn.Left = right_pos - 90
                btn.Top = 15
                right_pos -= btn_spacing
                
        except Exception:
            pass
    
    def _create_input_widget(self, col: ColumnDefinition, value: str, y: int,
                              input_height: int = 28, input_font = None):
        """Create the appropriate input widget for a column type."""
        width = self._get_input_width()
        if input_font is None:
            input_font = Font('Segoe UI', 10)
        
        if col.data_type == DataType.BOOLEAN:
            # Use CheckBox for boolean
            checkbox_props = {
                'Text': '',
                'Left': self._content_padding,
                'Top': y,
                'Width': width,
                'Height': input_height,
                'Checked': value == "Yes" or value is True,
                'Enabled': not self._readonly,
                'BackColor': self.COLORS['background']
            }
            # Apply additional input sub-properties
            for key, val in self._inputs_props.items():
                if key not in checkbox_props and key not in ('Height', 'Font'):
                    checkbox_props[key] = val
            checkbox = CheckBox(self._content_panel, checkbox_props)
            checkbox.CheckedChanged = lambda s, e: self._on_value_changed(col.name)
            self._inputs[col.name] = ('checkbox', checkbox, col)
            return checkbox
        else:
            # Use TextBox for other types
            textbox_props = {
                'Text': value if value else '',
                'Left': self._content_padding,
                'Top': y,
                'Width': width,
                'Height': input_height,
                'Font': input_font,
                'ReadOnly': self._readonly
            }
            # Apply additional input sub-properties
            for key, val in self._inputs_props.items():
                if key not in textbox_props and key not in ('Height', 'Font'):
                    textbox_props[key] = val
            textbox = TextBox(self._content_panel, textbox_props)
            # Bind change event
            textbox.TextChanged = lambda s, e: self._on_value_changed(col.name)
            self._inputs[col.name] = ('textbox', textbox, col)
            return textbox
    
    def _get_input_width(self) -> int:
        """Calculate input widget width based on panel width."""
        try:
            width = self._tk_widget.winfo_width()
            if width < 10:
                width = 400
            # Subtract padding and scrollbar width
            return width - (self._content_padding * 2) - 40
        except Exception:
            return 360
    
    def _format_value(self, col: ColumnDefinition, value: Any) -> str:
        """Format a value for display in an input field."""
        if value is None:
            return ""
        
        if col.data_type == DataType.DATE and hasattr(value, 'strftime'):
            return value.strftime('%Y-%m-%d')
        elif col.data_type == DataType.DATETIME and hasattr(value, 'strftime'):
            return value.strftime('%Y-%m-%d %H:%M')
        elif col.data_type == DataType.BOOLEAN:
            return "Yes" if value else "No"
        elif col.data_type == DataType.CURRENCY:
            return f"{float(value):,.2f}" if value else "0.00"
        elif col.data_type == DataType.PERCENTAGE:
            return f"{float(value):.1f}" if value else "0.0"
        else:
            return str(value)
    
    def _on_value_changed(self, field_name: str):
        """Handle value change in a field."""
        self.ValueChanged(self, {
            'field': field_name,
            'values': self.get_values()
        })
    
    def _on_resize(self, event=None):
        """Handle panel resize - adjust input widths."""
        width = self._get_input_width()
        for name, (input_type, widget, col) in self._inputs.items():
            try:
                widget.Width = width
            except Exception:
                pass
        
        # Reposition action buttons
        if self._show_action_buttons:
            self._position_action_buttons()
        
        # Update scroll region
        self._update_content_scroll()
    
    def _clear_fields(self):
        """Clear all input fields and labels."""
        # Destroy input widgets
        for name, (input_type, widget, col) in self._inputs.items():
            try:
                if hasattr(widget, '_tk_widget'):
                    widget._tk_widget.destroy()
            except Exception:
                pass
        self._inputs.clear()
        
        # Destroy labels
        for lbl in self._field_labels:
            try:
                if hasattr(lbl, '_tk_widget'):
                    lbl._tk_widget.destroy()
            except Exception:
                pass
        self._field_labels.clear()
        
        # Destroy content panel
        if self._content_panel:
            try:
                self._content_panel._tk_widget.destroy()
            except Exception:
                pass
            self._content_panel = None
        
        # Destroy action panel
        if self._action_panel:
            try:
                self._action_panel._tk_widget.destroy()
            except Exception:
                pass
            self._action_panel = None
    
    def get_values(self) -> Dict[str, Any]:
        """
        Get the current values from all input fields.
        
        Returns:
            Dictionary with field names and their converted values.
        """
        result = {}
        for name, (input_type, widget, col) in self._inputs.items():
            try:
                if input_type == 'checkbox':
                    result[name] = widget.Checked
                else:
                    text = widget.Text
                    # Convert based on data type
                    if col.data_type == DataType.INTEGER:
                        result[name] = int(text) if text else 0
                    elif col.data_type in (DataType.FLOAT, DataType.CURRENCY, DataType.PERCENTAGE):
                        clean = text.replace(',', '').replace('$', '').replace('%', '')
                        result[name] = float(clean) if clean else 0.0
                    elif col.data_type == DataType.BOOLEAN:
                        result[name] = text.lower() in ('yes', 'true', '1')
                    else:
                        result[name] = text
            except ValueError:
                result[name] = widget.Text if hasattr(widget, 'Text') else ""
        
        return result
    
    def set_values(self, record: Dict[str, Any]):
        """
        Set values in all input fields from a record.
        
        Args:
            record: Dictionary with field names and values.
        """
        self._record = record
        for name, (input_type, widget, col) in self._inputs.items():
            value = self._format_value(col, record.get(name))
            try:
                if input_type == 'checkbox':
                    widget.Checked = value == "Yes" or record.get(name) is True
                else:
                    widget.Text = value if value else ''
            except Exception:
                pass
    
    def load_record(self, record: Dict[str, Any]):
        """
        Load a record into the form for viewing/editing.
        
        This is an alias for set_values(), provided for clarity when 
        integrating with DataGridPanel.DetailPanel.
        
        Args:
            record: Dictionary with field names and values.
        """
        self.set_values(record)
    
    def clear(self):
        """Clear all input field values."""
        for name, (input_type, widget, col) in self._inputs.items():
            try:
                if input_type == 'checkbox':
                    widget.Checked = False
                else:
                    widget.Text = ''
            except Exception:
                pass
        self._record = {}
    
    def new_record(self):
        """
        Prepare the form for inserting a new record.
        
        Clears all fields and sets mode to INSERT.
        If a backend is connected, uses its default values.
        """
        self._mode = RecordFormMode.INSERT
        self.ReadOnly = False
        
        # Get default values from backend if available
        if self._backend:
            defaults = self._backend.get_default_values()
            self.set_values(defaults)
        else:
            self.clear()
    
    def edit_record(self, record: Dict[str, Any] = None):
        """
        Prepare the form for editing an existing record.
        
        Args:
            record: Optional record to load. If None, keeps current record.
        """
        self._mode = RecordFormMode.EDIT
        self.ReadOnly = False
        
        if record is not None:
            self.set_values(record)
    
    def view_record(self, record: Dict[str, Any] = None):
        """
        Prepare the form for viewing a record (read-only).
        
        Args:
            record: Optional record to load. If None, keeps current record.
        """
        self._mode = RecordFormMode.VIEW
        self.ReadOnly = True
        
        if record is not None:
            self.set_values(record)

    def set_field_value(self, field_name: str, value: Any):
        """Set value for a specific field."""
        if field_name in self._inputs:
            input_type, widget, col = self._inputs[field_name]
            formatted = self._format_value(col, value)
            try:
                if input_type == 'checkbox':
                    widget.Checked = formatted == "Yes" or value is True
                else:
                    widget.Text = formatted if formatted else ''
            except Exception:
                pass
    
    def get_field_value(self, field_name: str) -> Any:
        """Get value for a specific field."""
        values = self.get_values()
        return values.get(field_name)
    
    # Properties
    @property
    def Columns(self) -> List[ColumnDefinition]:
        """Get column definitions."""
        return self._columns
    
    @Columns.setter
    def Columns(self, value: List[ColumnDefinition]):
        """Set column definitions and rebuild UI."""
        self._columns = value
        if self._columns:
            self._build_ui()
    
    @property
    def Record(self) -> Dict[str, Any]:
        """Get current record."""
        return self._record
    
    @Record.setter
    def Record(self, value: Dict[str, Any]):
        """Set record and update fields."""
        self.set_values(value or {})
    
    @property
    def ReadOnly(self) -> bool:
        """Get read-only state."""
        return self._readonly
    
    @ReadOnly.setter
    def ReadOnly(self, value: bool):
        """Set read-only state for all fields."""
        self._readonly = value
        for name, (input_type, widget, col) in self._inputs.items():
            try:
                if input_type == 'checkbox':
                    widget.Enabled = not value
                else:
                    widget.ReadOnly = value
            except Exception:
                pass
    
    @property
    def ShowActionButtons(self) -> bool:
        """Get whether action buttons are shown."""
        return self._show_action_buttons
    
    @property
    def ShowInsertButton(self) -> bool:
        """Get whether Insert button is shown."""
        return self._show_insert_button
    
    @ShowInsertButton.setter
    def ShowInsertButton(self, value: bool):
        """Set Insert button visibility."""
        self._show_insert_button = value
    
    @property
    def ShowUpdateButton(self) -> bool:
        """Get whether Update button is shown."""
        return self._show_update_button
    
    @ShowUpdateButton.setter
    def ShowUpdateButton(self, value: bool):
        """Set Update button visibility."""
        self._show_update_button = value
    
    @property
    def ShowDeleteButton(self) -> bool:
        """Get whether Delete button is shown."""
        return self._show_delete_button
    
    @ShowDeleteButton.setter
    def ShowDeleteButton(self, value: bool):
        """Set Delete button visibility."""
        self._show_delete_button = value
    
    @property
    def ShowCancelButton(self) -> bool:
        """Get whether Cancel button is shown."""
        return self._show_cancel_button
    
    @ShowCancelButton.setter
    def ShowCancelButton(self, value: bool):
        """Set Cancel button visibility."""
        self._show_cancel_button = value
    
    @property
    def Backend(self) -> Optional[RecordFormBackend]:
        """Get the backend for CRUD operations."""
        return self._backend
    
    @Backend.setter
    def Backend(self, value: Optional[RecordFormBackend]):
        """Set the backend for CRUD operations."""
        self._backend = value
        if self._backend:
            self._connect_backend()
    
    @property
    def Mode(self) -> RecordFormMode:
        """Get the current form mode."""
        return self._mode
    
    @Mode.setter
    def Mode(self, value: RecordFormMode):
        """Set the form mode."""
        self._mode = value
        # Update readonly state based on mode
        if value == RecordFormMode.VIEW:
            self.ReadOnly = True
        else:
            self.ReadOnly = False
    
    @property
    def FieldSpacing(self) -> int:
        """Get field spacing."""
        return self._field_spacing
    
    @FieldSpacing.setter
    def FieldSpacing(self, value: int):
        """Set field spacing (requires rebuild)."""
        self._field_spacing = value
    
    @property
    def LabelWidth(self) -> int:
        """Get label width."""
        return self._label_width
    
    @LabelWidth.setter
    def LabelWidth(self, value: int):
        """Set label width (requires rebuild)."""
        self._label_width = value

    # =========================================================================
    # Field Visibility Methods
    # =========================================================================
    
    def hide_field(self, field_names):
        """
        Hide one or more fields by name.
        
        Args:
            field_names: Field name (str) or list of field names to hide.
        """
        if isinstance(field_names, str):
            field_names = [field_names]
        
        changed = False
        for col in self._columns:
            if col.name in field_names and col.visible:
                col.visible = False
                changed = True
        
        if changed:
            self._rebuild_fields()
    
    def show_field(self, field_names):
        """
        Show one or more previously hidden fields.
        
        Args:
            field_names: Field name (str) or list of field names to show.
        """
        if isinstance(field_names, str):
            field_names = [field_names]
        
        changed = False
        for col in self._columns:
            if col.name in field_names and not col.visible:
                col.visible = True
                changed = True
        
        if changed:
            self._rebuild_fields()
    
    def set_field_visibility(self, field_names, visible: bool):
        """
        Set the visibility of one or more fields.
        
        Args:
            field_names: Field name (str) or list of field names.
            visible: True to show, False to hide.
        """
        if visible:
            self.show_field(field_names)
        else:
            self.hide_field(field_names)
    
    def get_field_visibility(self, field_name: str) -> bool:
        """
        Get the visibility state of a field.
        
        Args:
            field_name: The name of the field.
            
        Returns:
            True if visible, False if hidden, None if field not found.
        """
        for col in self._columns:
            if col.name == field_name:
                return col.visible
        return None
    
    def get_visible_fields(self) -> List[str]:
        """
        Get the names of all visible fields.
        
        Returns:
            List of visible field names.
        """
        return [col.name for col in self._columns if col.visible]
    
    def get_hidden_fields(self) -> List[str]:
        """
        Get the names of all hidden fields.
        
        Returns:
            List of hidden field names.
        """
        return [col.name for col in self._columns if not col.visible]
    
    def _rebuild_fields(self):
        """Rebuild the panel after field visibility changes."""
        # Save current values before rebuild
        current_values = self.get_values()
        self._record.update(current_values)
        # Rebuild UI but preserve action panel
        self._rebuild_content_only()
    
    def _rebuild_content_only(self):
        """Rebuild only the content area, preserving action buttons."""
        # Destroy input widgets
        for name, (input_type, widget, col) in self._inputs.items():
            try:
                if hasattr(widget, '_tk_widget'):
                    widget._tk_widget.destroy()
            except Exception:
                pass
        self._inputs.clear()
        
        # Destroy labels
        for lbl in self._field_labels:
            try:
                if hasattr(lbl, '_tk_widget'):
                    lbl._tk_widget.destroy()
            except Exception:
                pass
        self._field_labels.clear()
        
        # Destroy content panel only
        if self._content_panel:
            try:
                self._content_panel._tk_widget.destroy()
            except Exception:
                pass
            self._content_panel = None
        
        # Recreate content panel with AutoScroll for the fields
        content_props = {
            'Dock': DockStyle.Fill,
            'BackColor': self.COLORS['background'],
            'AutoScroll': True,
            'AutoScrollMargin': (10, 10)
        }
        content_props.update(self._content_panel_props)
        self._content_panel = Panel(self, content_props)
        
        # Get label and input styling from sub-properties
        label_font = self._labels_props.get('Font', Font('Segoe UI', 10))
        label_color = self._labels_props.get('ForeColor', self.COLORS['text'])
        input_height = self._inputs_props.get('Height', 28)
        input_font = self._inputs_props.get('Font', Font('Segoe UI', 10))
        
        # Filter to visible columns only
        visible_columns = [c for c in self._columns if c.visible]
        
        y = self._content_padding
        for col in visible_columns:
            # Label with sub-properties
            lbl_props = {
                'Text': col.header,
                'Left': self._content_padding,
                'Top': y,
                'Width': self._label_width,
                'Height': 20,
                'Font': label_font,
                'ForeColor': label_color
            }
            for key, val in self._labels_props.items():
                if key not in lbl_props:
                    lbl_props[key] = val
            lbl = Label(self._content_panel, lbl_props)
            self._field_labels.append(lbl)
            y += 22
            
            # Get value
            value = self._format_value(col, self._record.get(col.name))
            
            # Create appropriate input widget with sub-properties
            widget = self._create_input_widget(col, value, y, input_height, input_font)
            y += self._field_spacing
        
        # Update scroll region after layout
        self._tk_widget.after(100, self._update_content_scroll)


# Backwards compatibility alias
RecordDetailPanel = RecordFormPanel


# =============================================================================
# Example Usage
# =============================================================================
if __name__ == "__main__":
    from winformpy.winformpy import Form, Panel, Button, Label, DockStyle, AnchorStyles, Font
    from data_grid_backend import ColumnDefinition, DataType
    from record_form_backend import InMemoryRecordBackend, RecordFormMode
    
    print("=" * 60)
    print("RecordFormPanel Demo")
    print("=" * 60)
    print("\nSelect demo:")
    print("  1. Basic panel with action buttons (legacy mode)")
    print("  2. Embedded in master-detail layout")
    print("  3. Field visibility demo (hide/show fields)")
    print("  4. Read-only mode")
    print("  5. CRUD with backend (Insert/Update/Delete)")
    
    choice = input("\nEnter choice (1-5): ").strip()
    
    # Sample columns
    columns = [
        ColumnDefinition("id", "ID", DataType.INTEGER),
        ColumnDefinition("name", "Full Name", DataType.STRING),
        ColumnDefinition("email", "Email Address", DataType.STRING),
        ColumnDefinition("department", "Department", DataType.STRING),
        ColumnDefinition("salary", "Salary", DataType.CURRENCY),
        ColumnDefinition("hire_date", "Hire Date", DataType.DATE),
        ColumnDefinition("active", "Active", DataType.BOOLEAN),
        ColumnDefinition("notes", "Notes", DataType.STRING),
    ]
    
    # Sample record
    record = {
        "id": 1,
        "name": "John Doe",
        "email": "john.doe@example.com",
        "department": "Engineering",
        "salary": 75000.00,
        "hire_date": "2020-05-15",
        "active": True,
        "notes": "Senior developer"
    }
    
    if choice == "1":
        # Demo 1: Basic panel with action buttons (legacy)
        print("\n--- Basic Panel Demo (Legacy Mode) ---")
        
        form = Form({
            'Text': 'RecordFormPanel - Basic Demo',
            'Width': 500,
            'Height': 500,
            'StartPosition': 'CenterScreen'
        })
        form.ApplyLayout()
        
        panel = RecordFormPanel(form, props={
            'Dock': DockStyle.Fill,
            'Columns': columns,
            'Record': record,
            'ReadOnly': False,
            'ShowActionButtons': True
        })
        
        def on_save(sender, args):
            values = args.get('values', {})
            print("\nSaving values:")
            for k, v in values.items():
                print(f"  {k}: {v}")
            form.Close()
        
        def on_cancel(sender, args):
            print("\nCancelled")
            form.Close()
        
        panel.SaveClick = on_save
        panel.CancelClick = on_cancel
        panel.ValueChanged = lambda s, e: print(f"  Field changed: {e.get('field')}")
        
        form.ShowDialog()
    
    elif choice == "2":
        # Demo 2: Master-detail layout
        print("\n--- Master-Detail Layout Demo ---")
        
        employees = [
            {"id": 1, "name": "John Doe", "email": "john@example.com", "department": "Engineering", "salary": 75000, "hire_date": "2020-05-15", "active": True, "notes": "Senior dev"},
            {"id": 2, "name": "Jane Smith", "email": "jane@example.com", "department": "Marketing", "salary": 65000, "hire_date": "2019-08-20", "active": True, "notes": "Team lead"},
            {"id": 3, "name": "Bob Wilson", "email": "bob@example.com", "department": "Sales", "salary": 55000, "hire_date": "2021-03-10", "active": False, "notes": "On leave"},
        ]
        
        form = Form({
            'Text': 'RecordFormPanel - Master-Detail Demo',
            'Width': 800,
            'Height': 500,
            'StartPosition': 'CenterScreen'
        })
        form.ApplyLayout()
        
        # Left panel with buttons
        left_panel = Panel(form, {'Dock': DockStyle.Left, 'Width': 200, 'BackColor': '#F0F0F0'})
        
        title_lbl = Label(left_panel, {
            'Text': 'Employees',
            'Top': 10, 'Left': 10, 'Width': 180, 'Height': 25,
            'Font': Font('Segoe UI', 12, FontStyle.Bold)
        })
        
        # Right panel with detail form (create first to reference in buttons)
        detail_panel = RecordFormPanel(form, props={
            'Dock': DockStyle.Fill,
            'Columns': columns,
            'Record': employees[0],
            'ReadOnly': True,
            'ShowActionButtons': False
        })
        
        # Create buttons for each employee
        for i, emp in enumerate(employees):
            btn = Button(left_panel, {
                'Text': emp['name'],
                'Top': 45 + i * 40, 'Left': 10, 'Width': 180, 'Height': 35
            })
            btn.Click = lambda s, e, rec=emp: detail_panel.set_values(rec)
        
        form.ShowDialog()
    
    elif choice == "3":
        # Demo 3: Field visibility
        print("\n--- Field Visibility Demo ---")
        
        form = Form({
            'Text': 'RecordFormPanel - Visibility Demo',
            'Width': 600,
            'Height': 550,
            'StartPosition': 'CenterScreen'
        })
        form.ApplyLayout()
        
        # Toolbar
        toolbar = Panel(form, {'Dock': DockStyle.Top, 'Height': 45, 'BackColor': '#E0E0E0'})
        
        hide_btn = Button(toolbar, {'Text': 'Hide ID & Notes', 'Left': 10, 'Top': 8, 'Width': 120, 'Height': 30})
        show_btn = Button(toolbar, {'Text': 'Show All', 'Left': 140, 'Top': 8, 'Width': 100, 'Height': 30})
        toggle_btn = Button(toolbar, {'Text': 'Toggle Salary', 'Left': 250, 'Top': 8, 'Width': 110, 'Height': 30})
        info_btn = Button(toolbar, {'Text': 'Show Info', 'Left': 370, 'Top': 8, 'Width': 100, 'Height': 30})
        
        panel = RecordFormPanel(form, props={
            'Dock': DockStyle.Fill,
            'Columns': columns,
            'Record': record,
            'ReadOnly': False,
            'ShowActionButtons': True
        })
        
        def hide_fields(s, e):
            panel.hide_field(['id', 'notes'])  # Hide multiple fields at once
            print(f"Hidden fields: {panel.get_hidden_fields()}")
        
        def show_all(s, e):
            panel.show_field(panel.get_hidden_fields())
            print("All fields visible")
        
        def toggle_salary(s, e):
            visible = panel.get_field_visibility('salary')
            panel.set_field_visibility('salary', not visible)
            print(f"Salary visible: {not visible}")
        
        def show_info(s, e):
            print(f"\nVisible: {panel.get_visible_fields()}")
            print(f"Hidden: {panel.get_hidden_fields()}")
        
        hide_btn.Click = hide_fields
        show_btn.Click = show_all
        toggle_btn.Click = toggle_salary
        info_btn.Click = show_info
        
        panel.SaveClick = lambda s, e: form.Close()
        panel.CancelClick = lambda s, e: form.Close()
        
        form.ShowDialog()
    
    elif choice == "4":
        # Demo 4: Read-only mode
        print("\n--- Read-Only Mode Demo ---")
        
        form = Form({
            'Text': 'RecordFormPanel - Read-Only Demo',
            'Width': 500,
            'Height': 500,
            'StartPosition': 'CenterScreen'
        })
        form.ApplyLayout()
        
        panel = RecordFormPanel(form, props={
            'Dock': DockStyle.Fill,
            'Columns': columns,
            'Record': record,
            'ReadOnly': True,
            'ShowActionButtons': True
        })
        
        panel.CancelClick = lambda s, e: form.Close()
        
        form.ShowDialog()
    
    elif choice == "5":
        # Demo 5: CRUD with backend
        print("\n--- CRUD with Backend Demo ---")
        
        # Sample data
        employees = [
            {"id": 1, "name": "John Doe", "email": "john@example.com", "department": "Engineering", "salary": 75000, "hire_date": "2020-05-15", "active": True, "notes": "Senior dev"},
            {"id": 2, "name": "Jane Smith", "email": "jane@example.com", "department": "Marketing", "salary": 65000, "hire_date": "2019-08-20", "active": True, "notes": "Team lead"},
            {"id": 3, "name": "Bob Wilson", "email": "bob@example.com", "department": "Sales", "salary": 55000, "hire_date": "2021-03-10", "active": False, "notes": "On leave"},
        ]
        
        # Create backend with data
        backend = InMemoryRecordBackend(records=employees, primary_key='id')
        
        form = Form({
            'Text': 'RecordFormPanel - CRUD with Backend',
            'Width': 800,
            'Height': 550,
            'StartPosition': 'CenterScreen'
        })
        form.ApplyLayout()
        
        # Left panel with employee list
        left_panel = Panel(form, {'Dock': DockStyle.Left, 'Width': 220, 'BackColor': '#F5F5F5'})
        
        title_lbl = Label(left_panel, {
            'Text': 'Employees',
            'Top': 10, 'Left': 10, 'Width': 200, 'Height': 25,
            'Font': Font('Segoe UI', 12, FontStyle.Bold)
        })
        
        # Status label
        status_lbl = Label(left_panel, {
            'Text': '',
            'Top': 430, 'Left': 10, 'Width': 200, 'Height': 40,
            'Font': Font('Segoe UI', 9),
            'ForeColor': '#28A745'
        })
        
        # Right panel with form (CRUD enabled)
        detail_panel = RecordFormPanel(form, props={
            'Dock': DockStyle.Fill,
            'Columns': columns,
            'Record': employees[0],
            'Backend': backend,
            'ShowInsertButton': True,
            'ShowUpdateButton': True,
            'ShowDeleteButton': True,
            'ShowCancelButton': True
        })
        
        # Track employee buttons for proper cleanup
        employee_buttons = []
        
        # Create buttons for each employee
        def refresh_list():
            """Refresh the employee button list."""
            # Remove old employee buttons
            for btn in employee_buttons:
                try:
                    if hasattr(btn, '_tk_widget') and btn._tk_widget:
                        btn._tk_widget.destroy()
                except:
                    pass
            employee_buttons.clear()
            
            # Create new buttons for current records
            for i, emp in enumerate(backend.get_records()):
                btn = Button(left_panel, {
                    'Text': emp['name'],
                    'Top': 45 + i * 40, 'Left': 10, 'Width': 200, 'Height': 35
                })
                # Make a copy of the record to avoid reference issues
                emp_copy = emp.copy()
                btn.Click = lambda s, e, rec=emp_copy: detail_panel.edit_record(rec)
                employee_buttons.append(btn)
        
        refresh_list()
        
        # Event handlers
        def on_inserted(sender, args):
            status_lbl.Text = f"✓ Inserted: {args['record'].get('name', 'New')}"
            status_lbl.ForeColor = '#28A745'
            refresh_list()
        
        def on_updated(sender, args):
            status_lbl.Text = f"✓ Updated: {args['record'].get('name', '')}"
            status_lbl.ForeColor = '#0078D4'
            refresh_list()
        
        def on_deleted(sender, args):
            status_lbl.Text = f"✓ Deleted record"
            status_lbl.ForeColor = '#DC3545'
            refresh_list()
            # Load first record or clear the form
            records = backend.get_records()
            if records:
                detail_panel.edit_record(records[0])
            else:
                detail_panel.clear()
                detail_panel.new_record()
        
        def on_validation_error(sender, args):
            status_lbl.Text = f"✗ Error: {args.get('error', 'Validation failed')}"
            status_lbl.ForeColor = '#DC3545'
        
        detail_panel.RecordInserted = on_inserted
        detail_panel.RecordUpdated = on_updated
        detail_panel.RecordDeleted = on_deleted
        detail_panel.ValidationFailed = on_validation_error
        detail_panel.CancelClick = lambda s, e: form.Close()
        
        form.ShowDialog()
    
    else:
        print("Invalid choice")
