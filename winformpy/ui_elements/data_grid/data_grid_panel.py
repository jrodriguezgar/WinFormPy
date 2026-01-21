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
    Panel, Label, TextBox, Button, CheckBox, MaskedTextBox,
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
        
        # CRUD configuration
        self._allow_edit = props.pop('AllowEdit', False)
        self._allow_add = props.pop('AllowAdd', False)
        self._allow_delete = props.pop('AllowDelete', False)
        self._show_action_column = props.pop('ShowActionColumn', False)
        self._action_column_width = props.pop('ActionColumnWidth', 100)
        self._editing_row_index = None  # Index of row currently being edited
        self._is_adding_row = False  # True if adding a new row
        
        # Date/Time format configuration (locale-aware)
        # Supported formats: 'ISO' (YYYY-MM-DD), 'EU' (DD/MM/YYYY), 'US' (MM/DD/YYYY), 'system' (auto-detect)
        self._date_format = props.pop('DateFormat', 'system')
        self._time_format = props.pop('TimeFormat', '24h')  # '24h' or '12h'
        
        # Number format configuration (locale-aware)
        # 'US': 1,234.56 (comma thousands, dot decimal)
        # 'EU': 1.234,56 (dot thousands, comma decimal)
        # 'system': auto-detect from locale
        self._number_format = props.pop('NumberFormat', 'system')
        
        # Currency configuration
        # Symbol: '$', '€', '£', etc. or 'system' for auto-detect
        # Position: 'before' ($100) or 'after' (100 €)
        self._currency_symbol = props.pop('CurrencySymbol', 'system')
        self._currency_position = props.pop('CurrencyPosition', 'system')  # 'before', 'after', 'system'
        
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
        
        # CRUD event handlers
        self.RecordCreated: Callable[[object, Dict], None] = lambda s, e: None
        self.RecordUpdated: Callable[[object, Dict], None] = lambda s, e: None
        self.RecordDeleted: Callable[[object, Dict], None] = lambda s, e: None
        self.EditStarted: Callable[[object, Dict], None] = lambda s, e: None
        self.EditCancelled: Callable[[object, Dict], None] = lambda s, e: None
        
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
        self._add_btn = None
        
        # Track current X position for dynamic layout
        current_x = 10
        
        # Add button (for CRUD - placed first on left)
        if self._allow_add:
            self._add_btn = Button(self._toolbar, {
                'Text': '➕',
                'Left': current_x, 'Top': 12,
                'Width': 32, 'Height': 28,
                'Font': Font('Segoe UI', 12),
                'BackColor': '#4CAF50',
                'ForeColor': '#FFFFFF'
            })
            self._add_btn.Click = lambda s, e: self.BeginAdd()
            current_x += 40
        
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
        
        # Add action column header if enabled
        if self._show_action_column:
            action_header = Label(self._header_panel, {
                'Text': 'Actions',
                'Left': x, 'Top': 0,
                'Width': self._action_column_width,
                'Height': self._header_height,
                'Font': Font('Segoe UI', 10, FontStyle.Bold),
                'ForeColor': self.COLORS['header_text'],
                'BackColor': self.COLORS['header_bg']
            })
            self._column_headers.append(action_header)
    
    def _on_header_hover(self, header: Label, entering: bool):
        """Handle header hover effect."""
        if entering:
            header.BackColor = '#E5E5E5'
        else:
            header.BackColor = self.COLORS['header_bg']
    
    def _format_display_value(self, record: Dict, col) -> str:
        """
        Format a value for display with locale-aware formatting for all types.
        
        Args:
            record: The record dictionary.
            col: The column definition.
            
        Returns:
            Formatted string value.
        """
        value = record.get(col.name)
        
        if value is None:
            return ""
        
        try:
            # Get number format settings
            num_format = self._get_number_format_settings()
            
            if col.data_type == DataType.STRING:
                return str(value)
            
            elif col.data_type == DataType.INTEGER:
                int_val = int(value)
                # Format with thousands separator
                formatted = f"{abs(int_val):,}"
                if num_format['thousands'] == '.':
                    formatted = formatted.replace(',', '.')
                if int_val < 0:
                    formatted = '-' + formatted
                return formatted
            
            elif col.data_type == DataType.FLOAT:
                float_val = float(value)
                # Format with 2 decimals and thousands separator
                formatted = f"{abs(float_val):,.2f}"
                if num_format['thousands'] == '.' and num_format['decimal'] == ',':
                    # EU format: swap . and ,
                    formatted = formatted.replace(',', 'TEMP').replace('.', ',').replace('TEMP', '.')
                if float_val < 0:
                    formatted = '-' + formatted
                return formatted
            
            elif col.data_type == DataType.CURRENCY:
                float_val = float(value)
                # Format number part
                formatted = f"{abs(float_val):,.2f}"
                if num_format['thousands'] == '.' and num_format['decimal'] == ',':
                    formatted = formatted.replace(',', 'TEMP').replace('.', ',').replace('TEMP', '.')
                if float_val < 0:
                    formatted = '-' + formatted
                # Add currency symbol
                symbol = num_format['currency_symbol']
                if num_format['currency_position'] == 'before':
                    return f"{symbol}{formatted}"
                else:
                    return f"{formatted} {symbol}"
            
            elif col.data_type == DataType.PERCENTAGE:
                float_val = float(value)
                formatted = f"{abs(float_val):,.1f}"
                if num_format['thousands'] == '.' and num_format['decimal'] == ',':
                    formatted = formatted.replace(',', 'TEMP').replace('.', ',').replace('TEMP', '.')
                if float_val < 0:
                    formatted = '-' + formatted
                return f"{formatted}%"
            
            elif col.data_type == DataType.DATE:
                if hasattr(value, 'strftime'):
                    if not hasattr(self, '_date_strformat'):
                        self._get_mask_for_datatype(DataType.DATE)
                    strformat = getattr(self, '_date_strformat', '%Y-%m-%d')
                    return value.strftime(strformat)
                return str(value)
            
            elif col.data_type == DataType.DATETIME:
                if hasattr(value, 'strftime'):
                    if not hasattr(self, '_datetime_strformat'):
                        self._get_mask_for_datatype(DataType.DATETIME)
                    strformat = getattr(self, '_datetime_strformat', '%Y-%m-%d %H:%M')
                    return value.strftime(strformat)
                return str(value)
            
            elif col.data_type == DataType.BOOLEAN:
                return "Yes" if value else "No"
            
            else:
                return str(value)
                
        except (ValueError, TypeError, AttributeError):
            return str(value)
    
    def _get_number_format_settings(self) -> Dict:
        """
        Get number format settings based on locale configuration.
        
        Returns:
            Dict with 'thousands', 'decimal', 'currency_symbol', 'currency_position'
        """
        # Cache the settings
        if hasattr(self, '_number_format_settings'):
            return self._number_format_settings
        
        num_format = self._number_format
        currency_symbol = self._currency_symbol
        currency_position = self._currency_position
        
        # Auto-detect from system locale if needed
        if num_format == 'system' or currency_symbol == 'system' or currency_position == 'system':
            detected = self._detect_system_number_format()
            if num_format == 'system':
                num_format = detected['format']
            if currency_symbol == 'system':
                currency_symbol = detected['symbol']
            if currency_position == 'system':
                currency_position = detected['position']
        
        # Set separators based on format
        if num_format == 'EU':
            thousands = '.'
            decimal = ','
        else:  # US or ISO
            thousands = ','
            decimal = '.'
        
        self._number_format_settings = {
            'thousands': thousands,
            'decimal': decimal,
            'currency_symbol': currency_symbol,
            'currency_position': currency_position
        }
        
        return self._number_format_settings
    
    def _detect_system_number_format(self) -> Dict:
        """
        Detect system number format based on locale.
        
        Returns:
            Dict with 'format', 'symbol', 'position'
        """
        import locale
        try:
            loc = locale.getlocale()[0] or locale.getdefaultlocale()[0] or ''
            loc_lower = loc.lower()
            
            # Determine format (EU uses dot for thousands, comma for decimal)
            eu_locales = ['es_', 'fr_', 'de_', 'it_', 'pt_', 'nl_', 'pl_', 'ru_', 'uk_',
                         'el_', 'cs_', 'sk_', 'hu_', 'ro_', 'bg_', 'hr_', 'sl_', 'et_', 
                         'lv_', 'lt_', 'fi_', 'sv_', 'da_', 'no_', 'is_']
            
            is_eu = any(eu in loc_lower for eu in eu_locales)
            
            # Currency symbols and positions by region
            currency_map = {
                'es_': ('€', 'after'),
                'fr_': ('€', 'after'),
                'de_': ('€', 'after'),
                'it_': ('€', 'after'),
                'pt_': ('€', 'after'),
                'nl_': ('€', 'after'),
                'en_gb': ('£', 'before'),
                'en_us': ('$', 'before'),
                'en_au': ('$', 'before'),
                'en_ca': ('$', 'before'),
                'ja_': ('¥', 'before'),
                'zh_': ('¥', 'before'),
                'ko_': ('₩', 'before'),
                'ru_': ('₽', 'after'),
                'pl_': ('zł', 'after'),
                'br_': ('R$', 'before'),
            }
            
            symbol = '$'
            position = 'before'
            
            for pattern, (sym, pos) in currency_map.items():
                if pattern in loc_lower:
                    symbol = sym
                    position = pos
                    break
            
            return {
                'format': 'EU' if is_eu else 'US',
                'symbol': symbol,
                'position': position
            }
        except:
            return {'format': 'US', 'symbol': '$', 'position': 'before'}
    
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
            
            # Calculate row width including action column if shown
            row_width = sum(c.width for c in columns)
            if self._show_action_column:
                row_width += self._action_column_width
            
            row_panel = Panel(self._rows_panel, {
                'Left': 0, 'Top': y,
                'Width': row_width,
                'Height': self._row_height,
                'BackColor': bg_color
            })
            
            widgets = []
            x = 0
            for col in columns:
                # Get formatted value with locale-aware date formatting
                value = self._format_display_value(record, col)
                
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
            
            # Add action buttons if enabled
            action_buttons = []
            if self._show_action_column:
                btn_y = (self._row_height - 24) // 2
                
                if self._allow_edit:
                    edit_btn = Button(row_panel, {
                        'Text': '✏️',
                        'Left': x + 5, 'Top': btn_y,
                        'Width': 28, 'Height': 24,
                        'Font': Font('Segoe UI', 9)
                    })
                    edit_btn.Click = lambda s, e, i=idx: self.BeginEdit(i)
                    action_buttons.append(edit_btn)
                    x += 30
                
                if self._allow_delete:
                    delete_btn = Button(row_panel, {
                        'Text': '🗑️',
                        'Left': x + 5, 'Top': btn_y,
                        'Width': 28, 'Height': 24,
                        'Font': Font('Segoe UI', 9)
                    })
                    delete_btn.Click = lambda s, e, i=idx: self.DeleteRecord(i)
                    action_buttons.append(delete_btn)
            
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
                'action_buttons': action_buttons,
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
    # CRUD Properties and Methods
    # =========================================================================
    
    @property
    def AllowEdit(self) -> bool:
        """Get whether inline editing is allowed."""
        return self._allow_edit
    
    @AllowEdit.setter
    def AllowEdit(self, value: bool):
        """Set whether inline editing is allowed."""
        self._allow_edit = value
    
    @property
    def AllowAdd(self) -> bool:
        """Get whether adding new rows is allowed."""
        return self._allow_add
    
    @AllowAdd.setter
    def AllowAdd(self, value: bool):
        """Set whether adding new rows is allowed."""
        self._allow_add = value
    
    @property
    def AllowDelete(self) -> bool:
        """Get whether deleting rows is allowed."""
        return self._allow_delete
    
    @AllowDelete.setter
    def AllowDelete(self, value: bool):
        """Set whether deleting rows is allowed."""
        self._allow_delete = value
    
    @property
    def ShowActionColumn(self) -> bool:
        """Get whether the action column (Edit/Save/Delete buttons) is shown."""
        return self._show_action_column
    
    @ShowActionColumn.setter
    def ShowActionColumn(self, value: bool):
        """Set whether the action column is shown."""
        if self._show_action_column == value:
            return
        self._show_action_column = value
        self._rebuild_grid()
    
    @property
    def IsEditing(self) -> bool:
        """Check if a row is currently being edited."""
        return self._editing_row_index is not None
    
    @property
    def EditingRowIndex(self) -> Optional[int]:
        """Get the index of the row currently being edited."""
        return self._editing_row_index
    
    def BeginEdit(self, index: int = None):
        """
        Begin editing a row. If no index specified, edits the selected row.
        
        Args:
            index: The row index to edit. If None, uses selected row.
        """
        if not self._allow_edit:
            return
        
        if index is None:
            indices = self.manager.selected_indices
            if not indices:
                return
            index = indices[0]
        
        if index < 0 or index >= len(self.manager.records):
            return
        
        # Cancel any current edit first
        if self._editing_row_index is not None:
            self.CancelEdit()
        
        self._editing_row_index = index
        self._is_adding_row = False
        record = self.manager.records[index]
        
        # Convert row to edit mode
        self._convert_row_to_edit_mode(index)
        
        self.EditStarted(self, {'index': index, 'record': record})
    
    def BeginAdd(self):
        """Begin adding a new row."""
        if not self._allow_add:
            return
        
        # Cancel any current edit first
        if self._editing_row_index is not None:
            self.CancelEdit()
        
        # Create empty record with default values
        columns = self.manager.columns
        new_record = {}
        for col in columns:
            if col.data_type.value in ('integer', 'float', 'currency', 'percentage'):
                new_record[col.name] = 0
            elif col.data_type.value == 'boolean':
                new_record[col.name] = False
            else:
                new_record[col.name] = ''
        
        self._is_adding_row = True
        self._editing_row_index = len(self.manager.records)  # New row at end
        
        # Add temporary row to UI
        self._add_edit_row(new_record)
        
        self.EditStarted(self, {'index': self._editing_row_index, 'record': new_record, 'is_new': True})
    
    def SaveEdit(self) -> bool:
        """
        Save the current edit.
        
        Returns:
            True if save was successful, False otherwise.
        """
        if self._editing_row_index is None:
            return False
        
        # Get values from edit widgets
        row_data = self._row_widgets[self._editing_row_index] if self._editing_row_index < len(self._row_widgets) else None
        if not row_data or 'edit_widgets' not in row_data:
            return False
        
        # Collect values from edit widgets
        new_values = {}
        columns = [c for c in self.manager.columns if c.visible]
        edit_widgets = row_data.get('edit_widgets', [])
        
        for i, col in enumerate(columns):
            if i < len(edit_widgets):
                widget = edit_widgets[i]
                # Check for CheckBox first (has both Text and Checked)
                if hasattr(widget, 'Checked') and isinstance(widget, CheckBox):
                    new_values[col.name] = widget.Checked
                elif hasattr(widget, 'Text'):
                    raw_value = widget.Text
                    # Convert from masked format to clean value
                    new_values[col.name] = self._parse_masked_value(raw_value, col.data_type)
        
        # Validate
        backend = self.manager.backend
        is_valid, error_msg = backend.validate_record(new_values, is_new=self._is_adding_row)
        if not is_valid:
            print(f"Validation error: {error_msg}")  # TODO: Show in UI
            return False
        
        try:
            if self._is_adding_row:
                # Create new record
                created = backend.create_record(new_values)
                self._editing_row_index = None
                self._is_adding_row = False
                self.manager.refresh()
                self.RecordCreated(self, {'record': created})
            else:
                # Update existing record
                pk = backend.get_primary_key()
                if pk:
                    original = self.manager.records[self._editing_row_index]
                    pk_value = original.get(pk)
                    success = backend.update_record(pk_value, new_values)
                    if success:
                        self._editing_row_index = None
                        self.manager.refresh()
                        self.RecordUpdated(self, {'record': new_values})
                    else:
                        return False
                else:
                    # No primary key - just update in place
                    self._editing_row_index = None
                    self.manager.refresh()
            return True
        except Exception as e:
            print(f"Save error: {e}")  # TODO: Show in UI
            return False
    
    def _parse_masked_value(self, raw_value: str, data_type: DataType):
        """
        Parse a value from masked input format to clean value.
        Uses locale-aware parsing for numeric types.
        
        Args:
            raw_value: The raw string from the input widget
            data_type: The expected data type
            
        Returns:
            The parsed value in the appropriate type
        """
        if not raw_value:
            return None
        
        # Remove mask characters and placeholders
        clean = raw_value.replace('_', '').strip()
        
        if not clean:
            return None
        
        # Get number format for locale-aware parsing
        num_format = self._get_number_format_settings()
        
        try:
            if data_type == DataType.INTEGER:
                # Remove thousands separator (could be . or ,)
                if num_format['thousands'] == '.':
                    clean = clean.replace('.', '')
                else:
                    clean = clean.replace(',', '')
                return int(clean)
            
            elif data_type == DataType.FLOAT:
                # Normalize to standard float format
                if num_format['decimal'] == ',':
                    # EU format: remove . (thousands), replace , with . (decimal)
                    clean = clean.replace('.', '').replace(',', '.')
                else:
                    # US format: just remove , (thousands)
                    clean = clean.replace(',', '')
                return float(clean)
            
            elif data_type == DataType.CURRENCY:
                # Remove currency symbols and normalize
                for sym in ['$', '€', '£', '¥', '₩', '₽', 'zł', 'R$']:
                    clean = clean.replace(sym, '')
                clean = clean.strip()
                if num_format['decimal'] == ',':
                    clean = clean.replace('.', '').replace(',', '.')
                else:
                    clean = clean.replace(',', '')
                return float(clean) if clean else None
            
            elif data_type == DataType.PERCENTAGE:
                # Remove % and normalize
                clean = clean.replace('%', '').strip()
                if num_format['decimal'] == ',':
                    clean = clean.replace('.', '').replace(',', '.')
                else:
                    clean = clean.replace(',', '')
                return float(clean) if clean else None
            
            elif data_type == DataType.DATE:
                # Parse date using locale-aware format
                from datetime import datetime
                strformat = getattr(self, '_date_strformat', '%Y-%m-%d')
                return datetime.strptime(clean, strformat).date()
            
            elif data_type == DataType.DATETIME:
                # Parse datetime using locale-aware format
                from datetime import datetime
                strformat = getattr(self, '_datetime_strformat', '%Y-%m-%d %H:%M')
                return datetime.strptime(clean, strformat)
            
            else:
                # STRING or unknown - return as-is
                return raw_value
                
        except (ValueError, TypeError):
            # If parsing fails, return original value
            return raw_value
    
    def CancelEdit(self):
        """Cancel the current edit and restore original values."""
        if self._editing_row_index is None:
            return
        
        was_adding = self._is_adding_row
        index = self._editing_row_index
        
        self._editing_row_index = None
        self._is_adding_row = False
        
        # Rebuild rows to restore normal display
        self._build_rows()
        
        self.EditCancelled(self, {'index': index, 'was_adding': was_adding})
    
    def DeleteRecord(self, index: int = None) -> bool:
        """
        Delete a record. If no index specified, deletes the selected row.
        
        Args:
            index: The row index to delete. If None, uses selected row.
            
        Returns:
            True if delete was successful, False otherwise.
        """
        if not self._allow_delete:
            print("❌ Delete failed: AllowDelete is False")
            return False
        
        if index is None:
            indices = self.manager.selected_indices
            if not indices:
                print("❌ Delete failed: No row selected")
                return False
            index = indices[0]
        
        if index < 0 or index >= len(self.manager.records):
            print(f"❌ Delete failed: Invalid index {index}")
            return False
        
        backend = self.manager.backend
        if not backend.supports_crud():
            print("❌ Delete failed: Backend does not support CRUD")
            return False
        
        try:
            pk = backend.get_primary_key()
            if pk:
                record = self.manager.records[index]
                pk_value = record.get(pk)
                print(f"🗑️ Deleting record with {pk}={pk_value}...")
                success = backend.delete_record(pk_value)
                if success:
                    self.manager.refresh()
                    self.RecordDeleted(self, {'record': record})
                    print(f"✅ Record deleted successfully")
                    return True
                else:
                    print(f"❌ Delete failed: Backend returned False")
            else:
                print("❌ Delete failed: No primary key defined")
            return False
        except Exception as e:
            print(f"Delete error: {e}")  # TODO: Show in UI
            return False
    
    def _get_mask_for_datatype(self, data_type: DataType) -> str:
        """
        Get the appropriate mask for a data type based on locale settings.
        
        Returns:
            Mask string for MaskedTextBox, or empty string for no mask.
            Only DATE and DATETIME use masks; numeric types use TextBox with validation.
            
        Mask formats by DateFormat:
            - 'ISO': YYYY-MM-DD (international standard)
            - 'EU':  DD/MM/YYYY (European: Spain, France, Germany, etc.)
            - 'US':  MM/DD/YYYY (United States)
            - 'system': Auto-detect from system locale
        """
        date_format = self._date_format
        time_format = self._time_format
        
        # Auto-detect from system locale if 'system'
        if date_format == 'system':
            date_format = self._detect_system_date_format()
        
        # Define masks based on format
        if date_format == 'EU':  # DD/MM/YYYY
            date_mask = '00/00/0000'
            datetime_mask = '00/00/0000 00:00' if time_format == '24h' else '00/00/0000 00:00 LL'
            date_strformat = '%d/%m/%Y'
            datetime_strformat = '%d/%m/%Y %H:%M' if time_format == '24h' else '%d/%m/%Y %I:%M %p'
        elif date_format == 'US':  # MM/DD/YYYY
            date_mask = '00/00/0000'
            datetime_mask = '00/00/0000 00:00' if time_format == '24h' else '00/00/0000 00:00 LL'
            date_strformat = '%m/%d/%Y'
            datetime_strformat = '%m/%d/%Y %H:%M' if time_format == '24h' else '%m/%d/%Y %I:%M %p'
        else:  # ISO (default): YYYY-MM-DD
            date_mask = '0000-00-00'
            datetime_mask = '0000-00-00 00:00'
            date_strformat = '%Y-%m-%d'
            datetime_strformat = '%Y-%m-%d %H:%M'
        
        # Store strformat for value parsing/formatting
        self._date_strformat = date_strformat
        self._datetime_strformat = datetime_strformat
        
        masks = {
            DataType.DATE: date_mask,
            DataType.DATETIME: datetime_mask,
        }
        return masks.get(data_type, '')
    
    def _detect_system_date_format(self) -> str:
        """
        Detect the system's date format based on locale.
        
        Returns:
            'EU', 'US', or 'ISO' based on system locale.
        """
        import locale
        try:
            # Get system locale
            loc = locale.getlocale()[0] or locale.getdefaultlocale()[0] or ''
            loc_lower = loc.lower()
            
            # US format countries
            us_locales = ['en_us', 'en_ph', 'en_bz', 'en_fm', 'en_mh', 'en_pw']
            
            # Check if US format
            if any(us in loc_lower for us in us_locales):
                return 'US'
            
            # Most of the world uses EU format (DD/MM/YYYY) or ISO
            # European and Latin American countries
            eu_locales = ['es_', 'fr_', 'de_', 'it_', 'pt_', 'nl_', 'pl_', 'ru_', 'uk_',
                         'en_gb', 'en_au', 'en_nz', 'en_ie', 'en_za', 'en_in']
            
            if any(eu in loc_lower for eu in eu_locales):
                return 'EU'
            
            # Default to ISO for others (Asian countries, etc.)
            return 'ISO'
        except:
            return 'ISO'
    
    def _create_edit_widget(self, row_panel, col, value, x: int, is_new: bool = False):
        """
        Create the appropriate edit widget for a column based on its data type.
        
        Args:
            row_panel: Parent panel for the widget
            col: ColumnDefinition for the field
            value: Current value
            x: X position for the widget
            is_new: If True, show placeholder text
            
        Returns:
            The created widget (CheckBox, MaskedTextBox, or TextBox)
        """
        if col.data_type == DataType.BOOLEAN:
            # Use checkbox for boolean (no text label)
            return CheckBox(row_panel, {
                'Text': '',
                'Left': x + (col.width // 2) - 10, 
                'Top': (self._row_height - 20) // 2,
                'Width': 20,
                'Height': 20,
                'Checked': bool(value)
            })
        
        # Get mask for this data type (only DATE/DATETIME)
        mask = self._get_mask_for_datatype(col.data_type)
        
        # Get number format settings for locale-aware formatting
        num_format = self._get_number_format_settings()
        
        # Format value for display using locale-aware format
        display_value = ''
        if value is not None:
            if col.data_type == DataType.DATE:
                if hasattr(value, 'strftime'):
                    strformat = getattr(self, '_date_strformat', '%Y-%m-%d')
                    display_value = value.strftime(strformat)
                else:
                    display_value = str(value)
            elif col.data_type == DataType.DATETIME:
                if hasattr(value, 'strftime'):
                    strformat = getattr(self, '_datetime_strformat', '%Y-%m-%d %H:%M')
                    display_value = value.strftime(strformat)
                else:
                    display_value = str(value)
            elif col.data_type == DataType.FLOAT:
                # Format with locale-aware decimal separator
                try:
                    float_val = float(value)
                    if num_format['decimal'] == ',':
                        display_value = f"{float_val:.2f}".replace('.', ',')
                    else:
                        display_value = f"{float_val:.2f}"
                except:
                    display_value = str(value)
            elif col.data_type == DataType.CURRENCY:
                # Format with locale-aware decimal separator (without symbol for editing)
                try:
                    float_val = float(value)
                    if num_format['decimal'] == ',':
                        display_value = f"{float_val:.2f}".replace('.', ',')
                    else:
                        display_value = f"{float_val:.2f}"
                except:
                    display_value = str(value)
            elif col.data_type == DataType.PERCENTAGE:
                # Format with locale-aware decimal separator (without % for editing)
                try:
                    float_val = float(value)
                    if num_format['decimal'] == ',':
                        display_value = f"{float_val:.1f}".replace('.', ',')
                    else:
                        display_value = f"{float_val:.1f}"
                except:
                    display_value = str(value)
            else:
                display_value = str(value)
        
        widget_props = {
            'Left': x + 2, 
            'Top': 3,
            'Width': col.width - 4,
            'Height': self._row_height - 6,
            'Font': Font('Segoe UI', 9)
        }
        
        if mask:
            # Use MaskedTextBox for DATE/DATETIME (fixed-length formats)
            widget_props['Mask'] = mask
            widget_props['PromptChar'] = '_'
            widget = MaskedTextBox(row_panel, widget_props)
            # Set text after creation to ensure proper mask application
            if display_value:
                widget.Text = display_value
            return widget
        else:
            # Use regular TextBox for strings and numbers
            widget_props['Text'] = display_value
            if is_new:
                widget_props['PlaceholderText'] = col.header
            return TextBox(row_panel, widget_props)
    
    def _convert_row_to_edit_mode(self, index: int):
        """Convert a row from display to edit mode."""
        if index >= len(self._row_widgets):
            return
        
        row_data = self._row_widgets[index]
        row_panel = row_data['panel']
        record = row_data['record']
        columns = [c for c in self.manager.columns if c.visible]
        
        # Change background to indicate editing
        row_panel.BackColor = '#FFF8E1'  # Light yellow for editing
        
        # Destroy existing cell widgets and action buttons
        for widget in row_data.get('widgets', []):
            if hasattr(widget, '_tk_widget') and widget._tk_widget:
                widget._tk_widget.destroy()
        for btn in row_data.get('action_buttons', []):
            if hasattr(btn, '_tk_widget') and btn._tk_widget:
                btn._tk_widget.destroy()
        
        # Create edit widgets with appropriate masks
        edit_widgets = []
        x = 0
        for col in columns:
            value = record.get(col.name, '')
            edit_widget = self._create_edit_widget(row_panel, col, value, x, is_new=False)
            edit_widgets.append(edit_widget)
            x += col.width
        
        # Add Save/Cancel buttons in action column area
        edit_action_buttons = []
        if self._show_action_column:
            btn_y = (self._row_height - 24) // 2
            
            save_btn = Button(row_panel, {
                'Text': '✓',
                'Left': x + 5, 'Top': btn_y,
                'Width': 28, 'Height': 24,
                'Font': Font('Segoe UI', 10),
                'BackColor': '#4CAF50',
                'ForeColor': '#FFFFFF'
            })
            save_btn.Click = lambda s, e: self.SaveEdit()
            edit_action_buttons.append(save_btn)
            
            cancel_btn = Button(row_panel, {
                'Text': '✗',
                'Left': x + 38, 'Top': btn_y,
                'Width': 28, 'Height': 24,
                'Font': Font('Segoe UI', 10),
                'BackColor': '#F44336',
                'ForeColor': '#FFFFFF'
            })
            cancel_btn.Click = lambda s, e: self.CancelEdit()
            edit_action_buttons.append(cancel_btn)
        
        row_data['edit_widgets'] = edit_widgets
        row_data['edit_action_buttons'] = edit_action_buttons
        row_data['widgets'] = []  # Clear display widgets
        row_data['action_buttons'] = []  # Clear normal action buttons
    
    def _add_edit_row(self, record: Dict):
        """Add a new row in edit mode for adding a new record."""
        columns = [c for c in self.manager.columns if c.visible]
        y = len(self._row_widgets) * self._row_height
        
        # Calculate row width including action column
        row_width = sum(c.width for c in columns)
        if self._show_action_column:
            row_width += self._action_column_width
        
        row_panel = Panel(self._rows_panel, {
            'Left': 0, 'Top': y,
            'Width': row_width,
            'Height': self._row_height,
            'BackColor': '#FFFDE7'  # Light yellow for new row
        })
        
        # Create edit widgets with appropriate masks
        edit_widgets = []
        x = 0
        for col in columns:
            value = record.get(col.name, '')
            edit_widget = self._create_edit_widget(row_panel, col, value, x, is_new=True)
            edit_widgets.append(edit_widget)
            x += col.width
        
        # Add Save/Cancel buttons for new row
        edit_action_buttons = []
        if self._show_action_column:
            btn_y = (self._row_height - 24) // 2
            
            save_btn = Button(row_panel, {
                'Text': '✓',
                'Left': x + 5, 'Top': btn_y,
                'Width': 28, 'Height': 24,
                'Font': Font('Segoe UI', 10),
                'BackColor': '#4CAF50',
                'ForeColor': '#FFFFFF'
            })
            save_btn.Click = lambda s, e: self.SaveEdit()
            edit_action_buttons.append(save_btn)
            
            cancel_btn = Button(row_panel, {
                'Text': '✗',
                'Left': x + 38, 'Top': btn_y,
                'Width': 28, 'Height': 24,
                'Font': Font('Segoe UI', 10),
                'BackColor': '#F44336',
                'ForeColor': '#FFFFFF'
            })
            cancel_btn.Click = lambda s, e: self.CancelEdit()
            edit_action_buttons.append(cancel_btn)
        
        self._row_widgets.append({
            'panel': row_panel,
            'widgets': [],
            'edit_widgets': edit_widgets,
            'edit_action_buttons': edit_action_buttons,
            'action_buttons': [],
            'record': record,
            'index': len(self._row_widgets)
        })

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
    
    # =========================================================================
    # Demo 2: CRUD Inline DataGrid
    # =========================================================================
    class CrudDemoBackend(DataGridBackend):
        """Demo backend that supports CRUD operations."""
        
        def __init__(self):
            """Initialize with some sample products."""
            from datetime import date
            self._next_id = 6
            self._data = [
                {"id": 1, "name": "Laptop", "category": "Electronics", "price": 999.99, "stock": 50, "active": True, "created": date(2024, 1, 15)},
                {"id": 2, "name": "Mouse", "category": "Electronics", "price": 29.99, "stock": 200, "active": True, "created": date(2024, 2, 20)},
                {"id": 3, "name": "Keyboard", "category": "Electronics", "price": 79.99, "stock": 150, "active": True, "created": date(2024, 3, 10)},
                {"id": 4, "name": "Monitor", "category": "Electronics", "price": 349.99, "stock": 75, "active": True, "created": date(2024, 4, 5)},
                {"id": 5, "name": "Headphones", "category": "Audio", "price": 149.99, "stock": 100, "active": False, "created": date(2024, 5, 18)},
            ]
            self._columns = [
                ColumnDefinition("id", "ID", DataType.INTEGER, width=60, align="right"),
                ColumnDefinition("name", "Product Name", DataType.STRING, width=150),
                ColumnDefinition("category", "Category", DataType.STRING, width=100),
                ColumnDefinition("price", "Price", DataType.CURRENCY, width=80, align="right"),
                ColumnDefinition("stock", "Stock", DataType.INTEGER, width=60, align="right"),
                ColumnDefinition("active", "Active", DataType.BOOLEAN, width=60, align="center"),
                ColumnDefinition("created", "Created", DataType.DATE, width=110, align="center"),
            ]
        
        def get_columns(self) -> List[ColumnDefinition]:
            return self._columns
        
        def fetch_data(self, request: DataRequest) -> DataResponse:
            filtered = self._data.copy()
            
            # Apply search
            if request.search_text:
                search_lower = request.search_text.lower()
                filtered = [r for r in filtered 
                           if search_lower in r.get("name", "").lower() or
                              search_lower in r.get("category", "").lower()]
            
            # Apply sorting
            if request.sort_column and request.sort_order != SortOrder.NONE:
                reverse = request.sort_order == SortOrder.DESCENDING
                filtered.sort(key=lambda x: (x.get(request.sort_column) is None, 
                                            x.get(request.sort_column)), reverse=reverse)
            
            total = len(filtered)
            total_pages = max(1, (total + request.page_size - 1) // request.page_size)
            current_page = min(request.page, total_pages)
            start = (current_page - 1) * request.page_size
            end = start + request.page_size
            
            return DataResponse(
                records=filtered[start:end],
                page_info=PageInfo(current_page=current_page, page_size=request.page_size,
                                  total_records=total, total_pages=total_pages),
                columns=self._columns
            )
        
        # CRUD Methods
        def supports_crud(self) -> bool:
            return True
        
        def get_primary_key(self) -> str:
            return "id"
        
        def create_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
            new_record = record.copy()
            new_record["id"] = self._next_id
            self._next_id += 1
            # Convert types
            if "price" in new_record:
                try:
                    new_record["price"] = float(new_record["price"])
                except: new_record["price"] = 0.0
            if "stock" in new_record:
                try:
                    new_record["stock"] = int(new_record["stock"])
                except: new_record["stock"] = 0
            self._data.append(new_record)
            print(f"✅ Created: {new_record}")
            return new_record
        
        def update_record(self, primary_key_value: Any, changes: Dict[str, Any]) -> bool:
            for i, record in enumerate(self._data):
                if record.get("id") == primary_key_value:
                    # Convert types
                    if "price" in changes:
                        try:
                            changes["price"] = float(changes["price"])
                        except: changes["price"] = record.get("price", 0.0)
                    if "stock" in changes:
                        try:
                            changes["stock"] = int(changes["stock"])
                        except: changes["stock"] = record.get("stock", 0)
                    self._data[i].update(changes)
                    print(f"✅ Updated ID {primary_key_value}: {changes}")
                    return True
            return False
        
        def delete_record(self, primary_key_value: Any) -> bool:
            for i, record in enumerate(self._data):
                if record.get("id") == primary_key_value:
                    deleted = self._data.pop(i)
                    print(f"🗑️ Deleted: {deleted.get('name')} (ID: {primary_key_value})")
                    return True
            return False
        
        def validate_record(self, record: Dict[str, Any], is_new: bool = False) -> tuple:
            if not record.get("name"):
                return False, "Product name is required"
            if not record.get("category"):
                return False, "Category is required"
            return True, ""
    
    def demo_crud():
        """CRUD Inline DataGrid demo."""
        form = Form()
        form.Text = "DataGrid CRUD Demo - Product Inventory"
        form.Width = 900
        form.Height = 500
        form.StartPosition = 'CenterScreen'
        form.ApplyLayout()
        
        # Create CRUD-enabled backend
        backend = CrudDemoBackend()
        manager = DataGridManager(backend)
        
        # Create data grid with CRUD enabled
        grid = DataGridPanel(form, props={
            'Dock': DockStyle.Fill,
            'AllowEdit': True,
            'AllowAdd': True,
            'AllowDelete': True,
            'ShowActionColumn': True,
            'ActionColumnWidth': 80
        }, manager=manager)
        
        # CRUD Event handlers
        grid.RecordCreated = lambda s, e: print(f"Event: RecordCreated - {e.get('record', {}).get('name')}")
        grid.RecordUpdated = lambda s, e: print(f"Event: RecordUpdated - {e.get('record', {}).get('name')}")
        grid.RecordDeleted = lambda s, e: print(f"Event: RecordDeleted - {e.get('record', {}).get('name')}")
        grid.EditStarted = lambda s, e: print(f"Event: EditStarted - Row {e.get('index')}")
        grid.EditCancelled = lambda s, e: print(f"Event: EditCancelled - Row {e.get('index')}")
        
        # Load data
        manager.refresh()
        
        # Instructions
        print("=" * 60)
        print("DataGrid CRUD Demo - Product Inventory")
        print("=" * 60)
        print("\nCRUD Features:")
        print("  - Click ➕ Add button to add a new product")
        print("  - Click ✏️ (edit) to edit a row inline")
        print("  - Click 🗑️ (delete) to delete a row")
        print("  - When editing: ✓ to save, ✗ to cancel")
        print("=" * 60)
        
        form.ShowDialog()
    
    # Menu to choose demo
    def main():
        print("\n" + "=" * 50)
        print("DataGridPanel Demos")
        print("=" * 50)
        print("1. Basic DataGrid with events")
        print("2. CRUD Inline DataGrid")
        print("=" * 50)
        
        choice = input("Select demo (1-2): ").strip()
        
        if choice == "1":
            demo_basic()
        elif choice == "2":
            demo_crud()
        else:
            print("Invalid choice. Running basic demo...")
            demo_basic()
    
    main()
