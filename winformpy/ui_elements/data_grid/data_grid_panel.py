"""
DataGrid Panel - Visual component for displaying tabular data.

This module provides the DataGridPanel, an embeddable data grid component
with pagination, search, sorting, and selection capabilities.
"""

import sys
import os
from enum import Enum
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from winformpy.winformpy import (
    Panel, Label, TextBox, Button, CheckBox,
    DockStyle, AnchorStyles, Font, FontStyle, ControlBase
)
from typing import Any, List, Dict, Optional, Callable


class SelectionMode(Enum):
    """Defines how rows can be selected in the DataGridPanel."""
    NONE = 'none'           # No selection allowed
    SINGLE = 'single'       # Only one row can be selected at a time
    MULTIPLE = 'multiple'   # Multiple rows can be selected (Ctrl+Click, Shift+Click)

# Handle imports for both module and direct execution
try:
    from .data_grid_backend import (
        DataGridBackend, ColumnDefinition, DataType, SortOrder
    )
    from .data_grid_manager import DataGridManager
except ImportError:
    from data_grid_backend import (
        DataGridBackend, ColumnDefinition, DataType, SortOrder
    )
    from data_grid_manager import DataGridManager


class DataGridPanel(Panel):
    """
    A panel component for displaying tabular data with pagination and search.
    
    Features:
    - Sortable columns
    - Search/filter functionality
    - Pagination with configurable page size
    - Row selection (single and multi-select)
    - Customizable column formatting
    - External backend architecture
    - Optional integration with RecordFormPanel for detail view/editing
    
    Example:
        backend = MySQLBackend(connection, "customers")
        manager = DataGridManager(backend)
        
        grid = DataGridPanel(form, props={'Dock': DockStyle.Fill}, manager=manager)
        grid.RowDoubleClick = lambda sender, args: edit_record(args['record'])
        
        manager.refresh()
    
    Integration with RecordFormPanel:
        from winformpy.ui_elements.record_form import RecordFormPanel
        
        # Create grid and detail panel
        grid = DataGridPanel(left_panel, props={'Dock': DockStyle.Fill}, manager=manager)
        detail = RecordFormPanel(right_panel, props={
            'Dock': DockStyle.Fill,
            'Columns': backend.get_columns(),
            'ReadOnly': True
        })
        
        # Link detail panel to grid (updates on selection change)
        grid.DetailPanel = detail
        
        # Or use RowDoubleClick for edit dialog
        grid.RowDoubleClick = lambda s, e: show_edit_dialog(e['record'])
    """
    
    # Color scheme
    COLORS = {
        'background': '#FFFFFF',
        'header_bg': '#F3F3F3',
        'header_text': '#1A1A1A',
        'row_bg': '#FFFFFF',
        'row_alt_bg': '#FAFAFA',
        'row_hover': '#E8F4FD',
        'row_selected': '#CCE4F7',
        'border': '#E0E0E0',
        'text': '#1A1A1A',
        'text_secondary': '#666666',
        'primary': '#0078D4',
        'pagination_bg': '#F8F8F8',
    }
    
    def __init__(self, master_form, props: dict = None,
                 backend: DataGridBackend = None,
                 manager: DataGridManager = None):
        """
        Initialize the DataGridPanel.
        
        Args:
            master_form: Parent Form or Panel
            props: Optional properties dictionary. Supports sub-properties for internal elements:
                - 'Toolbar': {'Height': 50, 'BackColor': '#FFF', ...}
                - 'Header': {'Height': 40, 'BackColor': '#F3F3F3', 'ForeColor': '#1A1A1A', ...}
                - 'Rows': {'Height': 36, 'BackColor': '#FFF', 'AlternateBackColor': '#FAFAFA', 
                           'HoverColor': '#E8F4FD', 'SelectedColor': '#CCE4F7', ...}
                - 'Pagination': {'Height': 45, 'BackColor': '#F8F8F8', ...}
                - 'SearchBox': {'Width': 250, 'Height': 28, ...}
                
                Visibility properties for toolbars:
                - 'ShowToolbar': bool (default True)
                - 'ShowPagination': bool (default True)
                
                Visibility properties for Toolbar elements:
                - 'ShowSearch': bool (default True) - Search icon, box, button, and clear button
                - 'ShowCaseSensitive': bool (default True)
                - 'ShowExactMatch': bool (default True)
                - 'ShowPageSizeControl': bool (default True)
                
                Visibility properties for Pagination elements:
                - 'ShowRecordInfo': bool (default True)
                - 'ShowRecordNavigation': bool (default True) - All navigation buttons and page info
                
                Action buttons (for picker mode):
                - 'ShowActionButtons': bool (default False) - Show OK/Cancel buttons at bottom
            backend: Optional DataGridBackend for data source
            manager: Optional pre-configured DataGridManager
            
        Example:
            grid = DataGridPanel(form, props={
                'Dock': DockStyle.Fill,
                'ShowToolbar': True,
                'ShowPagination': True,
                'ShowCaseSensitive': False,  # Hide case-sensitive checkbox
                'ShowExactMatch': False,      # Hide exact match checkbox
                'Toolbar': {'Height': 60, 'BackColor': '#F0F0F0'},
                'Header': {'Height': 50, 'BackColor': '#333', 'ForeColor': '#FFF'},
                'Rows': {'Height': 40, 'AlternateBackColor': '#F5F5F5'},
                'Pagination': {'Height': 50}
            }, backend=my_backend)
        """
        # Extract visibility properties before sub-properties
        props = props or {}
        
        # Toolbar/Pagination visibility
        self._show_toolbar = props.pop('ShowToolbar', True)
        self._show_pagination = props.pop('ShowPagination', True)
        
        # Toolbar element visibility
        self._show_search = props.pop('ShowSearch', True)
        self._show_case_sensitive = props.pop('ShowCaseSensitive', True)
        self._show_exact_match = props.pop('ShowExactMatch', True)
        self._show_page_size_control = props.pop('ShowPageSizeControl', True)
        
        # Pagination element visibility
        self._show_record_info = props.pop('ShowRecordInfo', True)
        self._show_record_navigation = props.pop('ShowRecordNavigation', True)
        
        # Action buttons visibility (for picker mode)
        self._show_action_buttons = props.pop('ShowActionButtons', False)
        
        # Selection configuration
        selection_mode = props.pop('SelectionMode', SelectionMode.MULTIPLE)
        if isinstance(selection_mode, str):
            selection_mode = SelectionMode(selection_mode.lower())
        self._selection_mode = selection_mode
        self._show_row_checkboxes = props.pop('ShowRowCheckboxes', False)
        
        # Extract sub-properties before passing to parent
        self._toolbar_props = props.pop('Toolbar', {}) if props else {}
        self._header_props = props.pop('Header', {}) if props else {}
        self._rows_props = props.pop('Rows', {}) if props else {}
        self._pagination_props = props.pop('Pagination', {}) if props else {}
        self._searchbox_props = props.pop('SearchBox', {}) if props else {}
        
        defaults = {
            'Width': 800,
            'Height': 500,
            'BackColor': self.COLORS['background'],
        }
        if props:
            defaults.update(props)
        
        super().__init__(master_form, defaults)
        
        # Apply sub-properties to internal settings
        self._row_height = self._rows_props.get('Height', 36)
        self._header_height = self._header_props.get('Height', 40)
        
        # Update COLORS from sub-properties (instance copy)
        self.COLORS = self.COLORS.copy()
        if 'BackColor' in self._header_props:
            self.COLORS['header_bg'] = self._header_props['BackColor']
        if 'ForeColor' in self._header_props:
            self.COLORS['header_text'] = self._header_props['ForeColor']
        if 'BackColor' in self._rows_props:
            self.COLORS['row_bg'] = self._rows_props['BackColor']
        if 'AlternateBackColor' in self._rows_props:
            self.COLORS['row_alt_bg'] = self._rows_props['AlternateBackColor']
        if 'HoverColor' in self._rows_props:
            self.COLORS['row_hover'] = self._rows_props['HoverColor']
        if 'SelectedColor' in self._rows_props:
            self.COLORS['row_selected'] = self._rows_props['SelectedColor']
        if 'BackColor' in self._pagination_props:
            self.COLORS['pagination_bg'] = self._pagination_props['BackColor']
        
        # Setup manager
        if manager:
            self.manager = manager
        else:
            self.manager = DataGridManager(backend)
        
        # Wire up manager events
        self.manager.DataLoaded = self._on_data_loaded
        self.manager.DataLoadError = self._on_data_load_error
        self.manager.SelectionChanged = self._on_selection_changed
        
        # UI state
        self._row_widgets: List[Dict] = []
        self._column_headers: List[Label] = []
        
        # External event handlers
        self.RowClick: Callable[[object, Dict], None] = lambda s, e: None
        self.RowDoubleClick: Callable[[object, Dict], None] = lambda s, e: None
        self.SelectionChanged: Callable[[object, Dict], None] = lambda s, e: None
        self.DataLoaded: Callable[[object, Dict], None] = lambda s, e: None
        self.DataLoadError: Callable[[object, Dict], None] = lambda s, e: None
        
        # Action button events (for picker mode)
        self.OkClick: Callable[[object, Dict], None] = lambda s, e: None
        self.CancelClick: Callable[[object, Dict], None] = lambda s, e: None
        
        # Optional linked RecordFormPanel for detail view
        self._detail_panel = None
        
        # Build UI
        self._build_ui()
    
    def _build_ui(self):
        """Build the grid user interface."""
        # Top bar with search - apply toolbar props
        self._toolbar = None
        if self._show_toolbar:
            toolbar_defaults = {
                'Dock': DockStyle.Top,
                'Height': 50,
                'BackColor': self.COLORS['background']
            }
            toolbar_defaults.update(self._toolbar_props)
            self._toolbar = Panel(self, toolbar_defaults)
            self._build_toolbar()
        
        # Action buttons panel (OK/Cancel) - must be created before pagination for correct dock order
        self._action_panel = None
        self._ok_btn = None
        self._cancel_btn = None
        if self._show_action_buttons:
            self._action_panel = Panel(self, {
                'Dock': DockStyle.Bottom,
                'Height': 55,
                'BackColor': self.COLORS['pagination_bg']
            })
            self._build_action_buttons()
        
        # Pagination bar at bottom - apply pagination props
        self._pagination_bar = None
        if self._show_pagination:
            pagination_defaults = {
                'Dock': DockStyle.Bottom,
                'Height': 45,
                'BackColor': self.COLORS['pagination_bg']
            }
            pagination_defaults.update(self._pagination_props)
            self._pagination_bar = Panel(self, pagination_defaults)
            self._build_pagination()
        
        # Main grid area
        self._grid_container = Panel(self, {
            'Dock': DockStyle.Fill,
            'BackColor': self.COLORS['background']
        })
        
        # Header row - apply header props
        header_defaults = {
            'Dock': DockStyle.Top,
            'Height': self._header_height,
            'BackColor': self.COLORS['header_bg']
        }
        # Only apply positioning props, not color (handled separately)
        for key in ['Height', 'Dock']:
            if key in self._header_props:
                header_defaults[key] = self._header_props[key]
        self._header_panel = Panel(self._grid_container, header_defaults)
        
        # Data rows container with scroll
        self._rows_panel = Panel(self._grid_container, {
            'Dock': DockStyle.Fill,
            'BackColor': self.COLORS['background'],
            'AutoScroll': True
        })
    
    def _build_toolbar(self):
        """Build the toolbar with search."""
        # Keep references to prevent garbage collection
        self._toolbar_widgets = []
        
        # Initialize all toolbar elements as None
        self._search_icon = None
        self._search_box = None
        self._search_btn = None
        self._clear_btn = None
        self._case_sensitive_chk = None
        self._exact_match_chk = None
        self._show_label = None
        self._page_size_box = None
        self._page_size_btn = None
        
        # Track current X position for dynamic layout
        current_x = 10
        
        # Search controls (ShowSearch controls icon, box, search button, and clear button)
        if self._show_search:
            # Search icon/label
            self._search_icon = Label(self._toolbar, {
                'Text': '🔍',
                'Left': current_x, 'Top': 14,
                'Width': 25, 'Height': 25,
                'Font': Font('Segoe UI', 12)
            })
            current_x += 30
            
            # Search textbox
            searchbox_defaults = {
                'Left': current_x, 'Top': 12,
                'Width': 250, 'Height': 28,
                'Font': Font('Segoe UI', 10),
                'PlaceholderText': 'Search...'
            }
            searchbox_defaults.update(self._searchbox_props)
            self._search_box = TextBox(self._toolbar, searchbox_defaults)
            self._search_box.BindKey('<Return>', lambda e: self._do_search())
            current_x += searchbox_defaults['Width'] + 10
            
            # Search button (part of ShowSearch)
            self._search_btn = Button(self._toolbar, {
                'Text': 'Search',
                'Left': current_x, 'Top': 12,
                'Width': 70, 'Height': 28,
                'Font': Font('Segoe UI', 9)
            })
            self._search_btn.Click = lambda s, e: self._do_search()
            current_x += 75
            
            # Clear button
            self._clear_btn = Button(self._toolbar, {
                'Text': 'Clear',
                'Left': current_x, 'Top': 12,
                'Width': 60, 'Height': 28,
                'Font': Font('Segoe UI', 9)
            })
            self._clear_btn.Click = lambda s, e: self._clear_search()
            current_x += 70
        
        # Case-sensitive checkbox
        if self._show_case_sensitive:
            self._case_sensitive_chk = CheckBox(self._toolbar, {
                'Text': 'Aa',
                'Left': current_x, 'Top': 14,
                'Width': 45, 'Height': 24,
                'Font': Font('Segoe UI', 9),
                'Checked': False
            })
            self._case_sensitive_chk.CheckedChanged = lambda s, e: self._on_case_sensitive_changed()
            current_x += 45
        
        # Exact match checkbox
        if self._show_exact_match:
            self._exact_match_chk = CheckBox(self._toolbar, {
                'Text': 'Exact',
                'Left': current_x, 'Top': 14,
                'Width': 55, 'Height': 24,
                'Font': Font('Segoe UI', 9),
                'Checked': False
            })
            self._exact_match_chk.CheckedChanged = lambda s, e: self._on_exact_match_changed()
            current_x += 65
        
        # Page size controls
        if self._show_page_size_control:
            self._show_label = Label(self._toolbar, {
                'Text': 'Rows:',
                'Left': current_x, 'Top': 16,
                'Width': 40, 'Height': 20,
                'Font': Font('Segoe UI', 9),
                'ForeColor': self.COLORS['text_secondary']
            })
            
            self._page_size_box = TextBox(self._toolbar, {
                'Text': str(self.manager.page_size),
                'Left': current_x + 40, 'Top': 12,
                'Width': 50, 'Height': 28,
                'Font': Font('Segoe UI', 9)
            })
            self._page_size_box.BindKey('<Return>', lambda e: self._apply_page_size())
            
            self._page_size_btn = Button(self._toolbar, {
                'Text': 'Apply',
                'Left': current_x + 95, 'Top': 12,
                'Width': 50, 'Height': 28,
                'Font': Font('Segoe UI', 9)
            })
            self._page_size_btn.Click = lambda s, e: self._apply_page_size()
    
    def _build_action_buttons(self):
        """Build the OK/Cancel action buttons panel."""
        # Cancel button (left)
        self._cancel_btn = Button(self._action_panel, {
            'Text': 'Cancel',
            'Left': self.Width - 230, 'Top': 12,
            'Width': 100, 'Height': 32,
            'Font': Font('Segoe UI', 10),
            'Anchor': AnchorStyles.Right | AnchorStyles.Bottom
        })
        self._cancel_btn.Click = lambda s, e: self._on_cancel_click()
        
        # OK button (right)
        self._ok_btn = Button(self._action_panel, {
            'Text': 'OK',
            'Left': self.Width - 120, 'Top': 12,
            'Width': 100, 'Height': 32,
            'Font': Font('Segoe UI', 10),
            'BackColor': self.COLORS['primary'],
            'ForeColor': '#FFFFFF',
            'Anchor': AnchorStyles.Right | AnchorStyles.Bottom
        })
        self._ok_btn.Click = lambda s, e: self._on_ok_click()
    
    def _on_ok_click(self):
        """Handle OK button click."""
        self.OkClick(self, {
            'selected_records': self.manager.selected_records,
            'selected_indices': self.manager.selected_indices
        })
    
    def _on_cancel_click(self):
        """Handle Cancel button click."""
        self.CancelClick(self, {})
    
    def _build_pagination(self):
        """Build the pagination bar."""
        # Initialize all pagination elements as None
        self._info_label = None
        self._btn_first = None
        self._btn_prev = None
        self._page_label = None
        self._btn_next = None
        self._btn_last = None
        
        # Info label (left side)
        if self._show_record_info:
            self._info_label = Label(self._pagination_bar, {
                'Text': 'Showing 0 - 0 of 0 records',
                'Left': 15, 'Top': 13,
                'Width': 250, 'Height': 20,
                'Font': Font('Segoe UI', 9),
                'ForeColor': self.COLORS['text_secondary']
            })
        
        # Navigation buttons and page info (ShowRecordNavigation controls all)
        if self._show_record_navigation:
            btn_width = 35
            btn_height = 28
            current_x = 400
            
            # First page
            self._btn_first = Button(self._pagination_bar, {
                'Text': '⏮',
                'Left': current_x, 'Top': 9,
                'Width': btn_width, 'Height': btn_height,
                'Font': Font('Segoe UI', 10)
            })
            self._btn_first.Click = lambda s, e: self.manager.first_page()
            current_x += 40
            
            # Previous page
            self._btn_prev = Button(self._pagination_bar, {
                'Text': '◀',
                'Left': current_x, 'Top': 9,
                'Width': btn_width, 'Height': btn_height,
                'Font': Font('Segoe UI', 10)
            })
            self._btn_prev.Click = lambda s, e: self.manager.previous_page()
            current_x += 45
            
            # Page indicator
            self._page_label = Label(self._pagination_bar, {
                'Text': 'Page 1 of 1',
                'Left': current_x, 'Top': 13,
                'Width': 100, 'Height': 20,
                'Font': Font('Segoe UI', 9),
                'ForeColor': self.COLORS['text']
            })
            current_x += 105
            
            # Next page
            self._btn_next = Button(self._pagination_bar, {
                'Text': '▶',
                'Left': current_x, 'Top': 9,
                'Width': btn_width, 'Height': btn_height,
                'Font': Font('Segoe UI', 10)
            })
            self._btn_next.Click = lambda s, e: self.manager.next_page()
            current_x += 40
            
            # Last page
            self._btn_last = Button(self._pagination_bar, {
                'Text': '⏭',
                'Left': current_x, 'Top': 9,
                'Width': btn_width, 'Height': btn_height,
                'Font': Font('Segoe UI', 10)
            })
            self._btn_last.Click = lambda s, e: self.manager.last_page()
    
    def _build_headers(self):
        """Build column headers."""
        # Clear existing headers
        for header in self._column_headers:
            if hasattr(header, '_tk_widget') and header._tk_widget:
                header._tk_widget.destroy()
        self._column_headers = []
        
        columns = self.manager.columns
        if not columns:
            return
        
        x = 0
        for col in columns:
            if not col.visible:
                continue
            
            # Determine sort indicator icon
            sort_icon = ""
            if self.manager.sort_column == col.name:
                if self.manager.sort_order == SortOrder.ASCENDING:
                    sort_icon = " ↑"  # Up arrow for ascending
                elif self.manager.sort_order == SortOrder.DESCENDING:
                    sort_icon = " ↓"  # Down arrow for descending
            elif col.sortable:
                sort_icon = " ⇅"  # Up-down arrow indicating sortable (subtle)
            
            header = Label(self._header_panel, {
                'Text': col.header + sort_icon,
                'Left': x, 'Top': 0,
                'Width': col.width,
                'Height': self._header_height,
                'Font': Font('Segoe UI', 10, FontStyle.Bold),
                'ForeColor': self.COLORS['header_text'],
                'BackColor': self.COLORS['header_bg']
            })
            
            # Make header clickable for sorting
            if col.sortable:
                header.MouseEnter = lambda s, e, h=header: self._on_header_hover(h, True)
                header.MouseLeave = lambda s, e, h=header: self._on_header_hover(h, False)
                header.Click = lambda s, e, c=col: self.manager.sort(c.name)
            
            self._column_headers.append(header)
            x += col.width
    
    def _on_header_hover(self, header: Label, entering: bool):
        """Handle header hover effect."""
        if entering:
            header.BackColor = '#E5E5E5'
        else:
            header.BackColor = self.COLORS['header_bg']
    
    def _build_rows(self):
        """Build data rows."""
        # Clear existing rows
        for row_data in self._row_widgets:
            for widget in row_data.get('widgets', []):
                if hasattr(widget, '_tk_widget') and widget._tk_widget:
                    widget._tk_widget.destroy()
            if 'panel' in row_data and hasattr(row_data['panel'], '_tk_widget'):
                row_data['panel']._tk_widget.destroy()
        self._row_widgets = []
        
        # Clear no data label if exists
        if hasattr(self, '_no_data_label') and self._no_data_label:
            if hasattr(self._no_data_label, '_tk_widget') and self._no_data_label._tk_widget:
                self._no_data_label._tk_widget.destroy()
            self._no_data_label = None
        
        records = self.manager.records
        columns = [c for c in self.manager.columns if c.visible]
        
        if not records or not columns:
            # Show "no data" message
            self._show_no_data()
            return
        
        y = 0
        for idx, record in enumerate(records):
            # Alternate row colors
            bg_color = self.COLORS['row_bg'] if idx % 2 == 0 else self.COLORS['row_alt_bg']
            
            # Check if selected
            if idx in self.manager.selected_indices:
                bg_color = self.COLORS['row_selected']
            
            row_panel = Panel(self._rows_panel, {
                'Left': 0, 'Top': y,
                'Width': sum(c.width for c in columns),
                'Height': self._row_height,
                'BackColor': bg_color
            })
            
            widgets = []
            x = 0
            for col in columns:
                value = self.manager.get_formatted_value(record, col.name)
                
                # Determine alignment
                anchor = 'w'  # left
                padx = 8
                if col.align == 'center':
                    anchor = 'center'
                elif col.align == 'right':
                    anchor = 'e'
                    padx = 8
                
                cell = Label(row_panel, {
                    'Text': value,
                    'Left': x, 'Top': 0,
                    'Width': col.width,
                    'Height': self._row_height,
                    'Font': Font('Segoe UI', 10),
                    'ForeColor': self.COLORS['text'],
                    'BackColor': bg_color
                })
                widgets.append(cell)
                x += col.width
            
            # Row events
            row_panel.MouseEnter = lambda s, e, rp=row_panel, i=idx: self._on_row_hover(rp, i, True)
            row_panel.MouseLeave = lambda s, e, rp=row_panel, i=idx: self._on_row_hover(rp, i, False)
            row_panel.Click = lambda s, e, i=idx, r=record: self._on_row_click(i, r, e)
            row_panel.DoubleClick = lambda s, e, i=idx, r=record: self._on_row_double_click(i, r)
            
            # Also bind events to cells
            for cell in widgets:
                cell.MouseEnter = lambda s, e, rp=row_panel, i=idx: self._on_row_hover(rp, i, True)
                cell.MouseLeave = lambda s, e, rp=row_panel, i=idx: self._on_row_hover(rp, i, False)
                cell.Click = lambda s, e, i=idx, r=record: self._on_row_click(i, r, e)
                cell.DoubleClick = lambda s, e, i=idx, r=record: self._on_row_double_click(i, r)
            
            self._row_widgets.append({
                'panel': row_panel,
                'widgets': widgets,
                'record': record,
                'index': idx
            })
            
            y += self._row_height
    
    def _show_no_data(self):
        """Show a 'no data' message."""
        self._no_data_label = Label(self._rows_panel, {
            'Text': 'No records found',
            'Left': 0, 'Top': 50,
            'Width': 300, 'Height': 30,
            'Font': Font('Segoe UI', 11),
            'ForeColor': self.COLORS['text_secondary']
        })
    
    def _on_row_hover(self, row_panel: Panel, index: int, entering: bool):
        """Handle row hover effect."""
        if index in self.manager.selected_indices:
            return  # Don't change selected row color
        
        if entering:
            color = self.COLORS['row_hover']
        else:
            color = self.COLORS['row_bg'] if index % 2 == 0 else self.COLORS['row_alt_bg']
        
        row_panel.BackColor = color
        # Update cell colors too
        if index < len(self._row_widgets):
            for widget in self._row_widgets[index].get('widgets', []):
                widget.BackColor = color
    
    def _on_row_click(self, index: int, record: Dict, event=None):
        """Handle row click."""
        # Always fire the RowClick event
        self.RowClick(self, {'index': index, 'record': record})
        
        # Check selection mode
        if self._selection_mode == SelectionMode.NONE:
            return
        
        # Check for modifier keys (event is EventArgs)
        ctrl_pressed = False
        shift_pressed = False
        if event:
            if hasattr(event, 'Control'):
                ctrl_pressed = event.Control
            if hasattr(event, 'Shift'):
                shift_pressed = event.Shift
        
        if self._selection_mode == SelectionMode.SINGLE:
            # Single selection mode - always select only this record
            self.manager.select_record(index, multi_select=False)
        elif self._selection_mode == SelectionMode.MULTIPLE:
            # Multiple selection mode - respect Ctrl and Shift
            if shift_pressed:
                # Shift+Click: Select range from last selected to current
                self.manager.select_range(index)
            elif ctrl_pressed:
                # Ctrl+Click: Toggle selection
                self.manager.select_record(index, multi_select=True)
            else:
                # Normal click: Select only this record
                self.manager.select_record(index, multi_select=False)
    
    def _on_row_double_click(self, index: int, record: Dict):
        """Handle row double-click."""
        self.RowDoubleClick(self, {'index': index, 'record': record})
    
    def _update_row_selection(self):
        """Update row visual selection state."""
        for row_data in self._row_widgets:
            idx = row_data['index']
            is_selected = idx in self.manager.selected_indices
            
            if is_selected:
                color = self.COLORS['row_selected']
            else:
                color = self.COLORS['row_bg'] if idx % 2 == 0 else self.COLORS['row_alt_bg']
            
            row_data['panel'].BackColor = color
            for widget in row_data.get('widgets', []):
                widget.BackColor = color
    
    def _update_pagination(self):
        """Update pagination controls."""
        info = self.manager.page_info
        
        # Update info label
        if self._info_label:
            if info.total_records > 0:
                self._info_label.Text = f"Showing {info.start_record} - {info.end_record} of {info.total_records} records"
            else:
                self._info_label.Text = "No records found"
        
        # Update page label
        if self._page_label:
            self._page_label.Text = f"Page {info.current_page} of {max(1, info.total_pages)}"
        
        # Enable/disable navigation buttons
        has_prev = self.manager.has_previous_page
        has_next = self.manager.has_next_page
        
        # Visual feedback for disabled state would require additional implementation
    
    def _do_search(self):
        """Perform search with current options."""
        if not self._search_box:
            return
        case_sensitive = self._case_sensitive_chk.Checked if self._case_sensitive_chk else False
        exact_match = self._exact_match_chk.Checked if self._exact_match_chk else False
        self.manager.search(self._search_box.Text, case_sensitive, exact_match)
    
    def _on_case_sensitive_changed(self):
        """Handle case-sensitive checkbox change."""
        if not self._case_sensitive_chk:
            return
        # Update manager state
        self.manager.case_sensitive = self._case_sensitive_chk.Checked
        # Re-run search if there's search text
        if self._search_box and self._search_box.Text:
            self._do_search()
    
    def _on_exact_match_changed(self):
        """Handle exact match checkbox change."""
        if not self._exact_match_chk:
            return
        # Update manager state
        self.manager.exact_match = self._exact_match_chk.Checked
        # Re-run search if there's search text
        if self._search_box and self._search_box.Text:
            self._do_search()
    
    def _clear_search(self):
        """Clear search."""
        if self._search_box:
            self._search_box.Text = ""
        self.manager.clear_search()
    
    def _apply_page_size(self):
        """Apply the page size from the input box."""
        if not self._page_size_box:
            return
        try:
            text = self._page_size_box.Text
            size = int(text.strip()) if text else self.manager.page_size
            if size < 1:
                size = 1
            elif size > 1000:
                size = 1000
            self._page_size_box.Text = str(size)
            self.manager.page_size = size
        except ValueError:
            # Restore current value if invalid input
            self._page_size_box.Text = str(self.manager.page_size)
    
    def _set_page_size(self, size: int):
        """Set the page size and update the input box."""
        self.manager.page_size = size
        if self._page_size_box:
            self._page_size_box.Text = str(size)
    
    def _on_data_loaded(self, sender, args):
        """Handle data loaded event."""
        self._build_headers()
        self._build_rows()
        self._update_pagination()
        # Update scroll region after adding rows
        if hasattr(self._rows_panel, 'UpdateScroll'):
            self._rows_panel.UpdateScroll()
        self.DataLoaded(self, args)
    
    def _on_data_load_error(self, sender, args):
        """Handle data load error event."""
        self.DataLoadError(self, args)
    
    def _on_selection_changed(self, sender, args):
        """Handle selection changed event."""
        self._update_row_selection()
        
        # Update linked DetailPanel if set
        if self._detail_panel is not None:
            records = args.get('selected_records', [])
            if records:
                # Load first selected record into the detail panel
                self._detail_panel.load_record(records[0])
            else:
                # Clear the detail panel when no selection
                self._detail_panel.clear()
        
        self.SelectionChanged(self, args)
    
    # =========================================================================
    # Visibility Properties
    # =========================================================================
    
    @property
    def ShowToolbar(self) -> bool:
        """Get whether the toolbar is visible."""
        return self._show_toolbar
    
    @ShowToolbar.setter
    def ShowToolbar(self, value: bool):
        """Set whether the toolbar is visible."""
        if self._show_toolbar == value:
            return
        self._show_toolbar = value
        if self._toolbar:
            self._toolbar.Visible = value
    
    @property
    def ShowPagination(self) -> bool:
        """Get whether the pagination bar is visible."""
        return self._show_pagination
    
    @ShowPagination.setter
    def ShowPagination(self, value: bool):
        """Set whether the pagination bar is visible."""
        if self._show_pagination == value:
            return
        self._show_pagination = value
        if self._pagination_bar:
            self._pagination_bar.Visible = value
    
    @property
    def ShowSearch(self) -> bool:
        """Get whether the search controls are visible (icon, box, search button, clear button)."""
        return self._show_search
    
    @property
    def ShowCaseSensitive(self) -> bool:
        """Get whether the case-sensitive checkbox is visible."""
        return self._show_case_sensitive
    
    @property
    def ShowExactMatch(self) -> bool:
        """Get whether the exact match checkbox is visible."""
        return self._show_exact_match
    
    @property
    def ShowPageSizeControl(self) -> bool:
        """Get whether the page size control is visible."""
        return self._show_page_size_control
    
    @property
    def ShowRecordInfo(self) -> bool:
        """Get whether the record info label is visible."""
        return self._show_record_info
    
    @property
    def ShowRecordNavigation(self) -> bool:
        """Get whether the record navigation buttons and page info are visible."""
        return self._show_record_navigation
    
    @property
    def ShowActionButtons(self) -> bool:
        """Get whether the OK/Cancel action buttons are visible."""
        return self._show_action_buttons
    
    @ShowActionButtons.setter
    def ShowActionButtons(self, value: bool):
        """Set whether the OK/Cancel action buttons are visible."""
        if self._show_action_buttons == value:
            return
        self._show_action_buttons = value
        if self._action_panel:
            self._action_panel.Visible = value
    
    # =========================================================================
    # Selection Properties and Methods
    # =========================================================================
    
    @property
    def SelectionMode(self) -> SelectionMode:
        """
        Get the selection mode.
        
        Returns:
            SelectionMode.NONE - No selection allowed
            SelectionMode.SINGLE - Only one row can be selected
            SelectionMode.MULTIPLE - Multiple rows can be selected (Ctrl/Shift+Click)
        """
        return self._selection_mode
    
    @SelectionMode.setter
    def SelectionMode(self, value: SelectionMode):
        """Set the selection mode."""
        if isinstance(value, str):
            value = SelectionMode(value.lower())
        self._selection_mode = value
        # Clear selection when changing mode
        self.ClearSelection()
    
    @property
    def ShowRowCheckboxes(self) -> bool:
        """Get whether row selection checkboxes are shown."""
        return self._show_row_checkboxes
    
    @ShowRowCheckboxes.setter
    def ShowRowCheckboxes(self, value: bool):
        """Set whether row selection checkboxes are shown."""
        if self._show_row_checkboxes == value:
            return
        self._show_row_checkboxes = value
        self._rebuild_grid()
    
    @property
    def selected_records(self) -> List[Dict[str, Any]]:
        """Get the currently selected records."""
        return self.manager.selected_records
    
    @property
    def selected_indices(self) -> List[int]:
        """Get the indices of the currently selected records."""
        return self.manager.selected_indices
    
    @property
    def selected_record(self) -> Optional[Dict[str, Any]]:
        """Get the first selected record (convenience property for single selection)."""
        records = self.manager.selected_records
        return records[0] if records else None
    
    def SelectAll(self):
        """Select all records on the current page."""
        if self._selection_mode == SelectionMode.NONE:
            return
        if self._selection_mode == SelectionMode.SINGLE:
            return  # Can't select all in single mode
        self.manager.select_all()
    
    def ClearSelection(self):
        """Clear all selections."""
        self.manager.clear_selection()
    
    def SelectRecord(self, index: int):
        """
        Select a record by index.
        
        Args:
            index: The index of the record to select.
        """
        if self._selection_mode == SelectionMode.NONE:
            return
        self.manager.select_record(index, multi_select=False)
    
    def ToggleRecordSelection(self, index: int):
        """
        Toggle selection of a record (for multi-select mode).
        
        Args:
            index: The index of the record to toggle.
        """
        if self._selection_mode != SelectionMode.MULTIPLE:
            return
        self.manager.select_record(index, multi_select=True)
    
    @property
    def DetailPanel(self):
        """
        Get/Set an optional RecordFormPanel for displaying selected record details.
        
        When set, the panel will automatically update when a row is selected in the grid.
        The RecordFormPanel must have fields that match the column names in the grid data.
        
        Example:
            detail = RecordFormPanel(right_panel, {'Backend': backend})
            grid.DetailPanel = detail  # Now selection automatically updates the detail panel
        """
        return self._detail_panel
    
    @DetailPanel.setter
    def DetailPanel(self, panel):
        """Set the linked RecordFormPanel for detail view."""
        self._detail_panel = panel

    # =========================================================================
    # Column Visibility Methods
    # =========================================================================
    
    def hide_column(self, column_names):
        """
        Hide one or more columns by name.
        
        Args:
            column_names: Column name (str) or list of column names to hide.
        """
        if isinstance(column_names, str):
            column_names = [column_names]
        
        changed = False
        for col in self.manager.columns:
            if col.name in column_names and col.visible:
                col.visible = False
                changed = True
        
        if changed:
            self._rebuild_grid()
    
    def show_column(self, column_names):
        """
        Show one or more previously hidden columns.
        
        Args:
            column_names: Column name (str) or list of column names to show.
        """
        if isinstance(column_names, str):
            column_names = [column_names]
        
        changed = False
        for col in self.manager.columns:
            if col.name in column_names and not col.visible:
                col.visible = True
                changed = True
        
        if changed:
            self._rebuild_grid()
    
    def set_column_visibility(self, column_names, visible: bool):
        """
        Set the visibility of one or more columns.
        
        Args:
            column_names: Column name (str) or list of column names.
            visible: True to show, False to hide.
        """
        if visible:
            self.show_column(column_names)
        else:
            self.hide_column(column_names)
    
    def get_column_visibility(self, column_name: str) -> bool:
        """
        Get the visibility state of a column.
        
        Args:
            column_name: The name of the column.
            
        Returns:
            True if visible, False if hidden, None if column not found.
        """
        for col in self.manager.columns:
            if col.name == column_name:
                return col.visible
        return None
    
    def get_visible_columns(self) -> List[str]:
        """
        Get the names of all visible columns.
        
        Returns:
            List of visible column names.
        """
        return [col.name for col in self.manager.columns if col.visible]
    
    def get_hidden_columns(self) -> List[str]:
        """
        Get the names of all hidden columns.
        
        Returns:
            List of hidden column names.
        """
        return [col.name for col in self.manager.columns if not col.visible]
    
    def _rebuild_grid(self):
        """Rebuild the grid after column visibility changes."""
        self._build_header()
        self._update_data()

    def refresh(self):
        """Refresh the grid data."""
        self.manager.refresh()


# =============================================================================
# Example Usage
# =============================================================================
if __name__ == "__main__":
    import random
    from datetime import datetime, timedelta
    from winformpy.winformpy import Form, RichTextBox
    from data_grid_backend import (
        DataGridBackend, DataRequest, DataResponse, 
        ColumnDefinition, PageInfo, DataType, SortOrder
    )
    
    # Add parent directory to path for record_form import
    _ui_elements_dir = os.path.join(os.path.dirname(__file__), '..')
    if _ui_elements_dir not in sys.path:
        sys.path.insert(0, _ui_elements_dir)
    _record_form_dir = os.path.join(os.path.dirname(__file__), '..', 'record_form')
    if _record_form_dir not in sys.path:
        sys.path.insert(0, _record_form_dir)
    
    # Import RecordFormPanel for integration demo
    try:
        from record_form_panel import RecordFormPanel
        from record_form_backend import InMemoryRecordBackend
        RECORD_FORM_AVAILABLE = True
    except ImportError as e:
        print(f"Note: RecordFormPanel not available ({e})")
        RECORD_FORM_AVAILABLE = False
    
    # =========================================================================
    # Demo Backend - Simulates a database with 200 records
    # =========================================================================
    class DemoDataBackend(DataGridBackend):
        """Demo backend that generates fake employee data."""
        
        def __init__(self, record_count: int = 200):
            """Generate demo data."""
            self._data = self._generate_data(record_count)
            self._columns = [
                ColumnDefinition("id", "ID", DataType.INTEGER, width=60, align="right"),
                ColumnDefinition("name", "Full Name", DataType.STRING, width=180),
                ColumnDefinition("email", "Email", DataType.STRING, width=220),
                ColumnDefinition("department", "Department", DataType.STRING, width=120),
                ColumnDefinition("salary", "Salary", DataType.CURRENCY, width=100, align="right"),
                ColumnDefinition("hire_date", "Hire Date", DataType.DATE, width=100, align="center"),
                ColumnDefinition("active", "Active", DataType.BOOLEAN, width=70, align="center"),
                ColumnDefinition("performance", "Performance", DataType.PERCENTAGE, width=100, align="right"),
            ]
        
        def _generate_data(self, count: int) -> List[Dict]:
            """Generate fake employee records."""
            first_names = ["John", "Jane", "Michael", "Emily", "David", "Sarah", 
                          "Robert", "Lisa", "William", "Maria", "James", "Jennifer",
                          "Carlos", "Ana", "Pedro", "Laura", "Diego", "Sofia"]
            last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia",
                         "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez",
                         "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore"]
            departments = ["Engineering", "Marketing", "Sales", "HR", "Finance", 
                          "Operations", "IT", "Legal", "Product", "Design"]
            
            records = []
            for i in range(1, count + 1):
                first = random.choice(first_names)
                last = random.choice(last_names)
                dept = random.choice(departments)
                
                records.append({
                    "id": i,
                    "name": f"{first} {last}",
                    "email": f"{first.lower()}.{last.lower()}@company.com",
                    "department": dept,
                    "salary": round(random.uniform(35000, 150000), 2),
                    "hire_date": datetime.now() - timedelta(days=random.randint(30, 3650)),
                    "active": random.random() > 0.15,
                    "performance": round(random.uniform(60, 100), 1),
                })
            return records
        
        def get_columns(self) -> List[ColumnDefinition]:
            """Return column definitions."""
            return self._columns
        
        def fetch_data(self, request: DataRequest) -> DataResponse:
            """Fetch data with pagination, sorting, and filtering."""
            # Start with all data
            filtered = self._data.copy()
            
            # Apply search filter
            if request.search_text:
                search = request.search_text
                search_lower = search.lower()
                
                def matches(value: str) -> bool:
                    """Check if value matches search criteria."""
                    val = str(value)
                    if request.exact_match:
                        # Exact match
                        if request.case_sensitive:
                            return val == search
                        else:
                            return val.lower() == search_lower
                    else:
                        # Contains match
                        if request.case_sensitive:
                            return search in val
                        else:
                            return search_lower in val.lower()
                
                filtered = [
                    r for r in filtered
                    if matches(r.get("name", "")) or
                       matches(r.get("email", "")) or
                       matches(r.get("department", ""))
                ]
            
            # Apply sorting
            if request.sort_column and request.sort_order != SortOrder.NONE:
                reverse = request.sort_order == SortOrder.DESCENDING
                filtered.sort(
                    key=lambda x: (x.get(request.sort_column) is None, x.get(request.sort_column)),
                    reverse=reverse
                )
            
            # Calculate pagination
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
    
    # =========================================================================
    # Demo 1: Basic DataGrid with Events
    # =========================================================================
    def demo_basic():
        """Basic DataGrid demo with event handlers."""
        # Create main form
        form = Form()
        form.Text = "DataGrid Panel Demo - Employee Database"
        form.Width = 1024
        form.Height = 700
        form.StartPosition = 'CenterScreen'
        form.ApplyLayout()
        
        # Create backend with 200 records
        backend = DemoDataBackend(200)
        manager = DataGridManager(backend)
        
        # Create data grid panel
        grid = DataGridPanel(form, props={
            'Dock': DockStyle.Fill
        }, manager=manager)
        
        # Handle events
        def on_row_click(sender, args):
            record = args.get('record', {})
            print(f"Clicked: {record.get('name')} ({record.get('department')})")
        
        def on_selection_changed(sender, args):
            selected = args.get('selected_records', [])
            indices = args.get('selected_indices', [])
            if len(selected) == 1:
                print(f"Selected: {selected[0].get('name')}")
            elif len(selected) > 1:
                names = [r.get('name') for r in selected]
                print(f"Selected {len(selected)} records (indices {indices}): {', '.join(names)}")
        
        def on_row_double_click(sender, args):
            record = args.get('record', {})
            print(f"Opening details for: {record.get('name')}")
            
            # Show RecordFormPanel in a dialog if available
            if RECORD_FORM_AVAILABLE:
                # Create a dialog form
                dialog = Form()
                dialog.Text = f"Employee Details - {record.get('name', 'Unknown')}"
                dialog.Width = 450
                dialog.Height = 450
                dialog.StartPosition = 'CenterScreen'
                dialog.ApplyLayout()
                
                # Create backend with the single record
                detail_backend = InMemoryRecordBackend(
                    records=[record.copy()],
                    primary_key='id'
                )
                
                # Define columns for the form using ColumnDefinition
                form_columns = [
                    ColumnDefinition('id', 'Employee ID', DataType.INTEGER),
                    ColumnDefinition('name', 'Full Name', DataType.STRING),
                    ColumnDefinition('email', 'Email', DataType.STRING),
                    ColumnDefinition('department', 'Department', DataType.STRING),
                    ColumnDefinition('salary', 'Salary', DataType.CURRENCY),
                    ColumnDefinition('hire_date', 'Hire Date', DataType.DATE),
                ]
                
                # Create RecordFormPanel
                detail_form = RecordFormPanel(dialog, props={
                    'Dock': DockStyle.Fill,
                    'Backend': detail_backend,
                    'Columns': form_columns,
                    'Record': record,
                    'ShowInsertButton': False,
                    'ShowDeleteButton': False,
                    'ShowUpdateButton': True,
                })
                
                # Show the dialog
                dialog.ShowDialog()
            else:
                # Fallback: just print details
                print(f"  Email: {record.get('email')}")
                print(f"  Salary: ${record.get('salary'):,.2f}")
                print(f"  Hired: {record.get('hire_date').strftime('%Y-%m-%d')}")
        
        def on_data_loaded(sender, args):
            info = args.get('page_info')
            if info:
                print(f"Loaded {len(args.get('records', []))} records (Page {info.current_page} of {info.total_pages})")
        
        grid.RowClick = on_row_click
        grid.RowDoubleClick = on_row_double_click
        grid.DataLoaded = on_data_loaded
        grid.SelectionChanged = on_selection_changed
        
        # Load initial data
        manager.refresh()
        
        # Print instructions
        print("=" * 60)
        print("DataGrid Panel Demo - Employee Database (200 records)")
        print("=" * 60)
        print("\nFeatures:")
        print("  - Click column headers to sort (toggle asc/desc)")
        print("  - Use search box to filter by name, email, or department")
        print("  - Use navigation buttons for pagination")
        print("  - Click a row to select")
        print("  - Ctrl+Click to add/remove from selection")
        print("  - Shift+Click to select a range")
        print("  - RowDoubleClick event available for custom actions")
        print("=" * 60)
        
        # Run application
        form.ShowDialog()
    
    # Run the demo
    demo_basic()
